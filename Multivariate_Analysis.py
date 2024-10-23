from API import api
import json
def goal_enhancer(p_data,summary,FORMAT_INSTRUCTIONS):
    Q_system_prompt = f'''You are a highly skilled data analyst. Your task is to evaluate the provided goals. If a goal is not appropriate create a new goal and replace it with the old goal, 
    Ask the following questions to evaluate each goal:
    1)Is this an appropriate question to extract valuable information about a variable from the summary, or is there a better way to ask it?
    2)Does this goal provide any highly valuable information to the user?
    3)Does there are dupliates between the goals? 
    Based on your evaluation:
    1)If the answers to questions are yes, then keep the goal unchanged.
    2)If the answer to any of the questions is no, generate a new goal to make it optimal for multivariate analysis .
    '''

    user_prompt = f'Evaluate and improve the goals\nGoals: {p_data}\n\nSummary of the Data: {summary}\n\n Rules :The newly generated, if any, should be based on multivariate analysis only.\n{FORMAT_INSTRUCTIONS}'

    messages = [
            {"role": "system", "content": Q_system_prompt},
            {"role": "user","content":f"{user_prompt}" +"Make sure no duplicates are present between the goals and total goals should be only 5"}]

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



