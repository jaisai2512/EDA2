from sambaparse import parse_doc_universal
import os
def pdf_parser(uploaded_file):
  temp_dir = "tempDir"
  if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Save the uploaded file temporarily to get the file path
    file_path = os.path.join(temp_dir, uploaded_file.name)
    with open(file_path, "wb") as f:    
        f.write(uploaded_file.getbuffer())

    # Display the file path
    st.write("File saved at:", file_path)
    additional_metadata = {'key': 'value'}
    texts, metadata_list, langchain_docs = parse_doc_universal(file_path,additional_metadata,source_type, additional_metadata)
    for i in langchain_docs:
        st.write(i)
        exit()
