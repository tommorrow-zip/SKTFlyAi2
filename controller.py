from flask import Flask, render_template
import pymysql
from models import *

app = Flask(__name__)

# 메인화면
@app.route('/')
def index():
    return render_template('index.html', furniture_classification_list=furniture_classification(), furniture_list=furniture())

if __name__ == '__main__':
    app.run(debug=True)