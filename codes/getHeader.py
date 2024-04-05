import pandas as pd
import re
import pytesseract
from pdf2image import convert_from_path

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\VARUN V KULKARNI\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

pdf_file = '../pdf/MR.ANANDMURTHYHN__AEUTU.pdf'

try:
    pages = convert_from_path(pdf_file, first_page=3, last_page=11)
except Exception as e:
    print(f"Error during PDF conversion: {e}")
    pages = []

start_keyword = "Patient events"
end_keyword = "End of recording"

# Flag to indicate when to start and stop extraction
start_extraction = False
end_extraction = False

# Extracted text accumulator
extracted_text = ''

for i, page in enumerate(pages):
    text = pytesseract.image_to_string(page)

    # print(f"Page {i+1} OCR output:\n{text}\n")  # Print OCR output for debugging

    # Check if start keyword is encountered
    if start_keyword in text:
        start_extraction = True

    # Check if end keyword is encountered
    if end_keyword in text:
        end_extraction = True

    # Append text to accumulator if extraction flag is True
    if start_extraction and not end_extraction:
        extracted_text += text + '\n'

    # Break loop if both start and end keywords are encountered
    if start_extraction and end_extraction:
        break

# Define a regex pattern for matching the header format
header_pattern = r'(\d{2}\.\w+\s\d{2}:\d{2}:\d{2})\s(\w+)\s(\w+\s\(\w+\))\s(\w+|\s)'

# Find all lines that match the header pattern
header_lines = re.findall(header_pattern, extracted_text)

# Replace empty "Findings" with "None"
header_lines = [(time_date, reported, evaluation, 'None' if findings.strip() == '' else findings) for time_date, reported, evaluation, findings in header_lines]

print(f"Extracted Headers:\n{header_lines}\n")  # Print extracted headers for debugging

# Create a DataFrame with the extracted headers
df = pd.DataFrame(header_lines, columns=['Time_Date', 'Reported', 'Evaluation', 'Findings'])

# Print the DataFrame (optional)
print(df)

# Save the DataFrame to a CSV file
csv_file = 'extracted_getheaders.csv'
df.to_csv(csv_file, index=False)

print(f'Headers extracted and saved to {csv_file}')
