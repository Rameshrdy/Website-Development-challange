from flask import Flask, render_template, request, flash, redirect, url_for
import fitz  # PyMuPDF library for PDF text extraction

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random secret key for security

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if a file is uploaded
        if 'file' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)

        file = request.files['file']

        # Check if the file is selected
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)

        # Check if the file has a PDF extension
        if not file.filename.endswith('.pdf'):
            flash('File must be a PDF', 'error')
            return redirect(request.url)

        try:
            # Extract text from the PDF using PyMuPDF
            pdf_document = fitz.open_stream(file.read(), 'pdf')
            text = ''
            for page_number in range(pdf_document.page_count):
                page = pdf_document[page_number]
                text += page.get_text()

            # Render the template with extracted text
            return render_template('index.html', text=text)

        except Exception as e:
            # Handle errors
            flash(f'Error processing PDF: {str(e)}', 'error')
            return redirect(request.url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
