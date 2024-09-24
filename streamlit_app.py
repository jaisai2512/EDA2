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
    SYSTEM_INSTRUCTIONS = """
You are a an experienced data analyst who can generate a given number of insightful GOALS about data , when given a summary of the data, and a specified persona. The VISUALIZATIONS YOU RECOMMEND MUST FOLLOW VISUALIZATION BEST PRACTICES  AND BE MEANINGFUL (e.g., plot longitude and latitude on maps where appropriate). They must also be relevant to the specified persona. Each goal must include a question(THE INSIGHT EXTRACTED FROM THE DATA), a visualization (THE VISUALIZATION MUST REFERENCE THE EXACT COLUMN FIELDS FROM THE SUMMARY), and a rationale (JUSTIFICATION FOR WHICH dataset FIELDS ARE USED and what we will learn from the visualization). Each goal MUST mention the exact fields from the dataset summary above
"""

    FORMAT_INSTRUCTIONS = """
THE OUTPUT MUST BE A CODE SNIPPET OF A VALID LIST OF JSON OBJECTS. IT MUST USE THE FOLLOWING FORMAT:

[
    {{
        "question": "...",
        "visualization": "...",
        "reason": "..."
    }},
    ...
]

THE OUTPUT SHOULD ONLY USE THE JSON FORMAT ABOVE.
"""
    

    user_prompt = f"""The number of GOALS to generate is 5. The goals should be based on the data summary below, \n\n .
        {summary} \n\n"""
    persona = "A highly skilled data analyst who can come up with complex, insightful goals about data"
    user_prompt += f"""\n The generated goals SHOULD BE FOCUSED ON THE INTERESTS AND PERSPECTIVE of a {persona} persona, who is insterested in complex, insightful goals about the data. \n"""
    messages = [
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "assistant",
             "content":
             f"{user_prompt}\n\n {FORMAT_INSTRUCTIONS} \n\n Key Consideration:\n\n i) Generate multiple visualization possibilities for the question, and select the one that adheres best to visualization best practices.\nThe generated 5 goals are: \n "}]
    st.write("Basic Information:")
    #st.write(api(messages))
    #exit()
    data = json.loads(api(messages))
    st.write(data)
    for i in data:
        temp = df
        prompt_vis = f'''You are an expert data visualization agent. You are given the following:
                                    i)Question: {i['question']}.
                                    ii)Visualization Type: {i['visualization']}.
                                    iii)Data: Provided in a DataFrame named temp.
                                    iv)Summary of the data: "{summary}".
                                    v) And a function to Complete.
                        Your Objective:
                            Create a plan to improve and complete the plot_and_save(temp) function, which should:
                                    i) Generate a Simple plan so that Completing the function won't be a big hustle.
                                    ii)Ensure that the function handles and processes the input temp (which contains the data) efficiently.
                                    iii)Implement appropriate labels, titles, and legends as needed for better readability.
                                    iv)Ensure the visualization is clear, relevant, and accurate for the question asked.
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






















