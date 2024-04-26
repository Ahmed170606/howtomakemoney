import json
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

input_json_file = "JSON_PROCESSED"
output_pdf_file = "INVOICE"

with open(input_json_file, 'r') as json_file:
    data = json.load(json_file)

# Create a PDF file
c = canvas.Canvas(output_pdf_file, pagesize=A4)
c.setFont("Helvetica", 12)

# Write JSON data to the PDF file
y_position = 700  # Starting y position
for key, value in data.items():
    c.drawString(100, y_position, f"{key}: {value}")
    y_position -= 20  # Move to the next line

c.save()
print(f"PDF '{output_pdf_file}.pdf' successfully created.")
c.save()
