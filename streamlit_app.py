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
    summary,d_summary = summary_gen(df)
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

    M_variate = f'''You are an expert data analyst. The user will provide a summary of a dataset, and your task is to generate goals that focus solely on the relationships between multiple variables and their interactions, using specific multivariate analysis techniques such as Pearson correlation, Spearman correlation, or interaction effects. From the summary, generate:
        1)Questions: Based on the type of measurement provided, what are the most valuable multivariate analysis questions that can be asked? Use specific techniques such as:\ni)For visualizing linear relationships between continuous variables (e.g., scatter plots with correlation coefficients).\nii)For visualizing rank-based or ordinal relationships (e.g., heatmaps for ranked variables)\niii)Interaction effects for visualizing how relationships between two variables change with a third (e.g., interaction plots or 3D surface plots).
        2)Suggested Visualizations: Come up with a visualization which is the most effective way to visually express the question (e.g., scatter plots , correlation matrices, pair plots, 3D scatter plots).
        3)Rationale: Provide a rationale for the insights you expect to uncover through these questions and visualizations. Why are these questions and visualizations important for understanding the relationships between variables in the dataset? What key interactions or patterns do you hope to reveal using these techniques?
Remember to generate exactly five goals.
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
        system_prompt = f'''You are an expert data visualization person who knows to code well. You are given the following:\ni)Question: {i['question']}.\nii)Visualization Type: {i['visualization']}.\niii)Reason : {i['reason']}\niv)Data: Provided in a DataFrame named temp.\nv)Summary of the data: {summary}.\nvi) And a function to Complete.'''
        user_prompt = '''Your Objective is to Create a plan to improve and complete the plot_and_save(temp) function, which should:
                                    i) Come up with a optimal plan and used this plan to complete the function.
                                    ii)Ensure that the function handles and processes the input temp (which contains the data) efficiently.
                                    iii)Implement appropriate labels, titles, and legends as needed for better readability.
                                    iv)Ensure the visualization is CLEAR, RELEVANT, and ACCURATE for the question asked.
                                    v) Rember to add spacing between the legends in the graph.
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






















