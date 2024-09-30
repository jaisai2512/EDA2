from API import api
import Rules
import json
import streamlit as st
def summary_gen(df):
  rules = Rules.extract_data(df)
  st.write(rules)
  prompt = f'''You are a data analyst with expertise in data interpretation using pandas dataframe. You are provided with a dataframe represented as a dictionary. Thoroughly analyze this data and provide a comprehensive summary in a single paragraph. The summary should be rich, compact, and concise, capturing all key information and insights from the data. Ensure that no critical details are omitted while keeping the text engaging.

  Please adhere to the following instructions:
    1.Do not generate any code.
    2.Do not generate tabular columns.
    3.Only use information obtained from the dictionary provided.
    
  Here is the dictionary for analysis:{rules}
    '''

  system_prompt = '''As an experienced data analyst, your task is to annotate datasets based on the following instructions:
  1. Generate a semantic_type (a single word) for each field, based on its values (e.g., company, city, number, supplier, location, gender, longitude, latitude, URL, IP address, zip code, email, etc.).
  2. Determine the data_type as either ordinal, nominal, discrete, or continuous, based on the sample elements.
Return the updated JSON dictionary directly, without any explanation.
'''
  template = '''{
  "dataset_name": "...",
  "dataset_description": "...",
  "fields": [
    {
      "field_name": "...",
      "field_description": "...",
      "semantic_type": "...",
      "data_type": "...",
      "mean": "...",
      "num_of_null": "..."
    },
    ...
  ]
}'''
  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "assistant", "content": f"""
    Please annotate the dictionary below using the provided instructions:
    {rules}
    
    Output template:
    {template}
    """},
]
  summary = json.loads(api(messages))
  return summary
  
