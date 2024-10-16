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
    #st.write(summary)
    SYSTEM_INSTRUCTIONS = """
You are an experienced data analyst who generates a specified number of insightful GOALS based on a univariate analysis of the dataset summary provided and a specified persona. The VISUALIZATIONS YOU RECOMMEND MUST FOLLOW VISUALIZATION BEST PRACTICES (e.g., must use bar charts instead of pie charts for comparing quantities) AND BE MEANINGFUL (e.g., plot longitude and latitude on maps where appropriate). They must also be relevant to the specified persona. Each goal must include a question(THE INSIGHT EXTRACTED FROM THE DATA), a visualization (THE VISUALIZATION MUST REFERENCE THE EXACT COLUMN FIELDS FROM THE SUMMARY), and a rationale (JUSTIFICATION FOR WHICH dataset FIELDS ARE USED and what we will learn from the visualization). Each goal MUST mention the exact fields from the dataset summary above
"""
    U_SYSTEM_INSTRUCTIONS = f"""You are an expert data analyst. The user will provide a summary of a dataset, and your task is to generate goals which only focuses on the distribution and behaviour of the data. From the summary, generate\nQuestions:Based on the summary given ,What are the Univariate analsysis that can be asked which is highly valuable?\nSuggested Visualizations: Recommend the most effective visualizations (e.g., histograms, box plots) that would help analyze this variable. Explain why these visualizations are useful.\nRationale: Provide a rationale for the insights you expect to uncover through these visualizations and questions. Why do these questions and visualizations matter for understanding the dataset?\n\n Remeber Only generate five goals
    Rule:\ni)PLEASE AVOID THE VARIABLE WHICH HAS NO POTENTIAL OF HAVING DISTRIBUTION OR BEHAVIOUR(EX:ID)\n\n{FORMAT_INSTRUCTIONS}"""

    

    user_prompt = f"""Generate goals which should be based on the data summary below, \n\nSummary:\n{summary} \n\n"""
    #persona = "A highly skilled data analyst who can come up with complex, insightful goals about the summary, and those goals are mainly focused on Univariate Analysis"
    #user_prompt += f"""\n The generated goals SHOULD BE FOCUSED ON THE INTERESTS AND PERSPECTIVE of a {persona} persona \n"""
    messages = [
            {"role": "system", "content": U_SYSTEM_INSTRUCTIONS},
            {"role": "user","content":f"{user_prompt}\n\n Rules :\ni) The goals should be only focused on Univariate Analysis(Strictly no bivariate or multivariate analysis)\nii)Choose appropriate chart types that best represent the data and make the information easy to understand(ex:For distributions: Histograms or box plots)\niii)Please AVOID goals will with time series"}]
    st.write("Basic Information:")
    #p_data = json.loads(api(messages))
    #st.write(p_data)
    Q_system_prompt = f'''You are a highly skilled data analyst. Your task is to evaluate the provided goals. If a goal is not appropriate, please propose a new one which replaces the old one , the new goal can either be an improved version of the previous one or a completely new goal.
    Ask the following questions to evaluate each goal:
    1)Is this an appropriate question to extract valuable information about a variable from the summary, or is there a better way to ask it?
    2)Does this goal provide any highly valuable information to the user?
    Based on your evaluation:
    1)If the answers to questions are yes, then keep the goal unchanged.
    2)If the answer to any of the questions is no, modify the goal to make it optimal for univariate analysis.'''
    #user_prompt = f'Evaluate and improve the goals\nGoals: {p_data}\n\nSummary of the Data: {summary}\n\n Rules :The newly generated goal, if any, should be based on univariate analysis only.\nOUTPUT THE GOALS IN THE FOLLOWING FOMRAT:{FORMAT_INSTRUCTIONS}'
    messages = [
            {"role": "system", "content": Q_system_prompt},
            {"role": "user","content":f"{user_prompt}"}]
    st.write("New Information:")
    
    M_variate = f'''You are a highly skilled data analyst. Based on the provided dataset summary, your task is to generate goals that focus solely on the relationships between multiple variables and their interactions. For each goal, include the following components:

Questions: Generate valuable goals which invloves cluster anslysis,correspondence analysis , conjoint analysis and canonical analysis .Avoid any univariate analysis.

Suggested Visualizations: Propose a specific visualization that can effectively help answer the question. Always consider the types of variables involved when creating the visualization. For example, use a scatter plot for continuous vs. continuous relationships.

Rationale: Provide a rationale for the insights you expect to uncover through these questions and visualizations. Explain why these questions and visualizations are important for understanding the relationships between variables in the dataset. What key interactions or patterns do you hope to reveal using these techniques?

Rules:
Ensure the questions, visualizations, and rationale are clear and detailed.
{FORMAT_INSTRUCTIONS}
'''

    messages = [
            {"role": "system", "content": M_variate},
            {"role": "user","content":f"{user_prompt}"}]
    
    st.write(api(messages))
    #exit()
    data = json.loads(api(messages))
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
        
        user_prompt = '''
Objective: Come up with a plan to answer the question by completing the `plot_and_save(temp)` function use the visualization specified in the visuationa part. The function must:
i) Develop an efficient plan to generate the visualization and implement it in the function.
ii) Process the DataFrame "temp" efficiently to create the plot.
iii) Add appropriate labels, titles, and legends, ensuring spacing between legends for clarity.
iv) Handle missing values in the data and other exceptions, such as incorrect input formats.
v) Save the plot to a buffer for return using:
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

Key Considerations:
- The plot must be clear, relevant, and accurate for the question asked.
- Ensure the function is modular, flexible, and has robust error handling for missing or incorrect data
Instruction
    1.The data is provided in a DataFrame named temp.
    2.Generate only Python code without any explanations or comments.
    3.Don't import anything apart from given.
    '''
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






















