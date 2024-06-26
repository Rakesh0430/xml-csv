import csv
from datetime import datetime
import xml.etree.ElementTree as ET

# File paths
csv_file_path = r"C:\Users\DELL\Desktop\xml-csv\customers.csv"
xml_file_path = r"C:\Users\DELL\Desktop\xml-csv\sorted_customers.xml"

# Read the CSV file
with open(csv_file_path, 'r') as file:
    reader = csv.DictReader(file)
    data = list(reader)

# Sort by Subscription Date (ascending)
data.sort(key=lambda row: datetime.strptime(row['Subscription Date'], "%d-%m-%Y"))

# Create XML structure with vertical format
root = ET.Element('customers')
for row in data:
    for key, value in row.items():
        item = ET.SubElement(root, key)
        item.text = value

# Create an ElementTree object
tree = ET.ElementTree(root)

# Write the XML file
with open(xml_file_path, 'wb') as file:
    tree.write(file, encoding='utf-8', xml_declaration=True)

print("XML file created successfully at:", xml_file_path)
