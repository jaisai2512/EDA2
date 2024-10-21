import json
from API import api
class Univariate:
  def goal_enhancer(p_data,summary,FORMAT_INSTRUCTIONS):
    Q_system_prompt = f'''ou are a highly skilled data analyst. Your task is to critically evaluate the provided goals to ensure they are optimized for extracting valuable insights through univariate analysis. Follow these steps to evaluate and, if needed, improve each goal:
    Assess the Goal:
    i)Clarity and Purpose: Is the goal clearly stated, and does it aim to extract valuable information about a variable from the summary? If not, suggest a clearer and more meaningful question.
Value and Insight: Does the goal provide valuable and actionable information for the user? Can the insight derived from this goal lead to important conclusions? If not, adjust the goal to ensure it yields highly valuable information.
    ii)Refine the Goal:\n1)If both criteria are met (i.e., clarity and value), keep the goal unchanged.\n2)If either criterion is not met, modify the goal to make it optimal for univariate analysis. Your revised goal can be an improved version of the original or a completely new one if the initial goal is not suitable.
    iii)Evaluation Questions:
        1)Is this an appropriate question to extract valuable information from the summary about the variable, or is there a better way to phrase it?
        2)Does this goal provide highly valuable insights for the user?
    If the goal is good, Then Don;t change the goal, If the goal needs improvement, provide the new, improved goal replace with the old one.
    {FORMAT_INSTRUCTIONS}
    '''

    user_prompt = f'Evaluate and improve the goals\nGoals: {p_data}\n\nSummary of the Data: {summary}\n\n Rules :The newly generated, if any, should be based on univariate analysis only.\n'

    messages = [
            {"role": "system", "content": Q_system_prompt},
            {"role": "user","content":f"{user_prompt}" }]

    data = json.loads(api(messages))

    return data
    
  def goal_generate(summary,FORMAT_INSTRUCTIONS):
    #System Prompt for the llm 
    U_SYSTEM_INSTRUCTIONS = f"""You are an expert data analyst. The user will provide a summary of a dataset, and your task is to generate goals which only focuses on the distribution and behaviour of the data. From the summary, generate\nQuestions:Based on the summary given ,What are the Univariate analsysis that can be asked which is highly valuable?\nSuggested Visualizations: Recommend the most effective visualizations (e.g., histograms, box plots) that would help analyze this variable. Explain why these visualizations are useful.\nRationale: Provide a rationale for the insights you expect to uncover through these visualizations and questions. Why do these questions and visualizations matter for understanding the dataset?\n\n Remeber Only generate five goals
    Rule:\ni)PLEASE AVOID THE VARIABLE WHICH HAS NO POTENTIAL OF HAVING DISTRIBUTION OR BEHAVIOUR(EX:ID)\n\n{FORMAT_INSTRUCTIONS}"""

    #User prompt for the llm
    user_prompt = f"""Generate goals which should be based on the data summary below,\n\nSummary:\n{summary} \n\n"""

    messages = [
            {"role": "system", "content": U_SYSTEM_INSTRUCTIONS},
            {"role": "user","content":f"{user_prompt}\n\n Rules :\ni) The goals should be only focused on Univariate Analysis(Strictly no bivariate or multivariate analysis)\nii)Choose appropriate chart types that best represent the data and make the information easy to understand(ex:For distributions: Histograms or box plots)\niii)Please AVOID goals will with time series\niv)Generate only five goals"}]

    u_goal_data = json.loads(api(messages))

    return u_goal_data













   
  
