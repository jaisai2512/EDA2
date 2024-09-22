import tempfile
import os
def execute_code_safely(code,var_dict):
        try:
            # Execute the code in a subprocess
            
            # Check if 'output.png' was created
            with tempfile.TemporaryDirectory() as tmp_dir:
              var_dict['tmp_dir'] = tmp_dir
              result = exec(code.replace('```python','').replace('```',''),var_dict)
              output_image_path = result
              if os.path.exists(output_image_path):
                with open(output_image_path, 'rb') as img_file:
                  image_data = img_file.read()
                  return image_data, None
              else:
                return None, "No plot image found. Ensure your code saves the plot as 'output.png'."
      
        except Exception as e:
            return None, f"Error during execution: {str(e)}"
