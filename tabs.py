import streamlit as st
def Tabs(summary,df):
  l = []
  for i in summary['fields']:
    l.append(i['field_name'])
  count = 0
  for j in st.tabs(l):
    with j:
      st.header("field_Name")
      st.write(summary['fields'][count])
      count = count +1
  