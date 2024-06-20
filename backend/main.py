from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, PlainTextResponse
import csv
import xml.etree.ElementTree as ET

app = FastAPI()

def xml_to_csv(xml_data, csv_file_path="output.csv"):
    root = ET.fromstring(xml_data)
    with open(csv_file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([elem.tag for elem in root[0]])  # Header
        for child in root:
            writer.writerow([subchild.text for subchild in child])
    return csv_file_path

def csv_to_xml(csv_file_path, xml_file_path="output.xml"):
    tree = ET.Element("data")  # Replace 'data' with a meaningful root tag
    with open(csv_file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            item = ET.SubElement(tree, "item")  # Replace 'item' if needed
            for key, value in row.items():
                ET.SubElement(item, key).text = value
    ET.ElementTree(tree).write(xml_file_path, encoding="utf-8", xml_declaration=True)
    return xml_file_path

@app.post("/convert/xml_to_csv")
async def convert_xml_to_csv(file: UploadFile = File(...)):
    xml_data = await file.read()
    csv_file_path = xml_to_csv(xml_data.decode("utf-8"))
    return FileResponse(csv_file_path, media_type="text/csv", filename="converted.csv")

@app.post("/convert/csv_to_xml")
async def convert_csv_to_xml(file: UploadFile = File(...)):
    csv_file_path = f"temp_{file.filename}"
    with open(csv_file_path, "wb") as f:
        f.write(await file.read())
    xml_file_path = csv_to_xml(csv_file_path)
    return FileResponse(xml_file_path, media_type="application/xml", filename="converted.xml")

@app.get("/")
async def root():
    return {"message": "Welcome to the XML-CSV Converter API!"}
