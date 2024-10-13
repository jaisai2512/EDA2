import Rules
from API import api
import streamlit as st
import pandas as pd
import json
from execute import execute_code_safely
import seaborn as sns
import matplotlib.pyplot as plt
import io
from Summary import summary_gen
from tabs import Tabs
from PDF import pdf_parser
import os

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
    summary = summary_gen(df)
    #st.write(summary)
    SYSTEM_INSTRUCTIONS = """
You are an experienced data analyst who generates a specified number of insightful GOALS based on a univariate analysis of the dataset summary provided and a specified persona. The VISUALIZATIONS YOU RECOMMEND MUST FOLLOW VISUALIZATION BEST PRACTICES (e.g., must use bar charts instead of pie charts for comparing quantities) AND BE MEANINGFUL (e.g., plot longitude and latitude on maps where appropriate). They must also be relevant to the specified persona. Each goal must include a question(THE INSIGHT EXTRACTED FROM THE DATA), a visualization (THE VISUALIZATION MUST REFERENCE THE EXACT COLUMN FIELDS FROM THE SUMMARY), and a rationale (JUSTIFICATION FOR WHICH dataset FIELDS ARE USED and what we will learn from the visualization). Each goal MUST mention the exact fields from the dataset summary above
"""
    U_SYSTEM_INSTRUCTIONS = """You are an expert data analyst. The user will provide a summary of a dataset, and your task is to generate goals which only focuses on the distribution and behaviour of the data. From the summary, generate\nQuestions: What are the important questions you should ask about this variable to understand its distribution and behavior?\nSuggested Visualizations: Recommend the most effective visualizations (e.g., histograms, box plots) that would help analyze this variable. Explain why these visualizations are useful.\nRationale: Provide a rationale for the insights you expect to uncover through these visualizations and questions. Why do these questions and visualizations matter for understanding the dataset? """

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
    

    user_prompt = f"""Generate goals which should be based on the data summary below, \n\n
        Summary:\n{summary} \n\n"""
    persona = "A highly skilled data analyst who can come up with complex, insightful goals about the summary, these goals are mainly focused on distribution and behaviour of the data"
    user_prompt += f"""\n The generated goals SHOULD BE FOCUSED ON THE INTERESTS AND PERSPECTIVE of a {persona} persona, who is insterested in complex, insightful goals about the data. \n"""
    messages = [
            {"role": "system", "content": U_SYSTEM_INSTRUCTIONS},
            {"role": "assistant",
             "content":
             f"{user_prompt}\n\n Key Consideration :\n\ni) Leave the Question which produce single line answer (eg:The question which does not require Visualization).\nii)Generate Only 5 goals.\n\n {FORMAT_INSTRUCTIONS} \n\n"}]
    st.write("Basic Information:")
    #st.write(api(messages))
    #exit()
    data = json.loads(api(messages))
    st.write(data)
    for i in data:
        temp = df
        system_prompt = f'''You are an expert data visualization person who knows to code well. You are given the following:\ni)Question: {i['question']}.\nii)Visualization Type: {i['visualization']}.\niii)Data: Provided in a DataFrame named temp.\niv)Summary of the data: "{summary}".\nv) And a function to Complete.'''
        user_prompt = '''Your Objective is to Create a plan to improve and complete the plot_and_save(temp) function, which should:
                                    i) Come up with a optimal plan and used this plan to complete the function.
                                    ii)Ensure that the function handles and processes the input temp (which contains the data) efficiently.
                                    iii)Implement appropriate labels, titles, and legends as needed for better readability.
                                    iv)Ensure the visualization is clear, relevant, and accurate for the question asked.
                        Key Considerations:
                            i) If there are any missing value in the data handle them.
                            ii)Handle exceptions gracefully, such as cases where the data might be missing or the input format is incorrect.
                            iii)Ensure flexibility, modularity, and exception handling for missing or incorrect data.
                            iv) Make sure the plot created should be returned as buffer by executing the following code below:
                                                buf = io.BytesIO()
                                                plt.savefig(buf, format='png')
                                                buf.seek(0)
                                                return buf
Instruction
    1.The data is provided in a DataFrame named temp.
    2.Generate only Python code without any explanations or comments.
    3.Don't import anything apart from given.
    '''
        function ='''
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
<imports>
# solution plan

def plot_and_save(temp: pd.DataFrame):

    <stub> # only modify this section
    '''
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant",
             "content":
             f'''{user_prompt} \n\nThe FUNCTION TO COMPLETE IS :\n{function}'''}]
        with st.spinner("Executing code..."):
            generated_code = api(messages)
        st.code(generated_code, language='Python')
        local_vars = {}
        try:
            exec(generated_code.replace('```python', '').replace('```', ''), globals(), local_vars)
        except:
            continue
        plot_and_save = local_vars['plot_and_save']
        try:
            plot_buffer = plot_and_save(temp)
        except:
            continue
        if plot_buffer:
            st.image(plot_buffer, caption="Age Chart", use_column_width=True)
else:
    st.write("Please upload a CSV or PDF file to proceed.")






















