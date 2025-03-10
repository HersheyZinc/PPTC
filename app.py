import streamlit as st
from src.modeling import PPT_assistant
from types import SimpleNamespace
import os

st.set_page_config(layout="wide")
base_ppt_path = "PPTC/PPT_Base_File/Create_new_slides/0_0.pptx"
dst_path = "PPTC/demo.pptx"

if "agent" not in st.session_state:
    args = SimpleNamespace(
        data_path="test",
        dataset="short",
        model_id="None",
        user_path='./PPTC/',
        save_path="test_pptx_data",
        prepare=False,
        eval=False,
        test=False,
        tf=True,
        sess=False,
        resume=False,
        model="gpt-4o-mini",
        planning=False,
        api_selection=False,
        api_topk=10,
        content_selection=False,
        api_lack=False,
        api_update=False,
        second=False,
        robust=False,
        robust_num=0,
        noisy=False
    )
    agent = PPT_assistant(args, "PPTC/slide_previews")
    agent.load_ppt(base_ppt_path)
    agent.save_ppt(dst_path)
    st.session_state["agent"] = agent
    st.session_state["chat_history"] = [{"role":"assistant", "content": "Hello! How can I help you?"}]
    st.session_state["slide_idx"] = 0


col_left, col_right = st.columns([0.6, 0.4])
agent = st.session_state["agent"]
slide_idx = st.session_state["slide_idx"]


with col_right:
    tab_chat, tab_config, tab_log = st.tabs(["Chat", "Settings", "Logs"])

    with tab_config:
        config = st.container(height=600)
        with config:
            if st.button("Reset", type="primary"):
                agent.load_ppt(base_ppt_path)
                slide_idx = 0


    with tab_chat:
        chat = st.container(height=600)
        # 
        with chat:
            for message in st.session_state["chat_history"]:
                # if message["role"] == "system":
                #     continue
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])


        if prompt := st.chat_input("Type instructions to modify the current slide"):
            with chat:
                st.chat_message("user").markdown(prompt)

                _, response = agent.chat(prompt)

                st.session_state["chat_history"].append({"role":"user", "content": prompt})
                st.session_state["chat_history"].append({"role":"assistant", "content": response})
                agent.save_ppt(dst_path)
                slide_idx = agent.current_page_id
                


    # with tab_log:
    #     log = st.container(height=600)
    #     with log:
    #         for msg in agent.log:
    #             for m in msg.split("\n"):
    #                 st.write(m)


with col_left:
    
    st.title("Agent PPT")
    slide_preview_container = st.container()
    slide_selection_container = st.container()
    
    
    with slide_selection_container:
        col1, col2, col3, col4, col5, = st.columns([4,1.3,2,1.3,4])
        
        with col2:
            if st.button("prev", use_container_width=True):
                slide_idx = max(0, slide_idx-1)
        with col4:
            if st.button("next", use_container_width=True):
                slide_idx = min(len(agent.ppt.slides)-1, slide_idx+1)
        with col3:
            st.button(f"Slide {slide_idx+1} of {len(agent.ppt.slides)}", use_container_width=True, disabled=True)
    

    with slide_preview_container:
        st.session_state["slide_idx"] = slide_idx
        slide_preview = st.image(f"{agent.slide_preview_dir}/{slide_idx}.jpg")

