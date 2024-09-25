def Tabs(summary,df):
  l = []
  for i in summary['fields']:
    l.append(i['field_name'])
  for j in st.tabs(l):
    with j:
      st.header("A cat")
  
