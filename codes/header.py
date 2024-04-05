import pytesseract
from pdf2image import convert_from_path
import pandas as pd

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\VARUN V KULKARNI\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

pdf_file = '../pdf/MR.ANANDMURTHYHN__AEUTU.pdf'

pages = convert_from_path(pdf_file, first_page=3, last_page=11)

# Define keywords to start and stop text extraction
start_keyword = "Patient events"
end_keyword = "End of recording"

# Flag to indicate when to start and stop extraction
start_extraction = False
end_extraction = False

# Extracted text accumulator
extracted_text = ''

for i, page in enumerate(pages):
    text = pytesseract.image_to_string(page)

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

# Create a Pandas DataFrame with the extracted text
df = pd.DataFrame({'Extracted_Text_header': [extracted_text]})

# Print the DataFrame (optional)
print(df)

# Save the DataFrame to a CSV file
csv_file = 'extracted_text_header.csv'
df.to_csv(csv_file, index=False)

print(f'DataFrame saved to {csv_file}')
