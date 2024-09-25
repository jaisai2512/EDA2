import streamlit as st
def Tabs(summary,df):
  l = []
  for i in summary['fields']:
    l.append(i['field_name'])
  count = 0
  for j in st.tabs(l):
    with j:
      st.header("Field_Name")
      st.write(summary['fields'][count]['field_name'])
      st.header("Field_Description")
      st.write(summary['fields'][count][' field_description'])
      st.header("semantic_type")
      st.write(summary['fields'][count]['semantic_type'])
      st.header("DATA TYPE")
      st.write(summary['fields'][count]['DATA TYPE'])
      count = count +1
  
