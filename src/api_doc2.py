class API(object):
    def __init__(self, name, description, required=[], parameters={}):
        self.name = name
        self.parameters = parameters
        self.description = description
        self.required = required
    
    def __api__(self):
        api_info = {'type': 'function','function': {'name': self.name,'description': self.description}}
        if self.parameters:
            api_info["function"]["parameters"] = {"type":"object", "properties":self.parameters}
        if self.required:
            api_info["function"]["required"] = self.required

        return api_info

# slide
slide_APIs = [
    API(name="create_slide", description="Creates a new slide."),
    API(name="move_to_previous_slide", description="Moves to the previous slide."),
    API(name="move_to_next_slide", description="Move to next slide."),
    API(name="move_to_slide", description="Moves to the given slide id.", required=['slide_id'],
        parameters={'slide_id': {'description':'The ID of the slide to move to.'}, 'type':'integer'}),
    API(name="set_background_color", parameters="(color)", description="Sets the background color of the slide.", required=["color"],
        parameters={'color':{'description':'The color name to set as a string, such as red, purple.', 'type':'string'}})
]

# choose
choose_APIs = [
    API(name="choose_title", description="Selects the title on the slide."),
    API(name="choose_content", description="Select the content on the slide."),  
    API(name="choose_textbox", description="Selects the textbox element on the slide.", required=['idx'],
        parameters={'idx': {'description': 'The index of textbox.', 'type': 'integer'}}),
    API(name="choose_picture", description="Selects the picture element on the slide.", required=['idx'],
        parameters={'idx': {'description': 'The index of picture.', 'type': 'integer'}}),
    API(name="choose_shape", description="Selects the auto_shape on the slide.", required=['idx'],
        parameters={'idx': {'description': 'The index of shape.', 'type': 'integer'}}),
    API(name="choose_table", description="Selects the table element on the slide."),
    API(name="choose_table_cell", description="Selects a specific cell in the table element. You should first call choose_table().", required=['row_id', 'column_id'],
        parameters={'row_id': {'description': 'The selected cell row.', 'type': 'integer'}, 'column_id': {'description': 'The selected cell column.', 'type': 'integer'}}),
]

# basic
basic_APIs = [
    API(name="set_width", description="Sets the width of the selected object.", required=['width'],
        parameters={'width': {'description': 'The width of an object in centimeters as float.', 'type': 'number'}}),
    API(name="set_height", description="Sets the height of the selected object.", required=['height'],
        parameters={'height': {'description': 'The height of an object in centimeters as float.', 'type': 'number'}}),
    API(name="rotate_element", description="Rotates the selected object clockwise.", required=['angle'],
        parameters={'angle': {'description': 'The angle to rotate in degrees', 'type': 'number'}}),
    API(name="set_fill_color", description="Sets the fill color of the selected object.", required=['color'],
        parameters={'color': {'description': 'The color name to set as a string, such as red, purple.', 'type': 'string'}}),
    API(name="set_left", description="Sets the x (horizontal) position of the selected object.", required=['left'],
        parameters={'left': {'description': 'The distance between the left side of the slide and the left side of the object in centimeters.', 'type': 'number'}}),
    API(name="set_top", description="Sets the y (vertical) position of the selected object.", required=['top'],
        parameters={'top': {'description': 'The distance between the top of the slide and the top of the object in centimeters.', 'type': 'number'}}),
    API(name="align_slide_top", description="Moves the selected object to the top side of the slide."),
    API(name="align_slide_bottom", description="Moves the selected object to the bottom side of the slide."),
    API(name="align_slide_left", description="Moves the selected object to the left side of the slide."),
    API(name="align_slide_right", description="Moves the selected object to the right side of the slide."),
    API(name="align_slide_center", description="Moves the selected object to the center of the slide."),
]

