import Rules
from API import api
import streamlit as st 
import pandas as pd
import json
from execute import execute_code_safely
import seaborn as sns
import matplotlib.pyplot as plt
import io
import openai
from Summary import summary_gen
from tabs import Tabs
from PDF import pdf_parser
import os
from Univariate_Analysis import goal_generate
from Multivariate_Analysis import mul_goal_generate
from Code_holder import code_generation
from dataclasses import dataclass
from typing import Literal
import streamlit as st

from langchain import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory
import streamlit.components.v1 as components

# Title of the Streamlit app
st.title("EDA Report Generator")

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV or pdf file",type=["csv", "pdf"])

# Check if a file has been uploaded
if uploaded_file is not None:
    if uploaded_file.name.endswith(".pdf"):
        pdf_parser(uploaded_file)
    elif not uploaded_file.name.endswith((".csv",".pdf")):
        st.write("Wrong file uploaded.Please upload a csv file")
    df = pd.read_csv(uploaded_file)
    # Display the content of the CSV file
    st.write("Summary of the CSV file:")
    var_dict = {'df': df}
    summary= summary_gen(df)
    FORMAT_INSTRUCTIONS = """
The output must follow the exact JSON format below:
[
    {{
        "question": "...",
        "visualization": "...",
        "reason": "..."
    }},
    ...
]

Ensure that the JSON format is strictly followed with no additional text outside of the JSON structure.
"""
    
    univariate_data = goal_generate(summary,FORMAT_INSTRUCTIONS)
    #st.write(univariate_data)
    #code_generation(univariate_data,'Univariate Analysis',df,summary)

    multivariate_data = mul_goal_generate(summary,FORMAT_INSTRUCTIONS)
    #code_generation(multivariate_data,'Multivariate Analysis',df,summary)
    prompt =  [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, can you summarize our conversation?"},
]
    @dataclass
    class Message:
        """Class for keeping track of a chat message."""
        origin: Literal["human", "ai"]
        message: str

    def load_css():
        with open("static/styles.css", "r") as f:
            css = f"<style>{f.read()}</style>"
            st.markdown(css, unsafe_allow_html=True)

    def initialize_session_state():
        if "history" not in st.session_state:
            st.session_state.history = []
        if "token_count" not in st.session_state:
            st.session_state.token_count = 0
        if "conversation" not in st.session_state:
            client = openai.OpenAI(
        api_key="3625d6ad-e51e-4d62-97df-149d8de8ffe9",
        base_url="https://api.sambanova.ai/v1",
    )

            response = client.chat.completions.create(
        model='Meta-Llama-3.1-8B-Instruct',
                messages=prompt,
        temperature=0,
        top_p=0.1
    )
           

# Initialize the Conversation Chain
            llm = response.choices[0].message.content
            st.session_state.conversation = ConversationChain(
            llm=llm,
            memory=ConversationSummaryMemory(llm=llm),
        )

    def on_click_callback():
        with get_openai_callback() as cb:
            human_prompt = st.session_state.human_prompt
            llm_response = st.session_state.conversation.run(
            human_prompt
        )
            st.session_state.history.append(
            Message("human", human_prompt)
        )
            st.session_state.history.append(
            Message("ai", llm_response)
        )
            st.session_state.token_count += cb.total_tokens

    load_css()
    initialize_session_state()

    st.title("Hello Custom CSS Chatbot 🤖")

    chat_placeholder = st.container()
    prompt_placeholder = st.form("chat-form")
    credit_card_placeholder = st.empty()

    with chat_placeholder:
        for chat in st.session_state.history:
            div = f"""
    <div class="chat-row 
    {'' if chat.origin == 'ai' else 'row-reverse'}">
    <img class="chat-icon" src="app/static/{
        'ai_icon.png' if chat.origin == 'ai' 
                      else 'user_icon.png'}"
         width=32 height=32>
    <div class="chat-bubble
    {'ai-bubble' if chat.origin == 'ai' else 'human-bubble'}">
        &#8203;{chat.message}
    </div>
</div>
        """
            st.markdown(div, unsafe_allow_html=True)
    
        for _ in range(3):
            st.markdown("")

    with prompt_placeholder:
        st.markdown("**Chat**")
        cols = st.columns((6, 1))
        cols[0].text_input(
            "Chat",
            value="Hello bot",
            label_visibility="collapsed",
        key="human_prompt",
    )
        cols[1].form_submit_button(
        "Submit", 
        type="primary", 
        on_click=on_click_callback, 
    )

    credit_card_placeholder.caption(f"""
    Used {st.session_state.token_count} tokens \n
    Debug Langchain conversation: 
{st.session_state.conversation.memory.buffer}
""")

    components.html("""
<script>
const streamlitDoc = window.parent.document;

const buttons = Array.from(
    streamlitDoc.querySelectorAll('.stButton > button')
);
const submitButton = buttons.find(
    el => el.innerText === 'Submit'
);

streamlitDoc.addEventListener('keydown', function(e) {
    switch (e.key) {
        case 'Enter':
            submitButton.click();
            break;
    }
});
</script>
""", 
    height=0,
    width=0,
)
    
else:
    st.write("Please upload a CSV or PDF file to proceed.")






















