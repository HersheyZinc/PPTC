
from src import ppt_executor, ppt_reader, openai_api, prompt_factor, dataset, api_selection, utils
from src import api_doc2 as api_doc
import json

class PPT_assistant(object):
    def __init__(self, args=None):
        self.chat_history = []
        self.args = args
        self.planning = args.planning
        self.api_selection = args.api_selection
        self.content_selection = args.content_selection
        self.model = args.model
        self.model_id=args.model_id
        self.ppt = None
        self.current_page_id = 0
        self.prompt = ""

    def planner(self, instruction):
        if not self.planning:
            return [instruction]
        else:
            print('Planning...')
            planning_prompt = prompt_factor.query_decomposition_prompt.format(instruction)
            self.prompt += planning_prompt + "\n\n"
            planning_reply = openai_api.query_azure_openai(planning_prompt, model=self.model).strip()
            decomposed = planning_reply.split('\n')
            decomposed = [d.replace('</d>','') for d in decomposed if (d != '</d>') and (d != '<d>')]
            print(f"{instruction}->{decomposed}")
            return decomposed

    def api_selector(self, instruction):
        if not self.api_selection:
            all_apis =  api_selection.get_all_apis(self.args)
            return all_apis
        else:
            selected_apis = api_selection.get_selected_apis(instruction, self.args)
            print('Selecting APIs...')
            print([x.name for x in selected_apis])
            return selected_apis

    def content_selector(self, ppt_path, instruction, args, ppt):
        content, prompt = ppt_reader.get_content_by_instructions(ppt_path, instruction, args, ppt)
        self.prompt += prompt + '\n\n'
        return content

    def api_executor(self, api_lines, test=False):
        print('Executing APIs...')
        error_info = ppt_executor.API_executor(api_lines,test=test,args=self.args)
        if error_info!="":
            print(error_info)
        self.ppt = ppt_executor.get_ppt()
        self.current_page_id = ppt_executor.get_current_page_id()
    
    def load_chat_history(self, instructions, labels):
        history = []
        for idx, instruction in enumerate(instructions):
            if self.args.api_lack:
                label = api_doc.api_lack_mask(labels[idx])
            else:
                label = labels[idx]
            label_str = ";\n".join(label)
            history += [
                f"¬User¬\n{instruction}",
                f"¬AI¬:\n{label_str};",
            ]
        self.chat_history = history
        return history
    
    def load_ppt(self, path):
        ppt_executor.set_ppt(path)
        if path != None:
            self.current_page_id = len(ppt_executor.get_ppt().slides)-1
            ppt_executor.set_current_slide(self.current_page_id)
        else:
            ppt_executor.create_slide()
            self.current_page_id = 0
        self.ppt = ppt_executor.get_ppt()
        self.chat_history = []
        return self.ppt

    def chat(self, user_instruction, ppt_path=None, verbose=False):
        self.prompt = ""
        instruction_list = self.planner(user_instruction)
        reply_list = []

        for instruction in instruction_list:
            if verbose:
                print('Executing instruction: ', instruction)

            selected_apis = self.api_selector(instruction)
            toolkit = api_doc.get_API_toolkit(selected_apis)


            PPT_content = self.content_selector(ppt_path, instruction, self.args, self.ppt)
            
            prompt = prompt_factor.get_instruction_to_API_code_prompt2(
                PPT_content,
                self.chat_history,
                instruction,
                current_page=self.current_page_id,
            )

            self.prompt += prompt + '\n\n'
            if verbose:
                print(f"== Prompt ==\n{prompt}\n\n")

            try:
                # reply = ""
                # reply = openai_api.query_azure_openai(prompt, model="ft:gpt-4o-mini-2024-07-18:personal:edi2:AxTglBO3",id=self.model_id).strip()
                messages = [{"role":"system","content":prompt}]
                tool_calls = openai_api.query_openai(messages, model="gpt-4o-mini", toolkit=toolkit)

                # print('#### Reply:')
                # print(reply)
                # print('#### Parsed:')
                # print(utils.parse_api(reply))
            except Exception as e:
                print("Query Failed!", e)
                tool_calls = []

            if verbose:
                print(f"== Reply from AI ==\n{tool_calls}\n\n")

            self.chat_history += [
                f"¬User¬\n{instruction}",
                # f"¬AI¬:\n{reply}",
            ]
            reply_list.extend(tool_calls)

        return self.prompt, reply_list


    def chat2(self, user_instruction, ppt_path=None, verbose=False):
        self.prompt = ""

        plan_prompt = user_instruction
        plan_toolkit = api_doc.plan_APIs
        plan_tool_calls = openai_api.query_openai(plan_prompt, )

        for plan_tool_call in plan_tool_calls:

            fn_name = plan_tool_call.function.name
            fn_args = json.loads(plan_tool_call.function.arguments)

            if fn_name == "new_slide":
                self.api_executor(["create_slide()"], test=True, args=self.args)
                slide_idx = ppt_executor.get_current_page_id()

            elif fn_name == "modify_slide":
                slide_idx = fn_args["idx"]
                self.api_executor([f"move_to_slide({slide_idx})"], test=True, args=self.args)

            

            edit_prompt = fn_args["instructions"]
            edit_tool_calls = openai_api.query_openai(edit_prompt)

            api_lines = utils.parse_api2(edit_tool_calls)
            self.api_executor(api_lines, test=True, args=self.args)

        reply_list = []
