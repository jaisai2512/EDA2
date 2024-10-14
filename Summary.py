from API import api
import Rules
import json
import streamlit as st
from json_correction import format_correction
def summary_gen(df):
  rules = Rules.get_column_properties(df)

  system_prompt = '''As a seasoned data analyst, your responsibility is to annotate the provided dictionary according to the specified template and follow this instructions below:
  1.Generate a semantic_type (a single word) for each field, based on its values (e.g., company, city, number, supplier, location, gender, longitude, latitude, URL, IP address, zip code, email, etc.).
  2.ALWAYS specify the type_of_data.
  3.ALWAYS specify the description.
'''
  template = '''{
  "dataset_name": "string",
  "dataset_description": "string",
  "number_of_fields": "integer",
  "number_of_rows": "integer",
  "fields_properties": [
    {
      "field_name": "string",
      "field_description": "string",
      "semantic_type": "string",
      "type_of_data": "string",
      "mean": "number",  // INCLUDE ONLY IF APPLICABLE (NOT NULL)
      "num_of_nulls": "integer",
      "sample_elements": ["element_1", "element_2", "..."]  // A list of sample values for the field
    },
    // More fields...
  ]
}
'''
  new_template = '''{
  "dataset_name": "string",
  "dataset_description": "string",
  "fields_properties": [
    {
      "Name": "string",
      "Description": "string",
      "Dtype":"string",
      "Semantic_type": "string",
      "type_of_data": "string", 
      "mean": "number",  // INCLUDE ONLY IF APPLICABLE (NOT NULL)
      "Skewness":"number", // INCLUDE ONLY IF APPLICABLE (NOT NULL)
      "num_of_nulls": "integer",
      "sample_elements": ["element_1", "element_2", "..."]  // A list of sample values for the field
    },
    // More fields...
  ]
}
'''
  information ='''Given a dataset field with the following properties: column name, data type, semantic type, description, unique value count, and sample values, classify the field into one of four categories: nominal, ordinal, discrete, or continuous. Use the following rules:
Nominal: If the data represents categories or labels that have no inherent order, even if numeric (e.g., codes, IDs, or categorical values).
Ordinal: If the data represents categories with a meaningful order but without consistent intervals (e.g., ranks or satisfaction levels).
Discrete: If the data represents countable, distinct numeric values (e.g., whole numbers with specific meanings like area codes or counts).
Continuous: If the data represents measurable, continuous values with consistent intervals (e.g., heights, temperatures, or time).
When classifying, prioritize the semantic type and description to understand the data's purpose. For example, numeric values representing categorical or countable data like area codes should be classified as discrete, not continuous'''
  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "assistant", "content": f"""
    Please annotate the dictionary below using the provided instructions:
    {rules}
    Please Consider the following information and sample elements for choosing type_of_data:
    {information}
    Output template:
    {new_template}
    Return the updated JSON dictionary directly, without any explanation.
    """},
]
  o_summary = api(messages)
  #st.write(o_summary)
  count = 0
  while count <2:
    try:
      count = count +1
      summary = json.loads(o_summary)
      break
    except:
      o_summary = format_correction(o_summary,new_template)
  if(count == 2):
    st.write("reupload")
    exit()
  system_prompt ='''As an experienced data analyst, your task is to create a structured dataset annotation based on the provided template. Follow these instructions:
      1. Fill in the dataset title and description accurately, ensuring clarity about the dataset's purpose and context.
      2. For each field in the dataset:
        i)Provide a concise description of the field's properties.
  '''
  temp = '''
      Dataset Title(Bold text): 
      [Provide the title of the dataset here]

      Dataset Description(Bold text): 
      [Provide a brief description of the dataset, including its purpose and any relevant context]

      Fields(Bold text):
          - Field 1(Bold text): 
                A summry on this field covering all the properties
          - Field 2(Bold text): 
                 A summry on this field covering all the properties
            [Continue for additional fields as necessary]
            ...
      '''
  sum = [
    {"role": "system", "content": system_prompt},
    {"role": "assistant", "content": f"""
    Please Create a summary based on the json given below:
    {summary}
    Output template:
    {temp}
    """},
]
  s = api(sum)
  st.write(s)
  
  return s
  
