from API import api
import Rules
import json

def summary_gen(df):
  summary = Rules.extract_data(df)
  prompt = f'''You are a data analyst with expertise in data interpretation using pandas dataframe. You are provided with a dataframe represented as a dictionary. Thoroughly analyze this data and provide a comprehensive summary in a single paragraph. The summary should be rich, compact, and concise, capturing all key information and insights from the data. Ensure that no critical details are omitted while keeping the text engaging.

  Please adhere to the following instructions:
    1.Do not generate any code.
    2.Do not generate tabular columns.
    3.Only use information obtained from the dictionary provided.
    
  Here is the dictionary for analysis:{summary}
    '''

  system_prompt = '''You are an experienced data analyst that can annotate datasets. Your instructions are as follows:
i) ALWAYS generate the name of the dataset and the dataset_description
ii) ALWAYS generate a field description.
iii.) ALWAYS generate a semantic_type (a single word) for each field given its values e.g. company, city, number, supplier, location, gender, longitude, latitude, url, ip address, zip code, email, etc
You must return an updated JSON dictionary without any preamble or explanation.
 Here is the dictionary for annonating:{summary}
'''
  messages = [
            {"role": "system", "content": system_prompt},
            {"role": "assistant", "content": f"""
        Annotate the dictionary below. Only return a JSON object.
        {summary}
        """},
        ]
  summary = json.loads(api(messages))
  return summary
  
