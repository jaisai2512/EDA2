from API import api
import Rules
import json
import streamlit as st
def summary_gen(df):
  rules = Rules.extract_data(df)
  prompt = f'''You are a data analyst with expertise in data interpretation using pandas dataframe. You are provided with a dataframe represented as a dictionary. Thoroughly analyze this data and provide a comprehensive summary in a single paragraph. The summary should be rich, compact, and concise, capturing all key information and insights from the data. Ensure that no critical details are omitted while keeping the text engaging.

  Please adhere to the following instructions:
    1.Do not generate any code.
    2.Do not generate tabular columns.
    3.Only use information obtained from the dictionary provided.
    
  Here is the dictionary for analysis:{rules}
    '''

  system_prompt = '''As an experienced data analyst, your task is to annotate datasets based on the following instructions:
  1.ALWAYS specify the field name.
  2.ALWAYS specify the field description should be consice.
  3.Generate a semantic_type (a single word) for each field, based on its values (e.g., company, city, number, supplier, location, gender, longitude, latitude, URL, IP address, zip code, email, etc.).
  4.ALWAYS specify the data_type as either ordinal, nominal, discrete, or continuous, based on the sample elements.
  5.ALWAYS specify mean values if it object then specify it as not numeric.
  6.ALWAYS specify num_of_null keep it has integer.
  7.ALWAYS include sample_elements, this should same as in the dictionary.
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
      "num_of_null": "...",
      "sample_elements": "..."
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
  system_prompt ='''As an experienced data analyst, your task is to create a structured dataset annotation based on the provided template. Follow these instructions:
      1. Fill in the dataset title and description accurately, ensuring clarity about the dataset's purpose and context.
      2. For each field in the dataset:
        i)Provide a concise description of the field's properties.
  '''
  temp = '''
      Dataset Title: 
      [Provide the title of the dataset here]

      Dataset Description: 
      [Provide a brief description of the dataset, including its purpose and any relevant context]

      Fields:
          - Field 1 Name: 
                A summry on this field covering all the properties
          - Field 2 Name: 
                 A summry on this field covering all the properties
            [Continue for additional fields as necessary]
            ...
      '''
  sum = messages = [
    {"role": "system", "content": system_prompt},
    {"role": "assistant", "content": f"""
    Please Create a summary based on the json given below:
    {summary}
    Output template:
    {temp}
    """},
]
  st.write(api(sum))
  
  return summary
  
