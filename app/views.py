import datetime
import json

import requests
from flask import render_template, redirect, request
import xml.etree.ElementTree as ET

from app import app

# The node with which our application interacts, there can be multiple
# such nodes as well.
URL_CURR = "http://www.cbr.ru/scripts/XML_daily.asp"

posts = []


@app.route('/')
def index():
    cur_ans_dict = {}  
    data = requests.get(URL_CURR)
    tree = ET.fromstring(data.text)
    data_date = tree.attrib[tree.keys()[0]]
    for element in tree.findall("Valute"):  
         name = element.find("Name")
         course = element.find("Value")
         code = element.find("CharCode")
         nominal = element.find("Nominal")
         cur_ans_dict[name.text] = [nominal.text, course.text, code.text]
    return render_template('index.html',
                           title='Курсы валют ЦБ',
                           book=cur_ans_dict,
                           node_address=URL_CURR,
                           date = data_date)
                           




@app.route('/submit')
def get_date():
    cur_ans_dict = {}
    date_req = request.args.get('date_req')
    data = requests.get(URL_CURR + "?date_req=" + date_req[-2:] + "/" + date_req[5:7]+"/" + date_req[:4])
    print(URL_CURR + "?date_req=" + date_req[-2:] + "/" + date_req[5:7]+"/" + date_req[:4] + " ----" + date_req)
    tree = ET.fromstring(data.text)
    data_date = tree.attrib[tree.keys()[0]]
    for element in tree.findall("Valute"):  
         name = element.find("Name")
         course = element.find("Value")
         code = element.find("CharCode")
         nominal = element.find("Nominal")
         cur_ans_dict[name.text] = [nominal.text, course.text, code.text]
    return render_template('index.html',
                           title='Курсы валют ЦБ',
                           book=cur_ans_dict,
                           node_address=URL_CURR,
                           date = data_date)