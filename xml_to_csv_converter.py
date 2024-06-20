import csv
import xml.etree.ElementTree as ET

def xml_to_csv(xml_file_path, csv_file_path):
    """Converts an XML file to a CSV file and saves it.

    Args:
        xml_file_path (str): Path to the input XML file.
        csv_file_path (str): Path to save the output CSV file.
    """

    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Open CSV file in write mode
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)

        # Write the header row
        header = [elem.tag for elem in root[0]] 
        writer.writerow(header)

        # Iterate through each employee and write data rows
        for employee in root:
            row = [elem.text for elem in employee]
            writer.writerow(row)

# Specify the path to your XML file
xml_file_path = r'C:\Users\DELL\Desktop\xml-csv\Employees.xml'

# Set the output CSV file path
csv_file_path = "employee.csv"  # This will save it in the current working directory

# Call the function to convert and save
xml_to_csv(xml_file_path, csv_file_path)

print(f"XML file converted to CSV and saved at: {csv_file_path}")
