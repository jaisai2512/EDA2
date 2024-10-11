from API import api
import Rules
import json
import streamlit as st
from json_correction import format_correction
def summary_gen(df):
  rules = Rules.extract_data(df)

  system_prompt = '''As a seasoned data analyst, your responsibility is to annotate the provided dictionary according to the specified template and follow this instructions below:
  1.Generate a semantic_type (a single word) for each field, based on its values (e.g., company, city, number, supplier, location, gender, longitude, latitude, URL, IP address, zip code, email, etc.).
  2.ALWAYS specify the data_type as either ordinal, nominal, discrete, or continuous, based on the sample elements.
  Return the updated JSON dictionary directly, without any explanation.
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
      "data_type": "string",
      "mean": "number",  // INCLUDE ONLY IF APPLICABLE (NOT NULL)
      "num_of_nulls": "integer",
      "sample_elements": ["element_1", "element_2", "..."]  // A list of sample values for the field
    },
    // More fields...
  ]
}
'''
  information ='''Nominal: Qualitative data that categorizes variables into distinct, non-ordered groups. Example: categories like "red," "blue," or "green."
  Ordinal: Qualitative data that classifies variables into ordered categories. While there is a ranking, the intervals between categories are not defined. Example: "poor," "middle income," "wealthy."
  Interval/Ratio:interval data has equal intervals but no true zero point (e.g., temperature in Celsius), while ratio data has a meaningful zero point (e.g., height, weight).'''
  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "assistant", "content": f"""
    Please annotate the dictionary below using the provided instructions:
    {rules}
    Please Consider the following information and sample elements for choosing data_type:
    {information}
    Output template:
    {template}
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
      o_summary = format_correction(o_summary,template)
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
  st.write(api(sum))
  
  return summary
  
