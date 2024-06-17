from flask import render_template, request, send_file
from src import app, database
from src.forms import FormNome
from src.models import Nome
from docx import Document
from docx2pdf import convert
import os

@app.route('/', methods=['GET', 'POST'])
def home():
    form = FormNome()
    if request.method == 'POST':
        name = request.form.get('name')
        user = Nome.query.filter_by(name=name).first()
        if user:
            # Caminho para o template do certificado
            template_path = os.path.join(os.path.dirname(__file__), '..', 'CERTIFICADO_WORK.docx')
            
            # Cria o documento a partir do template
            doc = Document(template_path)
            for paragraph in doc.paragraphs:
                if 'USERNAME' in paragraph.text:  # Assume que 'USERNAME' é o placeholder no template
                    paragraph.text = paragraph.text.replace('USERNAME', user.name)
            
            # Caminhos temporários para salvar o .docx e o PDF gerado
            temp_doc_path = 'certificate_{}.docx'.format(user.id)
            temp_pdf_path = 'certificate_{}.pdf'.format(user.id)
            doc.save(temp_doc_path)
            
            # Converte o .docx diretamente para PDF
            convert(temp_doc_path, temp_pdf_path)

            # Envia o arquivo PDF para o usuário
            response = send_file(temp_pdf_path, as_attachment=True)

            # Remove arquivos temporários
            os.remove(temp_doc_path)
            os.remove(temp_pdf_path)

            return response
        else:
            return "User not found", 404
    
    return render_template('index.html', form=form)
