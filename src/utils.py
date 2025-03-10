import pickle
import os
from src import dataset
from src import api_doc
from sacremoses import MosesTokenizer
from pptx.dml.color import RGBColor
import win32com.client, pythoncom
import tiktoken
import json
import re

def write_list(lst, filename):
    with open(filename, "wb") as f:
        pickle.dump(lst, f)

def read_list(filename):
    with open(filename, 'rb') as f:
        lst = pickle.load(f)
    return lst

def write_lines(lst, path):
    with open(path, 'w', encoding="utf-8") as file:
        for s in lst:
            file.write(s)
            file.write('\n')

def read_lines(path):
    data = []
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            data.append(line.strip())
    
    return data

def makedir(path):
    if not os.path.exists(path):
        os.makedirs(path)

def merge_list(lst):
    merged = []
    for l in lst:
        merged.extend(l)
    return merged

def get_picture_name(labels):
    # labels: all api list
    picture_name = []
    for api in labels:
        if "insert_picture(" in api:
            try:
                start_idx = api.index('insert_picture("')
                end_idx = api.index('")')
                s = api[start_idx+len('insert_picture("'):end_idx]
            except:
                start_idx = api.index("insert_picture('")
                end_idx = api.index("')")
                s = api[start_idx+len("insert_picture('"):end_idx]
            picture_name.append(s)
    return picture_name

def get_picture_name_list(args):
    instruction_data, label_data = dataset.load_data_v2(args.data_path)
    # [[["choose_content()","insert_triangle()"],['choose_shape("triangle 1")',"align_top_left_corner()"]]]
    label_list = []
    for x in label_data:
        for xx in x:
            label_list.extend(xx)
    labels = get_picture_name(label_list)
    write_lines(labels, f"{args.data_path}/pictures.txt")
    return labels

# def parse_api(codes):
#     # print(f"== Raw Codes ==\n{codes}\n\n")
#     apis = []
#     start = "<code>"
#     end = "</code>"
#     while start in codes and end in codes:
#         start_index = codes.index(start)
#         end_index = codes.index(end)
#         code = codes[start_index + len(start): end_index]
#         codes = codes[end_index+len(end):]
#         parsed = code.strip().split(';')
#         parsed = [x.strip() for x in parsed if x!='']
#         apis.extend(parsed)
    
#     # print(f"== Parsed Codes ==\n{apis}\n\n")
    
#     return apis

def parse_api(codes):
    # print(f"== Raw Codes ==\n{codes}\n\n")
    apis = []
    start = "<code>"
    end = "</code>"
    while start in codes and end in codes:
        start_index = codes.index(start)
        end_index = codes.index(end)
        code = codes[start_index + len(start): end_index]
        codes = codes[end_index+len(end):]
        lines = code.strip().split('\n')
        for line in lines:
            parsed = line.strip().split(';')
            for x in parsed:
                if len(x)!=0 and x[-1]==')':
                    apis.append(x.strip())
    if len(apis)==0:
        start = "<code>"
        end = "</code"
        while start in codes and end in codes:
            start_index = codes.index(start)
            end_index = codes.index(end)
            code = codes[start_index + len(start): end_index]
            codes = codes[end_index + len(end):]
            lines = code.strip().split('\n')
            for line in lines:
                parsed = line.strip().split(';')
                for x in parsed:
                    if len(x) != 0 and x[-1] == ')':
                        apis.append(x.strip())
    if len(apis)==0:
        start="```scss"
        end="```"
        while start in codes and end in codes:
            start_index = codes.index(start)
            end_index = codes.rindex(end)
            code = codes[start_index + len(start): end_index]
            codes = codes[end_index + len(end):]
            lines = code.strip().split('\n')
            for line in lines:
                parsed = line.strip().split(';')
                for x in parsed:
                    if len(x) != 0 and x[-1] == ')':
                        apis.append(x.strip())
    if len(apis)==0:
        start="```scss"
        end="```"
        while start in codes and end in codes:
            start_index = codes.index(start)
            end_index = codes.index("```", start_index + len(start))#rindex(end)
            code = codes[start_index + len(start): end_index]
            codes = codes[end_index + len(end):]
            lines = code.strip().split('\n')
            for line in lines:
                parsed = line.strip().split(';')
                for x in parsed:
                    if len(x) != 0 and x[-1] == ')':
                        apis.append(x.strip())
    if len(apis)==0:
        start="```python"
        end="```"
        while start in codes and end in codes:
            start_index = codes.index(start)
            end_index = codes.index("```", start_index + len(start))#rindex(end)
            code = codes[start_index + len(start): end_index]
            codes = codes[end_index + len(end):]
            lines = code.strip().split('\n')
            for line in lines:
                parsed = line.strip().split(';')
                for x in parsed:
                    if len(x) != 0 and x[-1] == ')':
                        apis.append(x.strip())
    if len(apis)==0:
        start="```"
        end="```"
        while start in codes and end in codes:
            start_index = codes.index(start)
            end_index = codes.index(end, start_index + len(start))#rindex(end)
            code = codes[start_index + len(start): end_index]
            codes = codes[end_index + len(end):]
            lines = code.strip().split('\n')
            for line in lines:
                parsed = line.strip().split(';')
                for x in parsed:
                    if len(x) != 0 and x[-1] == ')':
                        apis.append(x.strip())

    
    return apis


