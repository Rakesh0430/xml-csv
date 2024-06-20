import csv
import xml.etree.ElementTree as ET

def csv_to_xml(csv_file_path, xml_file_path):
    """Converts a CSV file to an XML file and saves it with indentation."""

    root = ET.Element('customers')

    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        for row in reader:
            customer = ET.SubElement(root, 'customer')
            for i, value in enumerate(row):
                ET.SubElement(customer, header[i]).text = value

    tree = ET.ElementTree(root)

    # Indent the XML tree for better readability
    ET.indent(tree, space="\t", level=0)  # Use tab for indentation

    tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)

# Specify the path to your CSV file
csv_file_path = r'C:\Users\DELL\Desktop\xml-csv\customers.csv'

# Set the output XML file path
xml_file_path = 'customer_xml.xml' 

# Call the function to convert and save
csv_to_xml(csv_file_path, xml_file_path)

print(f"CSV file converted to XML and saved at: {xml_file_path}")

