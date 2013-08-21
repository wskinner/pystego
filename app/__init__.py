from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.debug = True
app.config['UPLOAD_FOLDER'] = '/Users/willskinner/Dropbox/steganography/app/upload'
from app import views
