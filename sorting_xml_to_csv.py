import xmltodict
import pandas as pd
import json

def xml_to_csv_sorted(xml_file_path, output_csv_path):
    # Read the XML file
    with open(xml_file_path, 'r', encoding='utf-8') as file:
        xml_data = file.read()

    # Parse the XML data
    try:
        xml_dict = xmltodict.parse(xml_data)
        print("Parsed XML structure:")
        print(json.dumps(xml_dict, indent=2))  # Pretty-print the structure
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return
    
    # Identify the correct path to the employee data
    try:
        # Based on the provided XML structure
        employees = xml_dict['employees']['employee']
        df = pd.json_normalize(employees)
    except KeyError as e:
        print(f"KeyError: {e} - Please adjust the path to match your XML structure.")
        return
    except Exception as e:
        print(f"Error converting XML to DataFrame: {e}")
        return

    # Ensure the 'salary' column is treated as numeric
    df['salary'] = pd.to_numeric(df['salary'])

    # Sort the DataFrame by the 'salary' column in ascending order
    if 'salary' in df.columns:
        df = df.sort_values(by='salary', ascending=True)
    else:
        print("The 'salary' column does not exist in the XML data.")
        return

    # Save the sorted DataFrame to a CSV file
    try:
        df.to_csv(output_csv_path, index=False)
        print(f"CSV file saved successfully to {output_csv_path}")
    except Exception as e:
        print(f"Error saving CSV file: {e}")

# Path to the XML file
xml_file_path = r"C:\Users\DELL\Desktop\xml-csv\Employees.xml"
# Path to save the output CSV file
output_csv_path = r"C:\Users\DELL\Desktop\xml-csv\Sorted_Employees.csv"

# Convert and save the XML to CSV
xml_to_csv_sorted(xml_file_path, output_csv_path)
