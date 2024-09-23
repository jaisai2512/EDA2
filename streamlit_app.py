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
    prompt_qa = f'''You are an advanced EDA agent, your role is to perform exploratory data analysis (EDA) on the given data summary . Your task is to break down your findings and present the results in the form of:
                i)Question: What insight or hypothesis are you exploring based on the analysis?
                ii)Visualization: Create or suggest a specific visualization (e.g., histogram, scatter plot, correlation matrix) using the exact dataset column names from the provided summary to illustrate the insight.
                iii)Reason: Justify why you are using those specific fields and what we can learn from the visualization. Explain the significance of the relationships or patterns being revealed.

   
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
 2.Generate 5 questions.
Here is the summary of the data:
{summary}
'''
    st.write("Basic Information:")
    #st.write(api(prompt_qa))
    #exit()
    data = json.loads(api(prompt_qa))
    st.write(data)
    for i in data:
        temp = df
        prompt_vis = f'''You are given:
                                i)A question - {i['question']}.
                                ii)A specific visualization (the recommended chart type for the question) - {i['visualization']}.
                                ii)A summary of the whole data. 
                        Your Objective:
                            Create a plan to improve and complete the plot_and_save(temp) function, which should:
                                    i)Dynamically generate the appropriate visualization based on the given question and corresponding visualization type.
                                    ii)Ensure that the function handles and processes the input temp (which contains the data) efficiently.
                                    iii)Implement appropriate labels, titles, and legends as needed for better readability.
                                    iv)Ensure the visualization is clear, relevant, and accurate for the question asked.
                        Key Considerations:
                            i)The function should be modular and flexible enough to accommodate different types of visualizations based on future questions.
                            ii) If there are any missing value in the data handle them.
                            iii)Handle exceptions gracefully, such as cases where the data might be missing or the input format is incorrect.
                            iv)Ensure flexibility, modularity, and exception handling for missing or incorrect data.
Instruction
    1.The data is provided in a DataFrame named temp.
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
def plot_and_save(temp: pd.DataFrame):

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
            plot_buffer = plot_and_save(temp)
        except:
            continue
        if plot_buffer:
            st.image(plot_buffer, caption="Age Chart", use_column_width=True)
else:
    st.write("Please upload a CSV file to proceed.")






















