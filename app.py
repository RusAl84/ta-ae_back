from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
import os
import time
import convertQA as conv
import urllib.request
import process_nlp
import config as cfg
from tmodel import tmodel
from flask import Flask, jsonify, render_template, request, send_from_directory
from pathlib import Path
import re
from pymorphy2 import MorphAnalyzer
from nltk.corpus import stopwords
import pandas as pd
import os
from gensim.models import FastText
from gensim.test.utils import common_texts
import openpyxl
import defrazmeka
import defner

patterns = "[A-Za-z0-9!#$%&'()*+,./:;<=>?@[\]^_`{|}~—\"\-]+"
stopwords_ru = stopwords.words("russian")
morph = MorphAnalyzer()
parse_mode = "types.ParseMode.MARKDOWN_V2"
compare_value = 0.5

MAX_FILE_SIZE = 1024 * 1024 * 10


app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
ListOfMessages = []


@app.route('/')
def dafault_route():
    return 'API'


# @app.route('/uploads/<path:path>')
# def send_photo(path):
#     return send_from_directory('uploads', path)


@app.route('/uploadae', methods=['POST'])
@cross_origin()
def uploadae():
    for fname in request.files:
        f = request.files.get(fname)
        print(f)
        milliseconds = int(time.time() * 1000)
        filename = str(milliseconds)
        # f.save('./uploads/%s' % secure_filename(fname))
        full_filename = f"./uploads/{milliseconds}.json"
        f.save(full_filename)
        text = conv.convertJsonMessages2text(full_filename)
        d = {}
        d['text'] = text
        d['filename'] = filename
    return d


@app.route("/get_pattern", methods=['POST'])
def get_pattern():
    msg = request.json
    print(msg)
    data = process_nlp.get_pattern(msg['text'])
    str1 = str(f"Исходный текст: {data['text']} \n\n"
               f"Очищенный текст: {data['remove_all']} \n\n"
               f" Нормальная форма ключевых слов: {data['normal_form']} \n\n"
               f" YakeSummarizer: {data['YakeSummarizer']} \n\n"
               f" BERT_Summarizer: {data['BERT_Summarizer']} \n\n"
               f" Rake_Summarizer: {data['Rake_Summarizer']} \n\n")
    # process_nlp.add_data(data)
    data['print_text'] = str1
    print(str1)
    return data


@app.route("/get_pattern_add", methods=['POST'])
def get_pattern_add():
    msg = request.json
    print(msg)
    data = process_nlp.add_data(msg)
    print()
    print(data)
    return data


@app.route('/findae', methods=['POST'])
def findae():
    #     if request.method == 'POST':
    msg = str(request.json)
    print(msg)
    filename = msg
    data = process_nlp.find_ae(filename)
    print(data)
    return data


@app.route("/clear_db", methods=['GET'])
def clear_db():
    process_nlp.clear_db()
    return "ok clear_db"


@app.route("/load_db", methods=['GET'])
def load_db():
    data = process_nlp.load_db()
    return data


@app.route('/uploadsa', methods=['POST'])
def uploadsa():
    if request.method == 'POST':
        f = request.files['File']
        # filename = secure_filename(f.filename)
        milliseconds = int(time.time() * 1000)
        filename = f"./uploads/{milliseconds}.pcap"
        f.save(filename)
        # text = conv.convertJsonMessages2text(filename)
        # str1 = text
        from scan_detector import all_check
        str1 = all_check(filename)
        print(str1)
        str1 += "<br> <a href=""javascript:history.back()"">Назад</a>"
        return str1


@app.route('/tmodel', methods=['POST'])
def rtmodel():
    data = request.json
    text = data['text']
    topic_num = data['topic_num']
    print(text)
    print(topic_num)
    tmodel(text, topic_num)
    return jsonify("ok"), 200, {'Content-Type': 'application/json'}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
# app.run(host="0.0.0.0")