# text
text_APIs = [
    API(name="insert_text", description="Inserts text into the selected text frame (textbox, title, content, table).", required=['text'],
        parameters={'text': {'description': 'Exact string to be inserted.', 'type': 'string'}}),
    API(name="insert_bullet_point", description="Inserts a bullet point into the selected text frame (textbox, title, content, table).", required=['text'],
        parameters={'text': {'description': 'Exact string to be inserted.', 'type': 'string'}}),
    # API(name="insert_note", description="Inserts a note onto the slide.", required=['text'],
    #     parameters={'text': {'description': 'Exact string to be inserted.', 'type': 'string'}}),
    API(name="insert_textbox", description="Inserts an empty textbox into the slide and selects it. You should use insert_text() after calling this function."),
    API(name="delete_text", description="Deletes the text content of the selected object."),
    API(name="set_font_size", description="Sets font size of the selected text.", required=['font_size'],
        parameters={'font_size': {'description': 'Font size of text.', 'type': 'integer'}}),
    API(name="set_font_color", description="Sets font color of the selected text.", required=['color'],
        parameters={'color': {'description': 'The color name to set as a string, such as red, purple.', 'type': 'string'}}),
    API(name="set_font_bold", description="Sets the selected text to be bold."),
    API(name="set_font_italic", description="Sets the selected text to be italic."),
    API(name="set_font_underline", description="Sets the selected text to be underlined."),
    API(name="set_font_style", description="Sets font style of the selected text.", required=['font_name'],
        parameters={'font_name': {'description': 'The name of the font style.', 'type': 'string'}}),
    API(name="set_line_space", description="Sets the line spacing of the selected text.", required=['line_space_level'],
        parameters={'line_space_level': {'description': 'Spacing between each line of text, default 0.', 'type': 'number'}}),
    API(name="text_align_left", description="This API aligns the text to left."), 
    API(name="text_align_center", description="This API aligns the text to center."), 
    API(name="text_align_right", description="This API aligns the text to right."),
]

# picture
picture_APIs = [
    API(name="insert_picture", description="Inserts a picture into the slide", required=['picture_name'],
        parameters={'picture_name': {'description': 'A description of the picture.', 'type': 'string'}}),
]

# shape
shape_APIs = [
    API(name="insert_rectangle", description="Inserts a rectangle or square shape onto the slide."),
    API(name="insert_right_arrow", description="Inserts an arrow shape onto the slide."),
    API(name="insert_rounded_rectangle", description="Inserts a rounded rectangle shape onto the slide."),
    API(name="insert_triangle", description="Inserts a triangle shape onto the slide."),
    API(name="insert_callout", description="Inserts a callout shape onto the slide."),
    API(name="insert_cloud", description="Inserts a cloud shape onto the slide."),
    API(name="insert_star", description="Inserts a star shape onto the slide."),
    API(name="insert_circle", description="Inserts a circle or oval shape onto the slide."),
]

# table
table_APIs = [
    API(name="insert_table", description="Inserts a table of row_num rows and col_num columns onto the current slide.", required=['row_num', 'col_num'],
        parameters={'row_num': {'description': 'Number of rows in the table', 'type': 'integer'}, 'col_num': {'description': 'Number of columns in the table', 'type': 'integer'}}),
    API(name="insert_table_row", description="Inserts a row of data into the table.", required=['row_data'],
        parameters={'row_data': {'description': 'An array of strings corresponding to the text in each row cell.', 'type': 'array', 'items': {'type': 'string'}}}),
]

# chart
chart_APIs = [
    API(name="insert_line_chart", description="Inserts a line chart onto the slide", required=['data', 'series'],
        parameters={
            'data': {'description': 'An array of numbers.', 'type': 'array', 'items': {'type': 'number'}}, 
            'series': {'description': 'An array of strings corresponding to each number in data.', 'type': 'array', 'items': {'type': 'string'}}}
        ),
    API(name="insert_bar_chart", description="Inserts a bar chart onto the slide", required=['data', 'series'],
        parameters={
            'data': {'description': 'An array of numbers.', 'type': 'array', 'items': {'type': 'number'}}, 
            'series': {'description': 'An array of strings corresponding to each number in data.', 'type': 'array', 'items': {'type': 'string'}}}
        ),
    API(name="insert_pie_chart", description="Inserts a pie chart onto the slide", required=['data', 'series'],
        parameters={
            'data': {'description': 'An array of numbers.', 'type': 'array', 'items': {'type': 'number'}}, 
            'series': {'description': 'An array of strings corresponding to each number in data.', 'type': 'array', 'items': {'type': 'string'}}}
        ),
    API(name="set_chart_title", description="Sets the title of the selected chart", required=['title'],
        parameters={'title': {'description': 'Title of chart', 'type': 'string'}}),
]

lack_APIs = [
    API(name="seek_assistance", description="This API requests human help when the computer is unsure about the result or lacks the necessary API to fulfill the user's instruction."),
]

