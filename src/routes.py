import pythoncom  # Importe a biblioteca pythoncom
from docx.shared import Pt
from flask import render_template, request, send_file
from certificado.src import app
from certificado.src.forms import FormNome
from certificado.src.models import Nome
from docx import Document
from docx2pdf import convert
import os
import time


@app.route('/', methods=['GET', 'POST'])
def home():
    pythoncom.CoInitialize()
    form = FormNome()
    if request.method == 'POST':
        nome = request.form.get('nome')
        nome_padronizado = nome.upper()

        user = Nome.query.filter_by(username=nome_padronizado).first()
        print(user)
        if user:

            template_path = os.path.join(os.path.dirname(__file__), '..', 'CERTIFICADO_WORK.docx')

            doc = Document(template_path)

            for paragraph in doc.paragraphs:
                if 'NOME' in paragraph.text:
                    paragraph.text = paragraph.text.replace('NOME', user.username)
                    for run in paragraph.runs:
                        run.font.name = 'Arial'
                        run.font.bold = False
                        run.font.size = Pt(18)

            temp_dir = os.path.join(os.path.dirname(__file__), '..', 'temp_files')
            if not os.path.exists(temp_dir):
                os.makedirs(temp_dir)

            temp_doc_path = os.path.join(temp_dir, 'certificate_{}.docx'.format(user.username))
            temp_pdf_path = os.path.join(temp_dir, 'certificate_{}.pdf'.format(user.username))
            doc.save(temp_doc_path)

            convert(temp_doc_path, temp_pdf_path)

            time.sleep(4)

            if os.path.exists(temp_pdf_path):
                try:
                    return send_file(temp_pdf_path, as_attachment=True)
                except Exception as e:
                    return str(e), 500
            else:
                return "Arquivo PDF não encontrado", 404
        else:
            return "User not found", 404

    return render_template('index.html', form=form)
