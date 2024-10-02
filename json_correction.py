from API import api
def format_correction(summary,format):
  system_prompt = "You are an expert in correcting and optimizing JSON outputs. Given the following JSON format, ensure that all fields have the correct data types and structure, maintaining the intended format."
  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "assistant", "content": f'''
    Here is the JSON that needs to be corrected:
    {summary}
    
    Please optimize this.
    
    The format the JSON needs to follow is:
    {format}
    Return Only the json.
    '''}
]
  result = api(messages)
  return result
