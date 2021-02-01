from flask_cors import CORS
from werkzeug.utils import redirect
from app import App
import os
from flask import Flask, request, url_for
from config.api import api


app = Flask(__name__)
CORS(app)


@app.route('/progress')
def get_progress():
    domains = count_domains()
    processed = 0
    if os.path.isfile(os.path.join(os.getcwd(), "DOMAIN-report.xlsx")):
        processed = domains_processed()
    return "<!doctype html><title>Upload new File</title><span>" + str(domains) + " added</span> <br> <span><strong>" + str(processed) + " processed</strong></span>"


def start_process():
    App()


@app.route('/wd/hub', methods=['POST', 'GET'])
def save():
    if request.method == 'POST':
        file = request.files['file']
        save_path = os.getcwd() + "/upload/"
        if os.path.exists(save_path):
            pass
        else:
            os.makedirs(save_path)
        file.save(save_path + file.filename)
        return redirect(url_for('get_progress'))

    return """<!doctype html><title>Upload new File</title><h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data><input type='file' name='file' required='' accept='.csv, text/plain'><input type='submit' value='Upload'></form>"""


def count_domains():
    count = 0
    try:
        for files in os.listdir(os.path.join(os.getcwd(), "upload")):
            path = os.path.join(os.getcwd(), "upload", files)
            if path.endswith(".txt"):
                with open(path, 'r', encoding='utf-16') as file:
                    count = sum(1 for line in file)
            elif path.endswith(".csv"):
                with open(path, 'r') as file:
                    count = sum(1 for line in file)
    except:
        pass
    return count


def domains_processed():
    with open(os.path.join(os.getcwd(), "DOMAIN-report.xlsx"), 'r') as file:
        count = sum(1 for line in file)
    return count


if __name__ == "__main__":
    app.run(debug=api['debug'], threaded=api['threaded'], host=api['host'], port=api['port'])
