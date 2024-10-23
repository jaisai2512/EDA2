from API import api
import json
import streamlit as st
def goal_enhancer(p_data,summary,FORMAT_INSTRUCTIONS):
    Q_system_prompt = '''You are experienced data analysts responsible for processing a JSON object that includes questions, visualizations, and reasons. Your task is to identify and remove duplicated goals, replacing them with a new multivariate goal based on the provided data summary.

Questions: Based on the given summary, identify valuable multivariate analyses that can be performed. 
Suggested Visualizations: Recommend effective visualizations (e.g., histograms, box plots) to analyze these variables, and explain their utility. 
Rationale: Provide a rationale for the insights expected from these visualizations and questions, emphasizing their importance in understanding the dataset.

Rules: i) Output only the JSON, no additional descriptions.'''

    user_prompt = f'Replace duplicated questions with a new multivariate goal based on the provided JSON: {p_data} and the data summary: {summary}. Ensure adherence to the specified format:\n{FORMAT_INSTRUCTIONS}. Replace the old goals with the new goals and output everything in the required format.'

    messages = [
    {"role": "system", "content": Q_system_prompt},
    {"role": "user", "content": user_prompt}
]

# st.write(api(messages))
    data = json.loads(api(messages))

    return data

def mul_goal_generate(summary,FORMAT_INSTRUCTIONS):
    M_variate = f'''You are a highly skilled data analyst. Based on the provided dataset summary, your task is to generate goals that focus solely on the relationships between multiple variables and their interactions. For each goal, include the following components:
Questions: Create goals that investigate potential relationships between the variabels in the dataset , When creating the goals consider description , sample elements and type of measurement , Generate only  MULTIVARIATE ANALYSIS goals , For now DON'T CREATE GOALS which Involves Time(year,month,date) , ALWAYS allocate a goal for creating a correlation matrix between numerical variabels
Suggested Visualizations: Suggest a single and most effective visualization for answer the question , Consider the type of measurement and description for suggesting the visualization and sample elements ,ollow these rules if the type of measurement is :\ni)continuous vs continuous use scatter plot\nii)discrete vs discrete use Grouped Bar plot\niii)discrete vs continuous use box plot or violin plot\niv)categorical vs categorical use Contingency Plot(Cross Tab)\n
Rationale: Provide a rationale for the insights you expect to uncover through these questions and visualizations. Explain why these questions and visualizations are important for understanding the relationships between variables in the dataset. What key interactions or patterns do you hope to reveal using these techniques?
Specify the variable used
Can come up with 5 goals
Rules:
1) The VISUALIZATIONS YOU RECOMMEND MUST FOLLOW VISUALIZATION BEST PRACTICES (e.g., must use bar charts instead of pie charts for comparing quantities)
2) Striclty no univariate anlysis
{FORMAT_INSTRUCTIONS}
'''
    user_prompt = f"""Generate goals which should be based on the data summary below,\n\nSummary:\n{summary} \n\n"""
    
    messages = [{"role": "system", "content": M_variate},{"role": "user","content":f"{user_prompt}"}]
    data = json.loads(api(messages))
    data = goal_enhancer(data,summary,FORMAT_INSTRUCTIONS)
    return data



