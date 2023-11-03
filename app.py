from flask import Flask, request, send_file, render_template, redirect, url_for, flash
import os

app = Flask(__name__)

# Configure a directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensionsso
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'pdf', 'doc', 'docx', 'csv'}

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route to serve the file upload page
@app.route('/')
def file_upload_form():
    return render_template('upload.html')

# Route to handle file uploads (POST request)
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('File successfully uploaded')
        return redirect(url_for('file_upload_form'))
    else:
        flash('Invalid file format. Allowed formats: jpg, jpeg, png, gif, pdf, doc, docx')
        return redirect(request.url)

# Route to serve uploaded files (GET request)
@app.route('/uploads/<filename>')
def get_file(filename):
    print("Attempting to getch filename: ", filename)
    print("From: ", os.path.join(app.config['UPLOAD_FOLDER']))
    return send_file(os.path.join(app.config['UPLOAD_FOLDER'], filename))

if __name__ == '__main__':
    app.secret_key = 'jfskdlm934uiyt4i5oiqw3289ujd92387jnt'  # Change this to a strong and unique secret key
    app.run(host='0.0.0.0', port=5000)  # You may change the host and port as needed
