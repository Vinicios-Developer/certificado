from flask import send_file
from flask import request
from flask import Flask, render_template
from io import BytesIO
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from src.models import Nome

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        nome = request.form.get('nome')
        nome_padronizado = nome.upper()

        user = Nome.query.filter_by(username=nome_padronizado).first()
        if user:
            template_path = 'CERTIFICADO_WORK.docx'
            doc = Document(template_path)

            for paragraph in doc.paragraphs:
                if 'NOME' in paragraph.text:
                    paragraph.text = paragraph.text.replace('NOME', user.username)

            pdf_path = f'temp_files/certificate_{user.username}.pdf'
            doc.save('temp_files/temp.docx')

            docx_file = 'temp_files/temp.docx'
            pdf_file = pdf_path

            # Converting DOCX to PDF
            convert_docx_to_pdf(docx_file, pdf_file)

            return send_file(pdf_file, as_attachment=True)

    return render_template('index.html')

def convert_docx_to_pdf(input_docx, output_pdf):
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.lib.units import inch
    from docx import Document as DocxDocument
    from io import BytesIO

    # Read the DOCX file
    doc = DocxDocument(input_docx)

    # Create a buffer for the PDF
    buffer = BytesIO()

    # Create a PDF document
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    # Process each paragraph in the DOCX file
    for para in doc.paragraphs:
        text = para.text.strip()
        pdf_content = f'<para>{text}</para>'
        pdf.build([pdf_content], styles['Normal'])

    # Write the PDF document to the output file
    with open(output_pdf, 'wb') as f:
        f.write(buffer.getvalue())

if __name__ == '__main__':
    app.run()
