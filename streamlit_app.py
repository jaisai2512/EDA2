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
import sys
import io

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
    o_summary,summary= summary_gen(df)
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


    def on_click_callback():
        with get_openai_callback() as cb:
            human_prompt = st.session_state.human_prompt
            message = [
    {
        "role": "system",
        "content": "You are an expert query interpreter for data analysis. Your job is to assist users by identifying variables involved in their query and classifying the type of output they expect.\n\n### Your Tasks:\n1. **Variable Identification**:\n   - Analyze the user's query.\n   - Identify the variables in the query that match the given list and then output the variables with the name as in the list..\n\n2. **Output Type Classification**:\n   - Determine whether the query's output is:\n     - **Visual**: If the query asks for patterns, trends, comparisons, or insights requiring a graph, chart, or plot.\n     - **Numerical**: If the query asks for specific metrics, values, or summaries.\n\n### Input Format:\nYou will be given:\n- **Query**: A user-generated question or request.\n- **Variables**: A list of possible variables, e.g., `[\"variable_1\", \"variable_2\", ..., \"variable_n\"]`.\n\n### Response Format:\nProvide your response in the following structured JSON format:\n```json\n{\n  \"matched_variables\": [\"variable_1\", \"variable_2\"],\n  \"output_type\": \"visual\" // or \"numerical\"\n}\n```\n\n### Guidelines:\n- Select the variable name from the given list that is explicitly or implicitly mentioned in the user's query, ensuring there are no missing letters in the word.\n- Use context and intent from the query to decide the output type accurately.\n- If no variable matches, leave the \"matched_variables\" array empty."
    },
    {
        "role": "user",
        "content": f"Query:{human_prompt}\nVariables: {df.columns}\n Please output only the json nothing apart from it"
    }]           
            answer = json.loads(api(message))
            var_prop = []
            for i in answer['matched_variables']:
                for j in o_summary:
                    if(j['column'] == i):
                        var_prop.append(j)
                        break
            message1 =[
    {
        "role": "system",
        "content": "You are a problem-solving assistant tasked with generating code in a step-by-step Chain of Thought (CoT) manner. Break down the code generation process into logical steps, ensuring each step is clear and contributes to the solution. Do not jump directly to the solution; instead, explain each step briefly while generating the corresponding code for that step. You will be given a query and the properties of the variables in the DataFrame (such as data type, missing values, etc.). The DataFrame itself is stored as 'df'. You should analyze the structure of the DataFrame based on the variable properties provided and use 'df' accordingly. If data preprocessing is needed, you should perform it as part of the process."
    }
    ,
  {
    "role": "user",
    "content": "Please solve the following problem step-by-step using a DataFrame:\n\nProblem: {Query}\n\nThe variable properties (e.g., data type, missing values, etc.) will be provided."
  },
  {
    "role": "assistant",
    "content": "# Step 1: Access the relevant data column\n# Retrieve the specified column from the DataFrame. Ensure that the data type is appropriate for the required operation (e.g., numeric for summing or squaring).\n# Example:\ncolumn = df['column_name']\n\n# Step 2: Preprocessing (if required)\n# Check for missing values in the column. If there are missing values, choose an appropriate imputation strategy (e.g., filling with mean, median, or mode).\n# Handle any missing values using the chosen method.\n# Example:\ncolumn.fillna(column.mean(), inplace=True)  # Filling missing values with mean\n\n# Step 3: Filter data based on conditions\n# Apply any necessary filters to the data (e.g., selecting even numbers from the column using the modulus operator % 2 == 0).\n# Example:\neven_numbers = column[column % 2 == 0]\n\n# Step 4: Data transformation (if needed)\n# Apply the necessary transformation to the filtered data (e.g., squaring the numbers, applying a logarithmic transformation, etc.).\n# Example:\nsquared_numbers = even_numbers ** 2\n\n# Step 5: Perform the required operation\n# Execute the main operation (e.g., summing the squared numbers, counting occurrences, or computing the mean).\n# Example:\nsum_of_squares = squared_numbers.sum()\n\n# Step 6: Edge case handling\n# Check for edge cases, such as empty columns, no matching data (e.g., no even numbers), or columns with all missing values.\n# Return an appropriate result for these edge cases (e.g., return 0 if no matching data).\n# Example:\nif len(even_numbers) == 0:\n    sum_of_squares = 0\n\n# Step 7: Output the result\n# Provide the final result after completing all operations.\n# Example:\nprint(sum_of_squares)"
  },
  {
    "role": "user",
    "content": f"Please solve the following problem step-by-step:\n\nProblem: { human_prompt}\n\nPlease output the code in a step-by-step explanation format. The variable properties are:\n {var_prop}."
  },
  {
    "role": "assistant",
    "content": ""
  }
]
            #llm_response =exec(api(message1), {"df": df})
            captured_output = io.StringIO()
            sys.stdout = captured_output  # Redirect stdout

            exec(api(message1), {"df": df})

            sys.stdout = sys.__stdout__  # Restore stdout
            llm_response = captured_output.getvalue().strip()
            st.session_state.history.append(
            Message("human", human_prompt)
        )
            st.session_state.history.append(
            Message("ai", llm_response)
        )
            

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
    Used  tokens \n
    Debug Langchain conversation: 
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






















