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
                    Criteria for Each Goal:
                            Question:
                                i)The question must arise directly from the summary's key insights.
                                ii)It should be actionable, correct, and of high value to the user, offering critical insights into the data.
                                iii)For example, "What is the relationship between road type (road_type) and damage severity (damage_severity) in the dataset?"
                            Visualization:
                                i)The visualization should clearly represent the question in graphical form.
                                ii)It should reference specific column fields from the dataset that directly contribute to the insight.
                                iii)Specify the chart type (e.g., bar chart, scatter plot, heatmap) and explain the process: "A bar chart with road_type on the X-axis and the average damage_severity on the Y-axis will illustrate the relationship."
                                iv)Ensure the visualization method chosen is the best way to showcase the data (e.g., use a heatmap for correlations, bar chart for categories, scatter plots for continuous variables).
                            Reason:
                                i)Justify why the specific dataset fields were used and how the visualization will reveal new insights.
                                ii)Mention the learning outcome from this visualization: "This visualization will help identify if certain road types are more prone to severe damage, which can guide future maintenance priorities."
                    Key Consideration:
                        i) Your are allowed to use only the altair,seaborn, matplotlib and plotly libraries for visualization.
                        ii) Be cautious when selecting graphs for categorical data types.
                        iii) No comment should be created.

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
    st.write(api(prompt_qa))
    exit()
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






















