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
from Univariate_Analysis import Univariate

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
    data = Univariate.goal_generate(summary,FORMAT_INSTRUCTIONS)

    st.write(data)
    for i in data:
        temp = df
        system_prompt = f'''
You are an expert data visualization specialist and coder. Given:
i) Question: {i['question']}.
ii) Visualization Type: {i['visualization']}.
iii) Summary: {summary}.
iv) Data: A DataFrame named "temp".
v) Incomplete function: plot_and_save(temp).
'''
        
        user_prompt = '''You are an expert in data visualization and coding. You are provided with:
i) Question: {i['question']}.
ii) Summary: {summary}.
iii) Data: Provided in a DataFrame named temp.

Your task is to improve and complete the plot_and_save(temp) function by:
    i) Creating an optimal plan to answer the question.
    ii) Efficiently handling the input data.
    iii) Implementing labels, titles, and legends for clarity.
    iv) Ensuring the visualization is clear, relevant, and accurate.
    v) Adding spacing between the values in the x -axis and y-axis.
    vi) Handling missing data and incorrect input gracefully.
    vii) Returning the plot as a buffer using:
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        return buf.

 
Output only code.'''

        function ='''
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
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






















