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
    prompt_qa = f'''You are a an experienced data analyst who can generate a given number of insightful GOALS about data, when given a summary of the data . The VISUALIZATIONS YOU RECOMMEND MUST FOLLOW VISUALIZATION BEST PRACTICES (e.g., must use bar charts instead of pie charts for comparing quantities) AND BE MEANINGFUL (e.g., plot longitude and latitude on maps where appropriate). Each goal must include a question, a visualization (THE VISUALIZATION MUST REFERENCE THE EXACT COLUMN FIELDS FROM THE SUMMARY), and a reason (JUSTIFICATION FOR WHICH dataset FIELDS ARE USED and what we will learn from the visualization). Each goal MUST mention the exact fields from the dataset summary above .
    The question should be based on the mix of the following:
        i)Univariate Analysis Questions: Focus on individual variables.
        ii)Bivariate Analysis Questions: Explore relationships between two variables.
        iii)Multivariate Analysis Questions: Investigate interactions among three or more variables.
   
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
 2.Generate 10 questions.
Here is the summary of the data:
{summary}
'''
    st.write("Basic Information:")
    #st.write(api(prompt_qa))
    #exit()
    data = json.loads(api(prompt_qa))
    for i in data:
        prompt_vis = f'''If the solution requires a single value (e.g. max, min, median, first, last etc), ALWAYS add a line (axvline or axhline) to the chart, ALWAYS with a legend containing the single value (formatted with 0.2F). If using a <field> where semantic_type=date, YOU MUST APPLY the following transform before using that column i) convert date fields to date types using df[''] = pd.to_datetime(df[<field>], errors='coerce'), ALWAYS use  errors='coerce' ii) drop the rows with NaT values df = df[pd.notna(df[<field>])] iii) convert field to right time format for plotting.  ALWAYS make sure the x-axis labels are legible (e.g., rotate when needed). Solve the task  carefully by completing ONLY the <imports> AND <stub> section. Given the dataset summary, the plot_and_save(df) method should generate a chart ({i['visualization']}) that addresses this goal: {i['question']}. DO NOT WRITE ANY CODE TO LOAD THE DATA. The data is already loaded and available in the variable data.
Instructions:
    1.The data is provided in a DataFrame named df.
    2.Generate only Python code without any explanations or comments.
    3.Don't import anything apart from given.
Here are the details:
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
        #st.code(generated_code, language='Python')
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






















