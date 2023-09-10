import streamlit as st
from Main import AgentHead


if "agent_head" not in st.session_state:
    st.session_state['agent_head'] = AgentHead(n_breakups=5)


##Hiding default streamlit theme components
hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                header {visibility: hidden;}
                </style>
                """
st.markdown(hide_st_style, unsafe_allow_html=True)
st.markdown("""
                <style>
                .block-container {
                padding-top: 0rem;
                margin-top:0rem;
                }
                </style>
                """, unsafe_allow_html=True)


# Create a Streamlit app


##Title and heading
col1, col2 = st.columns(spec=[0.3,0.7])
with col1:
    st.title("TaskBreaker")
with col2:
    style_for_caption = """<style>[data-testid="stCaptionContainer"] {
                            padding-top: 29px;
                            padding-left: 20px;
                            bottom:0;
                            }</style>"""
    st.markdown(style_for_caption, unsafe_allow_html=True)
    st.caption("powered by GPT-3.5")
    
st.write('<i>"Simplify your tasks, uncomplicate your life"</i>',unsafe_allow_html=True)
st.divider()

##Slider for selecting number of steps
st.session_state['n_breakups_slider'] = st.slider(min_value=2, max_value=15, step=1,label="Select the number of steps")


##Input and button functionality
user_input = st.text_input(label="Enter your task", label_visibility="hidden", placeholder="Enter the task here") 
main_button = st.button('⚡Break it down!!', use_container_width=True)

##Button click event, calling LLM and getting response
if main_button:
    if 'task_json' in st.session_state:
        del st.session_state['task_json']
    st.session_state['agent_head'] = AgentHead(n_breakups=st.session_state['n_breakups_slider'])
    st.session_state['task_json'] = st.session_state['agent_head'].get_response(user_input)

##Loading the task list on each re-run
if 'task_json' in st.session_state:
    for n,task in st.session_state['task_json'].items():
        with st.container():
            col1, col2 = st.columns(spec=[0.2,0.7])
            with col1:
                st.checkbox(label='', label_visibility="hidden", key=f"checkbox_{n}")
            with col2:
                st.markdown(task)




