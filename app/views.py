from app import app
from flask import render_template, flash, redirect
from flask import request, send_from_directory, url_for
from forms import LoginForm, Form
import os

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Will'}
    posts = [
            {'author': {'nickname': 'john'}, 'body': 'foobar'},
            {'author': {'nickname': 'jeff'}, 'body': 'baz'}
            ]
    return render_template('index.html', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID=%s, remember_me=%s' %
                (form.openid.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/show/<filename>', methods=['GET', 'POST'])
def uploaded_file(filename):
    filename = 'http://127.0.0.1:5000/uploads/' + filename
    return render_template('show.html', filename=filename)

@app.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
            return redirect(url_for('uploaded_file', filename=file.filename))
    else:
        form = Form()
        return render_template('upload.html', title='Upload Images', form=form)