def parse_tool_calls(tool_calls):
    # print(tool_calls)
    apis = []
    for tool_call in tool_calls:
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)
        try:
            args_str = ', '.join(f'{key}={value!r}' for key, value in func_args.items())
        except:
            args_str = ""

        api_str = f"{func_name}({args_str})"
        apis.append(api_str)
    
    return apis


def prepare_exp_name(args):
    name = ""
    if args.robust:
        name += f'robust{args.robust_num}'
    if args.noisy:
        name += f'noisy'
    if args.tf:
        name += "tf_"
    if args.sess:
        name += "sess_"
    if args.api_update:
        name += 'up_'
    if args.api_lack:
        name += 'lack_'
    name += args.model +"_"
    if args.planning:
        name += "p"
    if args.api_selection:
        name += f"a{args.api_topk}"
    if args.content_selection:
        name += "c"
    if not (args.planning or args.api_selection or args.content_selection):
        name += "n"
    if args.second:
        name += "4"
    return name

def get_tokens(text):
    tokenizer = MosesTokenizer()
    tokens = tokenizer.tokenize(text)
    return len(tokens)

def calc_api_cost(path):
    all_apis = api_doc.get_all_APIs()
    api_names = [x.name for x in all_apis]
    line = open(path, "r", encoding="utf-8").read()
    lines = line.split('\n')
    cnt = 0
    for l in lines:
        l = l.strip(';')
        if l.endswith(')') and l.split('(')[0] in api_names:
            cnt += 1
    return cnt

def check_token(model, prompt):
    if model == 'gpt4':
        max_token_limit = 8191
    elif model == "gpt-4o-mini":
        max_token_limit = 16000
    elif model == 'text3':
        max_token_limit = 3095
    elif 'Llama' in model:

        max_token_limit = 2800
       # if '70b' in model:
        #    max_token_limit = 1200
    elif 'WizardLM':
        max_token_limit= 1200

    else:
        max_token_limit = 4095
    if model == 'text3':
        encoding_model = tiktoken.get_encoding('p50k_base')
    else:
        encoding_model = tiktoken.get_encoding('cl100k_base')
    num_tokens = len(encoding_model.encode(prompt))
    exceeded = num_tokens - max_token_limit
    return exceeded if exceeded > 0 else 0

def get_token(text, trunc_num, model):
    if model == 'text3':
        encoding_model = tiktoken.get_encoding('p50k_base')
    else:
        encoding_model = tiktoken.get_encoding('cl100k_base')
    encoded = encoding_model.encode(text)[:-trunc_num]
    truncated = encoding_model.decode(encoded)
    return truncated

def checkpoint(mode,args,idx,step):
    if not args.resume: 
        return 0
    if mode == 'prepare' and args.prepare:
        if args.api_lack:
            if os.path.exists(os.path.join(args.save_path,str(idx),str(step),"lack_after_label.pptx")):
                print(f"Prepare data Exists {idx}/{step}!")
                return 1
        else:
            if os.path.exists(os.path.join(args.save_path,str(idx),str(step),"after_label.pptx")):
                print(f"Prepare data Exists {idx}/{step}!")
                return 1    
    if mode == 'sess' and args.sess and os.path.exists(os.path.join(args.save_path,str(idx),str(step),f"{args.exp_name}_after_pred.pptx")):
        print(f"Sess data Exists {idx}!")
        return 1
    if mode == 'tf' and args.tf and os.path.exists(os.path.join(args.save_path,str(idx),str(step),f"{args.exp_name}_after_pred.pptx")):
        print(f"Tf data Exists {idx}!")
        return 1
    return 0

def sorted_list(path):
    import pdb
    #pdb.set_trace()
    return sorted(os.listdir(path),key=lambda x:int(x.split('_')[-1].split('.')[0]))

def parse_train_json(path):
    turns = []
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            data = json.loads(line)
            turn_id, instruction, label_api, base_ppt_path, label_ppt_path, api_lack_base_ppt_path, api_lack_label_ppt_path = data['Turn'],data['User instruction'],data['Feasible API sequence'],data['Base File'],data['Label File'],data['API Lack Base File'],data['API Lack Label File']
            turns.append([turn_id, instruction, label_api, base_ppt_path, label_ppt_path, api_lack_base_ppt_path, api_lack_label_ppt_path])
    return turns 

def parse_test_json(path):
    turns = []
    with open(path, 'r', encoding="utf-8") as file:
        for line in file:
            data = json.loads(line)
            turn_id, instruction, label_api, reply, pred_api, pred_ppt_path, label_ppt_path, prompt_path = data['Turn'],data['User instruction'],data['Feasible API sequence'],data['Reply'],data['Pred API sequence'],data['Pred File'],data['Label File'],data['Prompt File']
            turns.append([turn_id, instruction, label_api, reply, pred_api, pred_ppt_path, label_ppt_path, prompt_path])
    return turns

def validate_hex(hex_string):
    if re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', hex_string):
        return True
    elif re.search(r'(?:[0-9a-fA-F]{3}){1,2}$', hex_string):
        return True
    else:
        return False
    
def color_to_rgb(color_str:str):
    color_mapping = {
        "blue": "0000FF","light blue": "ADD8E6","dark blue": "00008B",
        "green": "008000","light green": "90EE90","dark green": "006400",
        "yellow": "FFFF00","light yellow": "FFFFE0","dark yellow": "BDB76B",
        "orange": "FFA500","light orange": "FFDAB9","dark orange": "FF8C00",
        "red": "FF0000","light red": "FFC0CB","dark red": "8B0000",
        "black": "000000","white": "FFFFFF","purple": "800080","pink": "FFC0CB",
    }
    # Check if input is valid hex code
    if validate_hex(color_str):
        color_hex = color_str.replace("#","")
    # Check if input has a mapped hex value
    elif color_str in color_mapping:
        color_hex = color_mapping[color_str]
    else:
        color_hex = "000000"
    
    return RGBColor.from_string(color_hex)

if __name__ == '__main__':
    # code_str = "<code>insert_picture('1.png');insert_picture('2.png')</code>##<code>insert_picture('3.png')</code>"
    # # apis = parse_api(code_str)
    # # print(apis)
    # print(get_tokens(code_str))
    # calc_api_cost("/Users/zzk/Desktop/Code/PPT_assistant/test_pptx_data_v4/0/2/p_api_pred.txt")
    api_text = """<code>
# Set the height of pictures of slide 1 as 5
move_to_slide(1);
choose_picture(0);
set_height(5);
choose_picture(1);
set_height(5);
choose_picture(2);
set_height(5);

# Set the title of slide 1 as 'The Art of Young' and underline it
move_to_slide(1);
choose_title();
delete_text();
insert_text('The Art of Young');
set_font_underline();
</code>"""
    parse_api(api_text)


def render_slides(ppt_path="test.pptx", dst_dir="slide_previews", slide_indexes=[0]):
    os.makedirs(dst_dir, exist_ok=True)
    pythoncom.CoInitialize()
    Application = win32com.client.Dispatch("PowerPoint.Application")
    full_path = os.getcwd()
    Presentation = Application.Presentations.Open(os.path.join(full_path, ppt_path), WithWindow=False)
    for slide_idx in slide_indexes:
        Presentation.Slides[slide_idx].Export(os.path.join(full_path, f"{dst_dir}/{slide_idx}.jpg"), "JPG")
    Application.Quit()