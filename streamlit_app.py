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
import requests
from langchain import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationSummaryMemory
import streamlit.components.v1 as components

st.set_page_config(
    layout="wide", 
    page_title="EDA AUTOMATION", 
    page_icon="📂"
)
# Function to fetch raw CSS from GitHub
def github_css(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return f"<style>{response.text}</style>"
        else:
            return f"<style>/* Failed to load CSS: {response.status_code} */</style>"
    except Exception as e:
        return f"<style>/* Error loading CSS: {e} */</style>"

# URL to the raw CSS file on GitHub
css_url = "https://raw.githubusercontent.com/jaisai2512/frontend/main/style.css"

# Inject the CSS into the Streamlit app
st.markdown(github_css(css_url), unsafe_allow_html=True)


# Set page layout

# Create a sidebar for file upload
st.sidebar.header("📁 Upload Your File")
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["csv"])

# Display content on the main page
st.title("🤖 EDA Automation")

if uploaded_file is not None:
    st.success("File uploaded successfully!")
    # Display file details
    st.write("### File Details:")
    file_details = {
        "Filename": uploaded_file.name,
        "Filetype": uploaded_file.type,
        "Filesize (KB)": uploaded_file.size / 1024,
    }
    st.json(file_details)

    # Read and display content if it's a text-based file
    try:
        if uploaded_file.type == "text/csv":
            import pandas as pd

            df = pd.read_csv(uploaded_file)
            st.write("### Preview of Uploaded CSV File:")
            st.dataframe(df)
        elif uploaded_file.type == "application/json":
            import json

            content = json.load(uploaded_file)
            st.write("### Content of Uploaded JSON File:")
            st.json(content)
        elif uploaded_file.type == "text/plain":
            content = uploaded_file.read().decode("utf-8")
            st.write("### Content of Uploaded Text File:")
            st.text(content)
        elif "spreadsheet" in uploaded_file.type:
            import pandas as pd

            df = pd.read_excel(uploaded_file)
            st.write("### Preview of Uploaded Excel File:")
            st.dataframe(df)
    except Exception as e:
        st.error(f"An error occurred while reading the file: {e}")
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
    code_generation(univariate_data,'Univariate Analysis',df,summary)

    multivariate_data = mul_goal_generate(summary,FORMAT_INSTRUCTIONS)
    code_generation(multivariate_data,'Multivariate Analysis',df,summary)

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
            }
        ]
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
            },
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
                "content": f"Please solve the following problem step-by-step:\n\nProblem: { human_prompt}\n\nPlease output the code in a step-by-step explanation format. The variable properties are:\n {var_prop}.,USE ONLY DATAFRAME FOR OPERATIONS."
            },
            {
                "role": "assistant",
                "content": ""
            }
        ]
            captured_output = io.StringIO()
            sys.stdout = captured_output  # Redirect stdout
            exec(api(message1), {"df": df})
            sys.stdout = sys.__stdout__  # Restore stdout
            llm_response = captured_output.getvalue().strip()
        
        # Update history
            st.session_state.history.append(Message("human", human_prompt))
            st.session_state.history.append(Message("ai", llm_response))

# Setup session and UI components
    load_css()
    initialize_session_state()

    st.title("Question Bot 🤖")

    chat_placeholder = st.container()
    prompt_placeholder = st.form("chat-form")

    with chat_placeholder:
        chat_container = st.empty()  # Empty container for the chat

    # Function to display chat history
        def display_chat():
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

        display_chat()  # Display chat content in the placeholder

    # Input form for human message
        with prompt_placeholder:
            st.markdown("**Chat**")
            cols = st.columns((6, 1))
            cols[0].text_input("Chat", value="Hello bot", label_visibility="collapsed", key="human_prompt")
            cols[1].form_submit_button("Submit", type="primary", on_click=on_click_callback)

# Update chat interface only, not the entire page
    
else:
    st.info("Please upload a file from the sidebar to view its content.")





















