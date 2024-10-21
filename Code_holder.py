import json
import streamlit as st
from API import api
def code_generation(data,type_analysis,df,summary):
  st.write(f"**{type_analysis}**")
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
        #st.code(generated_code, language='Python')
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
            st.write("Question:\n"+i["question"])
            st.write("Reason:\n"+i["reason"])
            st.image(plot_buffer, caption="Age Chart", use_column_width=True)
