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
from Univariate_Analysis import goal_generate
from Multivariate_Analysis import mul_goal_generate
from Code_holder import code_generation

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
    
    univariate_data = goal_generate(summary,FORMAT_INSTRUCTIONS)
    #st.write(univariate_data)
    code_generation(univariate_data,'Univariate Analysis',df,summary)

    multivariate_data = mul_goal_generate(summary,FORMAT_INSTRUCTIONS)
    code_generation(univariate_data,'Multivariate Analysis',df,summary)
    
else:
    st.write("Please upload a CSV or PDF file to proceed.")






















