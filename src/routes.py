from docx.shared import Pt
from flask import render_template, request, send_file

from certificado.src import app
from certificado.src.forms import FormNome
from certificado.src.models import Nome
from docx import Document
from docx2pdf import convert
import os


@app.route('/', methods=['GET', 'POST'])
def home():
    form = FormNome()
    if request.method == 'POST':
        nome = request.form.get('nome')
        user = Nome.query.filter_by(username=nome).first()
        print(user)
        if user:
            # Caminho para o template do certificado
            template_path = os.path.join(os.path.dirname(__file__), '..', 'CERTIFICADO_WORK.docx')
            
            # Cria o documento a partir do template
            doc = Document(template_path)

            for paragraph in doc.paragraphs:
                if 'NOME' in paragraph.text:
                    paragraph.text = paragraph.text.replace('NOME', user.username)
                    paragraph.style.font.name = 'Arial'
                    paragraph.style.font.bold = True
                    paragraph.style.font.size = Pt(20)

            # Caminhos temporários para salvar o .docx e o PDF gerado
            temp_doc_path = 'certificate_{}.docx'.format(user.username)
            temp_pdf_path = os.path.join(os.path.dirname(__file__), 'certificado',
                                         'certificate_{}.pdf'.format(user.username))
            doc.save(temp_doc_path)

            # Converte o .docx diretamente para PDF
            convert(temp_doc_path, temp_pdf_path)

            # Verifica se o arquivo PDF existe antes de enviar
            if os.path.exists(temp_pdf_path):
                try:
                    return send_file(temp_pdf_path, as_attachment=True)
                except Exception as e:
                    return str(e), 500  # Retorna o erro para depuração
                finally:
                    os.remove(temp_doc_path)
            else:
                return "Arquivo PDF não encontrado", 404
        else:
            return "User not found", 404

    return render_template('index.html', form=form)
