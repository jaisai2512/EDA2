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

  system_prompt = '''You are an experienced data analyst that can annotate datasets. Your instructions are as follows:
  i) ALWAYS generate the name of the dataset and the dataset_description
  ii) ALWAYS generate a field description.
iii) ALWAYS generate a semantic_type (a single word) for each field given its values e.g. company, city, number, supplier, location, gender, longitude, latitude, url, ip address, zip code, email, etc
You must return an updated JSON dictionary without any preamble or explanation.
iv) The DICTIONARY provided has mean  and no of null values add this in the json if mean is dtype('O') then write not applicable.
v) Using sample_elements and column_names_data_types, introduce a new parameter that categorizes the data as either ordinal or nominal. For numeric data, determine whether it is discrete or continuous.
'''
  template = '''{
              dataset_name: ...
              dataset_description: ...
              fields:[
                      0:{field_name: ...,
                        field_description: ...
                        semantic_type: ...
                        DATA TYPE: ...
                        mean: ...
                        num_of_null: ... }
                      1: ...
              ]
                }'''
  messages = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": f"""
        Annotate the dictionary below. .
        {rules}
        Follow the below template,Only return a JSON object:
        {template}
        """},
        ]
  summary = json.loads(api(messages))
  return summary
  