import random
random.seed(42)
def random_permutation(lst):
    shuffled = lst.copy()
    random.shuffle(shuffled)
    return shuffled

def get_all_APIs(args):
    all_apis =  slide_APIs + choose_APIs + basic_APIs + text_APIs + picture_APIs+ shape_APIs + table_APIs + chart_APIs 
    if args.api_update:
        all_apis += update_APIs
        all_apis = random_permutation(all_apis)
    if args.api_lack:
        all_apis = [x for x in all_apis if x.name in original_apis]
        all_apis += lack_APIs
    return all_apis



def get_API_name(apis):
    return [api.name + api.parameters for api in apis]

def get_API_desc(apis):
    return [api.api_desc for api in apis]

def get_must_APIs(args):
    if args.dataset == 'long':
        must_APIs = [slide_APIs[3], text_APIs[0], text_APIs[4], choose_APIs[2]]
    else:
        must_APIs = [slide_APIs[3], text_APIs[0], text_APIs[4], choose_APIs[1], basic_APIs[4], basic_APIs[5]]
    if args.api_lack:
        must_APIs += lack_APIs
    return must_APIs

def api_lack_mask(apis):
    ans = []
    for api in apis:
        if not api.split('(')[0] in original_apis:
            ans.append("seek_assistance()")
        else:
            ans.append(api)
    return ans

# update     

