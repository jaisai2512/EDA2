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
    summary = '''The Bank Marketing Dataset contains information about bank customers and their responses to marketing campaigns, offering insights into customer demographics, behavior, and interactions with the bank to inform marketing strategies and enhance customer engagement. The dataset includes various fields: the last contact date, which is a date field with no null values, indicating the date of the last contact with customers; the age field represents the customer's age as a discrete numerical value with a mean of 47.0 and no null values; the job field, a categorical nominal field with 59 null values, identifies the job category of the customer; the marital field is also categorical and nominal with no null values, denoting the customer's marital status; the education field, another categorical nominal field, contains 390 null values and represents the customer's education level; the default field indicates whether the customer has defaulted on a loan,
is categorical and nominal with no null values; the balance field represents the customer's account balance as a continuous numerical value with a mean of 1233.0 and no null values; the housing field shows whether the customer owns a house, is categorical and nominal with no null values; the loan field indicates whether the customer has a loan, is categorical and nominal with no null values; the contact field, a categorical nominal field with 2684 null values, represents the customer's contact method; the duration field represents the duration of customer contact as a continuous numerical value with a mean of 106.0 and no null values; the campaign field, representing the number of contacts made to the customer, is a discrete numerical field with a mean of 4.0 and no null values; the pdays field indicates the number of days passed since the last contact, is a discrete numerical field with a mean of 42.0 and no null values; the previous field shows the number of contacts made to the customer in the previous year as a discrete numerical field with a mean of 1.0 and no null values; and the poutcome field represents the outcome of the previous contact as a categorical nominal field with 7508 null values.'''
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

    

    user_prompt = f"""Generate goals which should be based on the data summary below,\n\nSummary:\n{summary} \n\n"""
    #persona = "A highly skilled data analyst who can come up with complex, insightful goals about the summary, and those goals are mainly focused on Univariate Analysis"
    #user_prompt += f"""\n The generated goals SHOULD BE FOCUSED ON THE INTERESTS AND PERSPECTIVE of a {persona} persona \n"""
    messages = [
            {"role": "system", "content": U_SYSTEM_INSTRUCTIONS},
            {"role": "user","content":f"{user_prompt}\n\n Rules :\ni) The goals should be only focused on Univariate Analysis(Strictly no bivariate or multivariate analysis)\nii)Choose appropriate chart types that best represent the data and make the information easy to understand(ex:For distributions: Histograms or box plots)\niii)Please AVOID goals will with time series"}]
    st.write("Basic Information:")
    p_data = json.loads(api(messages))
    #st.write(p_data)
    Q_system_prompt = f'''You are a highly skilled data analyst. Your task is to evaluate the provided goals. If a goal is not appropriate, please propose a new one which replaces the old one , the new goal can either be an improved version of the previous one or a completely new goal.
    Ask the following questions to evaluate each goal:
    1)Is this an appropriate question to extract valuable information about a variable from the summary, or is there a better way to ask it?
    2)Does this goal provide any highly valuable information to the user?
    Based on your evaluation:
    1)If the answers to questions are yes, then keep the goal unchanged.
    2)If the answer to any of the questions is no, modify the goal to make it optimal for univariate analysis.'''
    user_prompt = f'Evaluate and improve the goals\nGoals: {p_data}\n\nSummary of the Data: {summary}\n\n Rules :The newly generated goal, if any, should be based on univariate analysis only.\nOUTPUT THE GOALS IN THE FOLLOWING FOMRAT:{FORMAT_INSTRUCTIONS}'
    messages = [
            {"role": "system", "content": Q_system_prompt},
            {"role": "user","content":f"{user_prompt}"}]
    st.write("New Information:")
    
    M_variate = f'''You are a highly skilled data analyst. Based on the provided dataset summary, your task is to generate goals that focus solely on the relationships between multiple variables and their interactions. For each goal, include the following components:
Questions: Create goals that investigate potential relationships between the specified variable and other fields in the dataset, with a focus on questioning how these variables are related to one another 
Suggested Visualizations: generate an appropriate visualization to help answer the question. Choose the visualization type that best represents the relationship between the variables involved
Rationale: Provide a rationale for the insights you expect to uncover through these questions and visualizations. Explain why these questions and visualizations are important for understanding the relationships between variables in the dataset. What key interactions or patterns do you hope to reveal using these techniques?
Specify the variable used
Can come up with 10 goals
Rules:
1) The VISUALIZATIONS YOU RECOMMEND MUST FOLLOW VISUALIZATION BEST PRACTICES (e.g., must use bar charts instead of pie charts for comparing quantities)
2) Make sure the question is not just comparing but it should have a logical meaning 
3) Striclty no univariate anlysis
{FORMAT_INSTRUCTIONS}
'''

    #messages = [{"role": "system", "content": M_variate},{"role": "user","content":f"{user_prompt}"}]
    
    #st.write(api(messages))
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
        
        user_prompt = '''You are an expert data visualization person who knows to code well. You are given the following:\ni)Question: {i['question']}.\nii)Visualization Type: {i['visualization']}.\niii) Summary : {summary}\niv)Data: Provided in a DataFrame named temp.\n\nv) And a function to Complete.
        Your Objective is to Create a plan to answer the question through a code by improving and complete the plot_and_save(temp) function, which should:
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
                            V) MAKE SURE ONLY CODE IS PRODUCED'''
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






















