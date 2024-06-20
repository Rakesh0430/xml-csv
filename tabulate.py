import csv

# Read the CSV file
with open("employee.csv", "r", encoding="utf-8") as file:
    reader = csv.reader(file)
    data = list(reader)

# Calculate column widths for better alignment
col_widths = [max(len(str(val)) for val in col) for col in zip(*data)]

# Print the table with formatting
for row in data:
    print(" | ".join(str(val).ljust(width) for val, width in zip(row, col_widths)))

