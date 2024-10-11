import pandas as pd

def validate_obj(column):
    if column.isna().all():
        return 'All rows are null'
    unique_values = column.nunique()
    total_values = len(column)
    threshold = 0.5
    return "categorical" if  unique_values< (total_values*threshold) else "textual"

def sample(column,dt):
    unique_values = column.nunique()
    total_values = len(column)
    threshold = 0.5
    if((dt != 'categorical') and (dt !='textual')):
        return column[:6].tolist()
    if(dt == 'categorical' and (unique_values< (total_values*threshold)) and (unique_values<20 )):
        return list(column.unique())
    else:
        return column[:6].tolist()


def extract_data(data: pd.DataFrame) -> dict:
    num_rows, num_columns = data.shape

    column_data_types = {
        column: validate_obj(data[column]) if data[column].dtype == 'O' else data[column].dtype
        for column in data.columns
    }

    mean = {
        column:round(data[column].mean(),2)  if data[column].dtype in ['int64','float64',int,float] 
        for column in data.columns
    }

    no_null = {
        column: data[column].isnull().sum() for column in data.columns
    }

    sample_elements = {
        column:sample(data[column],column_data_types[column]) for column in data.columns
    }

    rules = {
        'num_rows': num_rows,
        'num_columns': num_columns,
        'column_names_data_types': column_data_types,
        'mean' : mean,
        'num_of_null' : no_null,
        'sample_elements':sample_elements
        
    }

    return rules
