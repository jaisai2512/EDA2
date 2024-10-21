import json
from API import api
class Univariate:
  def goal_enhancer(p_data,summary,FORMAT_INSTRUCTIONS):
    Q_system_prompt = f'''You are a highly skilled data analyst. Your task is to evaluate the provided goals. If a goal is not appropriate create a new goal and replace it with the old goal, 
    Ask the following questions to evaluate each goal:
    1)Is this an appropriate question to extract valuable information about a variable from the summary, or is there a better way to ask it?
    2)Does this goal provide any highly valuable information to the user?
    Based on your evaluation:
    1)If the answers to questions are yes, then keep the goal unchanged.
    2)If the answer to any of the questions is no, modify the goal to make it optimal for univariate analysis.
    
    '''

    user_prompt = f'Evaluate and improve the goals\nGoals: {p_data}\n\nSummary of the Data: {summary}\n\n Rules :The newly generated, if any, should be based on univariate analysis only.\n{FORMAT_INSTRUCTIONS}'

    messages = [
            {"role": "system", "content": Q_system_prompt},
            {"role": "user","content":f"{user_prompt}" +"Rules:The total number of goals should be only be 5"}]

    data = json.loads(api(messages))

    return data
    
  def goal_generate(summary,FORMAT_INSTRUCTIONS):
    #System Prompt for the llm 
    U_SYSTEM_INSTRUCTIONS = f"""You are an expert data analyst. The user will provide a summary of a dataset, and your task is to generate goals which only focuses on the distribution and behaviour of the ddata. From the summary, generate\nQuestions:Based on the summary given ,What are the Univariate analsysis that can be asked which is highly valuable?\nSuggested Visualizations: Recommend the most effective visualizations (e.g., histograms, box plots) that would help analyze this variable. Explain why these visualizations are useful.\nRationale: Provide a rationale for the insights you expect to uncover through these visualizations and questions. Why do these questions and visualizations matter for understanding the dataset?\n\n Remeber Only generate five goals
    Rule:\ni)PLEASE AVOID THE VARIABLE WHICH HAS NO POTENTIAL OF HAVING DISTRIBUTION OR BEHAVIOUR(EX:ID)\n\n{FORMAT_INSTRUCTIONS}"""

    #User prompt for the llm
    user_prompt = f"""Generate goals which should be based on the data summary below,\n\nSummary:\n{summary} \n\n"""

    messages = [
            {"role": "system", "content": U_SYSTEM_INSTRUCTIONS},
            {"role": "user","content":f"{user_prompt}\n\n Rules :\ni) The goals should be only focused on Univariate Analysis(Strictly no bivariate or multivariate analysis)\nii)Choose appropriate chart types that best represent the data and make the information easy to understand(ex:For distributions: Histograms or box plots)\niii)Please AVOID goals will with time series\niv)Generate only five goals"}]

    u_goal_data = json.loads(api(messages))

    return u_goal_data













   
  
