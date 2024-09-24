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
    prompt_qa = f'''You are given:
                         i) Summary of the data
                    Your Objective:
                        Create a goal , Each goal must include a question(THE INSIGHT OBTAINED FROM THE SUMMARY DATA), a visualization (THE VISUALIZATION MUST REFERENCE THE EXACT COLUMN FIELDS FROM THE SUMMARY), and a reason (JUSTIFICATION FOR WHICH dataset FIELDS ARE USED and what we will learn from the visualization). Each goal MUST mention the exact fields from the dataset summary
                    Key Consideration:
                        i)The question should be created considering the data types too.
                        ii) Select the most appropriate visualization for the question by analyzing the data types of the attributes involved.
                        iii) If the selected visuzlization is geographical used geography related graph.
                        iv) Your are allowed to use only the altair,seaborn, matplotlib and plotly libraries for visualization.
                        v) Be cautious when selecting graphs for categorical data types.

   The Goal Structure should be in valid JSON format as follows:

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
                            V) Make sure the plot created should be returned as buffer by executing the following code below:
                                                buf = io.BytesIO()
                                                plt.savefig(buf, format='png')
                                                buf.seek(0)
                                                return buf
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
import plotly.express as px
<imports>
# solution plan
# i.  ..
def plot_and_save(temp: pd.DataFrame):

    <stub> # only modify this section
    '''
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






















