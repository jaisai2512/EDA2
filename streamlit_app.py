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
    prompt_qa = f''' You are a data analyst tasked with performing an EXPLORATORY DATA ANALYSIS (EDA) on a dataset. Your role is to identify patterns by asking questions based on the data summary, ensuring that these questions can only be answered through visualizations, generating relevant visualizations, and providing reasoning for the insights and summary you present. For each insight, ensure you address:
			i)A clear question that guides the analysis.
			ii) A corresponding visualization that answers the question.
			iii) An explanation or reasoning for why this insight is important or relevant to the dataset.
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
	 1. Do not generate any code.
	 2. Only use information obtained from the dictionary provided.,
	 4. Don't generate any comment or anything apart from the json format list.
         5. The question should not be repeated.


Here is the summary of the data:
{summary}
'''
    st.write("Basic Information:")
    
    data = json.loads(api(prompt_qa))
    for i in data:
        prompt_vis = f'''You are a data analyst with coding skills and you are tasked to write a visualization code based on the provided question, visualization, reason and summary of the data

Instructions:
    1.The data is provided in a DataFrame named df.
    2.Generate only Python code without any explanations or comments.
    3.Do not modify any part of the provided code structure below .
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






