update_APIs = [
    API(name="insert_icon", parameters="(icon_id)", description="This API inserts an icon onto the slide.",parameter_description="It takes one parameter 'icon_id', the ID or name of the icon to insert as a string.", api_desc="icon"),
    API(name="insert_3d_model", parameters="(model_id)", description="This API inserts a 3D model onto the slide.",parameter_description="It takes one parameter 'model_id', the ID or name of the 3D model to insert as a string.", api_desc="3D model"),
    API(name="insert_smart_art_list", parameters="(smart_art_type_id)", description="This API inserts a SmartArt list onto the slide.",parameter_description="It takes one parameter 'smart_art_type_id', the ID or name of the SmartArt list type to insert as a string.", api_desc="SmartArt list"),
    API(name="insert_smart_art_process", parameters="(smart_art_type_id)", description="This API inserts a SmartArt process diagram onto the slide.",parameter_description="It takes one parameter 'smart_art_type_id', the ID or name of the SmartArt process type to insert as a string.", api_desc="SmartArt process"),
    API(name="insert_smart_art_cycle", parameters="(smart_art_type_id)", description="This API inserts a SmartArt cycle diagram onto the slide.",parameter_description="It takes one parameter 'smart_art_type_id', the ID or name of the SmartArt cycle type to insert as a string.", api_desc="SmartArt cycle"),
    API(name="insert_smart_art_pyramid", parameters="(smart_art_type_id)", description="This API inserts a SmartArt pyramid diagram onto the slide.",parameter_description="It takes one parameter 'smart_art_type_id', the ID or name of the SmartArt pyramid type to insert as a string.", api_desc="SmartArt pyramid"),
    API(name="insert_smart_art_relationship", parameters="(smart_art_type_id)", description="This API inserts a SmartArt relationship diagram onto the slide.",parameter_description="It takes one parameter 'smart_art_type_id', the ID or name of the SmartArt relationship type to insert as a string.", api_desc="SmartArt relationship"),
    API(name="insert_link", parameters="(link)", description="This API inserts a hyperlink onto the slide.",parameter_description="It takes one parameter 'link', the URL or path of the hyperlink as a string.", api_desc="hyperlink"),
    API(name="insert_comment", parameters="(comment)", description="This API inserts a comment onto the slide.",parameter_description="It takes one parameter 'comment', the text of the comment to insert as a string.", api_desc="comment"),
    API(name="insert_symbol", parameters="(symbol)", description="This API inserts a symbol onto the slide.",parameter_description="It takes one parameter 'symbol', the symbol character to insert as a string.", api_desc="symbol"),
    API(name="insert_equation", parameters="(equation)", description="This API inserts an equation onto the slide.",parameter_description="It takes one parameter 'equation', the mathematical equation to insert as a string.", api_desc="equation"),
    API(name="insert_audio", parameters="(url)", description="This API inserts an audio file onto the slide.",parameter_description="It takes one parameter 'url', the URL or path of the audio file to insert as a string.", api_desc="audio"),
    API(name="insert_video", parameters="(url)", description="This API inserts a video onto the slide.",parameter_description="It takes one parameter 'url', the URL or path of the video file to insert as a string.", api_desc="video"),
    API(name="insert_transition", parameters="(transition_id)", description="This API sets the slide transition effect for the current slide.",parameter_description="It takes one parameter 'transition_id', the ID or name of the transition effect to set as a string.", api_desc="slide transition"),
    API(name="set_transition_duration", parameters="(time)", description="This API sets the duration of the slide transition effect.",parameter_description="It takes one parameter 'time', the duration of the transition effect in seconds as an integer or float.", api_desc="transition duration"),
    API(name="set_transition_sound", parameters="(url)", description="This API sets the sound for the slide transition effect.",parameter_description="It takes one parameter 'url', the URL or path of the sound file to set for the transition as a string.", api_desc="transition sound"),
    API(name="set_transition_after_time", parameters="(time)", description="This API sets the delay time before the slide transition starts.",parameter_description="It takes one parameter 'time', the delay time in seconds as an integer or float.", api_desc="transition delay"),
    API(name="increase_transition_after_time", parameters="()", description="This API increases the delay time before the slide transition starts.", api_desc="increase transition delay"),
    API(name="decrease_transition_after_time", parameters="()", description="This API decreases the delay time before the slide transition starts.", api_desc="decrease transition delay"),
    API(name="increase_transition_duration", parameters="()", description="This API increases the duration of the slide transition effect.", api_desc="increase transition duration"),
    API(name="decrease_transition_duration", parameters="()", description="This API decreases the duration of the slide transition effect.", api_desc="decrease transition duration"),
    API(name="insert_entrance_animation", parameters="(animation_id)", description="This API adds an entrance animation to the selected object or text on the slide.",parameter_description="It takes one parameter 'animation_id', the ID or name of the entrance animation to apply as a string.", api_desc="entrance animation"),
    API(name="insert_emphasis_animation", parameters="(animation_id)", description="This API adds an emphasis animation to the selected object or text on the slide.",parameter_description="It takes one parameter 'animation_id', the ID or name of the emphasis animation to apply as a string.", api_desc="emphasis animation"),
    API(name="insert_exit_animation", parameters="(animation_id)", description="This API adds an exit animation to the selected object or text on the slide.",parameter_description="It takes one parameter 'animation_id', the ID or name of the exit animation to apply as a string.", api_desc="exit animation"),
    API(name="insert_path_animation", parameters="(animation_id)", description="This API adds a motion path animation to the selected object on the slide.",parameter_description="It takes one parameter 'animation_id', the ID or name of the motion path animation to apply as a string.", api_desc="motion path animation"),
    API(name="delete_animation", parameters="()", description="This API removes any animation applied to the selected object or text on the slide.", api_desc="remove animation"),
    API(name="set_animation_start_time", parameters="(time)", description="This API sets the start time of the animation for the selected object or text on the slide.",parameter_description="It takes one parameter 'time', the start time of the animation in seconds as an integer or float.", api_desc="animation start time"),
    API(name="set_animation_duration", parameters="(time)", description="This API sets the duration of the animation for the selected object or text on the slide.",parameter_description="It takes one parameter 'time', the duration of the animation in seconds as an integer or float.", api_desc="animation duration"),
    API(name="start_record", parameters="()", description="This API starts recording the slide show.", api_desc="start recording slide show"),
    API(name="end_record", parameters="()", description="This API stops recording the slide show.", api_desc="stop recording slide show"),
    API(name="get_screenshot", parameters="()", description="This API captures a screenshot of the current slide.", api_desc="capture slide screenshot"),
    API(name="set_font_crossline", parameters="()", description="This API adds a crossline to the selected font in the text on the slide.", api_desc="add font crossline"),
    API(name="delete_comment", parameters="(comment_id)", description="This API deletes a specific comment from the slide.",parameter_description="It takes one parameter 'comment_id', the ID or name of the comment to delete as a string.", api_desc="delete comment"),
    API(name="play_from_start", parameters="()", description="This API starts playing the slide show from the beginning.", api_desc="play slide show from start"),
    API(name="play_from_current_slide", parameters="()", description="This API starts playing the slide show from the current slide.", api_desc="play slide show from current slide"),
    API(name="play_from_slide", parameters="(slide_id)", description="This API starts playing the slide show from a specific slide.",parameter_description="It takes one parameter 'slide_id', the ID or number of the slide to start playing from as a string or integer.", api_desc="play slide show from specific slide"),
    API(name="insert_hierarchy_chart", parameters="(data, series)", description="This API inserts a hierarchy chart onto the slide.",parameter_description="It takes two parameters, 'data' as a list of numbers and 'series' as a list of strings.", api_desc="hierarchy chart"),
    API(name="insert_statistical_chart", parameters="(data, series)", description="This API inserts a statistical chart onto the slide.",parameter_description="It takes two parameters, 'data' as a list of numbers and 'series' as a list of strings.", api_desc="statistical chart"),
    API(name="insert_scatter_chart", parameters="(data, series)", description="This API inserts a scatter chart onto the slide.",parameter_description="It takes two parameters, 'data' as a list of numbers and 'series' as a list of strings.", api_desc="scatter chart"),
    API(name="insert_combo_chart", parameters="(data, series)", description="This API inserts a combo chart onto the slide.",parameter_description="It takes two parameters, 'data' as a list of numbers and 'series' as a list of strings.", api_desc="combo chart"),
    API(name="insert_map", parameters="()", description="This API inserts a map shape onto the slide.", api_desc="map"),
    API(name="insert_left_arrow", parameters="()", description="This API inserts a left arrow shape onto the slide.", api_desc="left arrow"),
    API(name="insert_down_arrow", parameters="()", description="This API inserts a down arrow shape onto the slide.", api_desc="down arrow"),
    API(name="insert_up_arrow", parameters="()", description="This API inserts an up arrow shape onto the slide.", api_desc="up arrow"),
    API(name="insert_pentagon", parameters="()", description="This API inserts a pentagon shape onto the slide.", api_desc="pentagon"),
    API(name="insert_trapezoid", parameters="()", description="This API inserts a trapezoid shape onto the slide.", api_desc="trapezoid"),
    API(name="insert_smile_face", parameters="()", description="This API inserts a smiley face shape onto the slide.", api_desc="smiley face"),
    API(name="insert_heart_shape", parameters="()", description="This API inserts a heart shape onto the slide.", api_desc="heart shape"),
    API(name="insert_lightening_shape", parameters="()", description="This API inserts a lightning shape onto the slide.", api_desc="lightning shape"),
    API(name="insert_stop_shape", parameters="()", description="This API inserts a stop sign shape onto the slide.", api_desc="stop sign shape"),
#
    API(name="insert_flow_chart", parameters="(flow_chart_type)", description="This API inserts a flow chart shape onto the slide.", parameter_description="It takes one parameter 'flow_chart_type', the type of flow chart shape to insert as a string.", api_desc="flow chart"),
    API(name="insert_moon", parameters="()", description="This API inserts a moon shape onto the slide.", api_desc="moon shape"),
    API(name="insert_sun", parameters="()", description="This API inserts a sun shape onto the slide.", api_desc="sun shape"),
    API(name="insert_ellipse", parameters="()", description="This API inserts an ellipse shape onto the slide.", api_desc="ellipse shape"),
    API(name="group_shapes", parameters="(shape_ids)", description="This API groups multiple shapes on the slide.", parameter_description="It takes one parameter 'shape_ids', a list containing the IDs or names of the shapes to group.", api_desc="group shapes"),
    API(name="ungroup_shapes", parameters="(group_id)", description="This API ungroups a set of grouped shapes on the slide.", parameter_description="It takes one parameter 'group_id', the ID or name of the shape group to ungroup.", api_desc="ungroup shapes"),
    API(name="set_border_color", parameters="(shape_id, color)", description="This API sets the border color of a specific shape.", parameter_description="It takes two parameters, 'shape_id' as the ID or name of the shape and 'color' for the border color.", api_desc="set border color"),
    API(name="lock_shape", parameters="(shape_id)", description="This API locks a specific shape, preventing it from being edited or moved.", parameter_description="It takes one parameter 'shape_id', the ID or name of the shape to lock.", api_desc="lock shape"),
    API(name="unlock_shape", parameters="(shape_id)", description="This API unlocks a specific shape, allowing it to be edited or moved.", parameter_description="It takes one parameter 'shape_id', the ID or name of the shape to unlock.", api_desc="unlock shape"),
    API(name="set_shape_opacity", parameters="(shape_id, opacity)", description="This API sets the opacity of a specific shape.", parameter_description="It takes two parameters, 'shape_id' as the ID or name of the shape and 'opacity' as a value between 0 (transparent) to 1 (opaque).", api_desc="set shape opacity"),
    API(name="send_to_back", parameters="(shape_id)", description="This API sends a specific shape to the back of the slide.", parameter_description="It takes one parameter 'shape_id', the ID or name of the shape to send to the back.", api_desc="send shape to back"),
    API(name="bring_to_front", parameters="(shape_id)", description="This API brings a specific shape to the front of the slide.", parameter_description="It takes one parameter 'shape_id', the ID or name of the shape to bring to the front.", api_desc="bring shape to front"),
    API(name="distribute_horizontally", parameters="(shape_ids)", description="This API distributes shapes equally in horizontal spacing.", parameter_description="It takes one parameter 'shape_ids', a list containing the IDs or names of the shapes to distribute.", api_desc="distribute shapes horizontally"),
    API(name="distribute_vertically", parameters="(shape_ids)", description="This API distributes shapes equally in vertical spacing.", parameter_description="It takes one parameter 'shape_ids', a list containing the IDs or names of the shapes to distribute.", api_desc="distribute shapes vertically"),
    API(name="export_slide_as_image", parameters="(file_name, format)", description="This API exports the current slide as an image in the specified format.", parameter_description="It takes two parameters, 'file_name' as the name of the file to save the image to and 'format' as the desired image format (e.g., 'JPEG', 'PNG').", api_desc="export slide as image"),
    API(name="set_shape_gradient", parameters="(shape_id, gradient_type, colors)", description="This API sets a gradient fill on a shape.", parameter_description="Takes 'shape_id' as the shape's ID or name, 'gradient_type' as the gradient's type (linear, radial, etc.), and 'colors' as a list of colors for the gradient.", api_desc="set shape gradient"),
    API(name="merge_cells", parameters="(table_id, start_row, start_column, end_row, end_column)", description="Merges cells in a table.", parameter_description="Parameters specify the table and the range of cells to merge.", api_desc="merge table cells"),
    API(name="split_cell", parameters="(table_id, row, column)", description="Splits a previously merged cell.", parameter_description="Takes 'table_id' for the table's ID or name and 'row' and 'column' for cell location.", api_desc="split table cell"),
    API(name="set_table_style", parameters="(table_id, style)", description="Applies a style to a table.", parameter_description="Takes 'table_id' for the table's ID or name and 'style' for the style name.", api_desc="set table style"),
    API(name="insert_hyperlink", parameters="(text, link)", description="Inserts a hyperlink onto the slide.", parameter_description="Takes 'text' as the visible text and 'link' as the actual hyperlink.", api_desc="insert hyperlink"),
    API(name="remove_animation", parameters="(shape_id)", description="Removes any animation from a shape.", parameter_description="Takes 'shape_id' for the shape's ID or name.", api_desc="remove animation"),
    API(name="remove_slide_transition", parameters="()", description="Removes any transition effect from the slide.", api_desc="remove slide transition"),
    API(name="play_media", parameters="(media_id)", description="Plays an audio or video clip on the slide.", parameter_description="Takes 'media_id' for the audio or video clip's ID or name.", api_desc="play media"),
    API(name="pause_media", parameters="(media_id)", description="Pauses an audio or video clip on the slide.", parameter_description="Takes 'media_id' for the audio or video clip's ID or name.", api_desc="pause media"),
    API(name="stop_media", parameters="(media_id)", description="Stops an audio or video clip on the slide.", parameter_description="Takes 'media_id' for the audio or video clip's ID or name.", api_desc="stop media"),
    API(name="set_media_volume", parameters="(media_id, volume)", description="Sets the volume for an audio or video clip.", parameter_description="Specifies the media and desired volume (0-100).", api_desc="set media volume"),
    API(name="mute_media", parameters="(media_id)", description="Mutes an audio or video clip.", parameter_description="Takes 'media_id' for the audio or video clip's ID or name.", api_desc="mute media"),
    API(name="unmute_media", parameters="(media_id)", description="Unmutes an audio or video clip.", parameter_description="Takes 'media_id' for the audio or video clip's ID or name.", api_desc="unmute media"),
    API(name="trim_media", parameters="(media_id, start_time, end_time)", description="Trims an audio or video clip's playback range.", parameter_description="Specifies the media and desired start and end times for playback.", api_desc="trim media"),
    API(name="set_slide_master", parameters="(master_id)", description="Applies a slide master layout to the current slide.", parameter_description="Takes 'master_id' as the ID or name of the slide master.", api_desc="set slide master"),
    API(name="duplicate_slide", parameters="()", description="Duplicates the current slide.", api_desc="duplicate slide"),
    API(name="hide_slide", parameters="()", description="Hides the current slide from the slideshow view.", api_desc="hide slide"),
    API(name="unhide_slide", parameters="()", description="Unhides the current slide for the slideshow view.", api_desc="unhide slide"),
    API(name="set_slide_orientation", parameters="(orientation)", description="Sets the slide orientation.", parameter_description="Takes 'orientation' as either 'portrait' or 'landscape'.", api_desc="set slide orientation"),
    API(name="insert_image_gallery", parameters="(image_paths)", description="Inserts a gallery of images onto the slide.", parameter_description="Takes 'image_paths' as a list of paths to the images.", api_desc="insert image gallery"),
    API(name="flip_shape", parameters="(shape_id, direction)", description="Flips a shape horizontally or vertically.", parameter_description="Takes 'shape_id' for the shape's ID or name and 'direction' as either 'horizontal' or 'vertical'.", api_desc="flip shape"),
    API(name="set_slide_looping", parameters="(loop_count)", description="Sets the number of times a slide should loop.", parameter_description="Takes 'loop_count' as the number of loops (0 for infinite).", api_desc="set slide looping"),
    API(name="insert_slide_number", parameters="(position)", description="Inserts slide number at a specified position.", parameter_description="Takes 'position' as the location on the slide (e.g., 'bottom_right').", api_desc="insert slide number"),
    API(name="insert_date_time", parameters="(format, position)", description="Inserts date and time on the slide.", parameter_description="Takes 'format' for date/time format and 'position' as the location.", api_desc="insert date and time"),
    API(name="embed_fonts", parameters="()", description="Embeds the fonts used in the presentation.", api_desc="embed fonts"),
    API(name="optimize_media", parameters="(compression_level)", description="Optimizes embedded media to reduce file size.", parameter_description="Takes 'compression_level' as the desired level of compression.", api_desc="optimize media"),
    API(name="enable_slide_grid", parameters="(grid_spacing)", description="Enables a grid overlay on the slide.", parameter_description="Takes 'grid_spacing' as the distance between grid lines.", api_desc="enable slide grid"),
    API(name="disable_slide_grid", parameters="()", description="Disables the grid overlay on the slide.", api_desc="disable slide grid"),
    API(name="set_slide_grid_color", parameters="(color)", description="Sets the color of the grid overlay on the slide.", parameter_description="Takes 'color' as the desired color value.", api_desc="set slide grid color"),
    API(name="set_text_wrap", parameters="(shape_id, wrap_type)", description="Sets how text wraps inside a shape.", parameter_description="Takes 'shape_id' for the shape's ID or name and 'wrap_type' as the desired wrap setting (e.g., 'square', 'tight').", api_desc="set text wrap"),
    API(name="lock_aspect_ratio", parameters="(shape_id)", description="Locks the aspect ratio of a shape.", parameter_description="Takes 'shape_id' as the shape's ID or name.", api_desc="lock shape aspect ratio"),
    API(name="unlock_aspect_ratio", parameters="(shape_id)", description="Unlocks the aspect ratio of a shape.", parameter_description="Takes 'shape_id' as the shape's ID or name.", api_desc="unlock shape aspect ratio")
]

update_apis = [x.name for x in update_APIs]

original_apis = [
    "move_to_slide",
    "create_slide",
    "choose_title",
    "choose_content",
    "choose_picture",
    "choose_shape",
    "choose_textbox",
    "set_background_color",
    "insert_text",
    "insert_picture",
    "insert_rectangle",
    "insert_right_arrow",
    "insert_line_chart",
    "insert_bar_chart",
    "insert_pie_chart",
    "choose_table",
    "choose_table_cell",
    "insert_table",
    "set_font_color",
    "set_font_size",
    "set_font_bold",
    "set_height",
    "set_width",
    "set_left",
    "set_top",
]

# api_selector
# - get_all_APIs
# - get_selected_APIs
# api_executor

# api update:


# api lack:
