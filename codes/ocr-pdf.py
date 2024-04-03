import pytesseract
from pdf2image import convert_from_path

# Set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\VARUN V KULKARNI\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

pdf_file = 'MR.ANANDMURTHYHN__AEUTU.pdf'

pages = convert_from_path(pdf_file)

# Open a text file in write mode
output_file = 'extracted_text.txt'
with open(output_file, 'w', encoding='utf-8') as f:
    for i, page in enumerate(pages):
        text = pytesseract.image_to_string(page)
        
        # Write the extracted text to the file
        f.write(f'Page {i+1} Text:\n')
        f.write(text + '\n')
        f.write('-' * 50 + '\n')

print(f'Extracted text saved to {output_file}')
