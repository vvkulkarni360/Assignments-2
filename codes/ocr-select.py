import pytesseract
from pdf2image import convert_from_path

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\VARUN V KULKARNI\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

pdf_file = 'MR.ANANDMURTHYHN__AEUTU.pdf'

pages = convert_from_path(pdf_file)

# Define keywords to start and stop text extraction
start_keyword = "Technician's interpretations: "
end_keyword = "Reported by"

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

# Print the extracted text
print(extracted_text)

# Save the extracted text to a file
output_file = 'extracted_text.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write(extracted_text)

print(f'Extracted text saved to {output_file}')
