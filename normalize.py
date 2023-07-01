import csv
import json
import xml.etree.ElementTree as ET

import csv

def normalize_data(data, file_format):
    normalized_data = ""

    if file_format == "csv":
        # Parse CSV data
        reader = csv.reader(data.splitlines())
        rows = list(reader)

        # Normalize CSV data
        # Perform your normalization operations on the rows

        # Convert the normalized data back to CSV format
        normalized_rows = []
        for row in rows:
            normalized_row = [str(cell).lower() for cell in row]  # Convert all cells to lowercase strings
            normalized_rows.append(normalized_row)
        
        normalized_data = "\n".join([",".join(row) for row in normalized_rows])

    return normalized_data

