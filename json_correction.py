from API import api
def format_correction(summary,format):
  system_prompt = "You are an expert in correcting the JSON output, Your main job to find any missing literals and correct them."
  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "assistant", "content": f'''
    Here is the JSON that needs to be corrected:
    {summary}
    Return Only the json object.
    '''}
]
  result = api(messages)
  return result
