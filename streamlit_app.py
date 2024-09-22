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

# Title of the Streamlit app
st.title("EDA Report Generator")

# File uploader widget
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# Check if a file has been uploaded
if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    # Display the content of the CSV file
    st.write("Summary of the CSV file:")
    var_dict = {'df': df}
    summary = summary_gen(df)
    st.write(summary)
    prompt_qa = f'''You are a an experienced data analyst who can generate a given number of insightful GOALS about data, when given a summary of the data . The VISUALIZATIONS YOU RECOMMEND MUST FOLLOW VISUALIZATION BEST PRACTICES (e.g., must use bar charts instead of pie charts for comparing quantities) AND BE MEANINGFUL (e.g., plot longitude and latitude on maps where appropriate). Each goal must include a question, a visualization (THE VISUALIZATION MUST REFERENCE THE EXACT COLUMN FIELDS FROM THE SUMMARY), and a reason (JUSTIFICATION FOR WHICH dataset FIELDS ARE USED and what we will learn from the visualization). Each goal MUST mention the exact fields from the dataset summary above . The questions must be a mix of UNIVARIATE , BIVARIATE AND MULITVARIATE ANALYSES.
   
   The final output should be in valid JSON format as follows:

[
    {{
        "question": "...",
        "visualization": "...",
        "reason": "..."
    }},
    ...
]
Instruction:
 1. No comment should be produced.
Here is the summary of the data:
{summary}
'''
    st.write("Basic Information:")
    
    data = json.loads(api(prompt_qa))
    for i in data:
        prompt_vis = f'''You are tasked with analyzing a dataset through Exploratory Data Analysis (EDA). For this task, you will be provided with predefined imports and functions. Your job is to develop solutions for the following:
                            i)A clear question that guides the analysis.
                            ii)An appropriate visualization that answers the question.
                            iii)A reasoning or explanation for the significance of the question and the insights derived from it.
You must insert your solutions into the designated spaces within the provided function while maintaining the integrity of the overall function.
Instructions:
    1.The data is provided in a DataFrame named df.
    2.Generate only Python code without any explanations or comments.
    3.Don't import anything apart from given.
Here are the details:

Question, visualization, and reason:
“”"
{i}
“”"

Summary of the data:
“”"
{summary}
“”"


import seaborn as sns
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
<imports>
# solution plan
# i.  ..
def plot_and_save(df: pd.DataFrame):

    <stub> # only modify this section
    buf = io.BytesIO()
    plt.savefig(buf, format='png') 
    buf.seek(0)
    return buf'''
        with st.spinner("Executing code..."):
            generated_code = api(prompt_vis)
        st.code(generated_code, language='Python')
        local_vars = {}
        try:
            exec(generated_code.replace('```python', '').replace('```', ''), globals(), local_vars)
        except:
            continue
        plot_and_save = local_vars['plot_and_save']
        try:
            plot_buffer = plot_and_save(df)
        except:
            continue
        if plot_buffer:
            st.image(plot_buffer, caption="Age Chart", use_column_width=True)
else:
    st.write("Please upload a CSV file to proceed.")






















