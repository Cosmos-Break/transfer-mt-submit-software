from flask import Flask, render_template, request, url_for, redirect
from torch import device
from werkzeug.utils import secure_filename
# from generate import generate
# from train import train
import os, subprocess
import torch

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'

@app.route('/',methods=['GET','POST'])
def navi():
    if request.method == 'POST':
        operation = request.values.get('operation')
        if operation == 'upload':
            return redirect(url_for('upload'))
        elif operation == 'train':
            return redirect(url_for('train'))
        elif operation == 'download':
            return redirect(url_for('download'))
    else:
        return render_template('navi.html')

@app.route('/download',methods=['GET', 'POST'])
def download():
    if request.method == 'POST':
        lang = request.values.get('language')
        print(lang)
        if not lang:
            return '请选择语种'
        subprocess.Popen(f'python3 predownload.py {lang} > download_log 2>&1', shell=True)
        return redirect(url_for('download_log'))
    else:
        return render_template('download.html')
        

@app.route('/download_log',methods=['GET'])
def download_log():
    with open('download_log') as f:
        x = f.read().split('\n')
    return render_template("download_log.html", x=x)

@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        lang = request.values.get('language')
        print(lang)
        if not lang:
            return '请选择语种'
        print(request.files)
        if 'file_train_lang' in request.files:
            f = request.files['file_train_lang']
            f.save(secure_filename(f'{lang}-en-data/train.{lang}'))
        elif 'file_val_lang' in request.files:
            f = request.files['file_val_lang']
            f.save(secure_filename(f'{lang}-en-data/val.{lang}'))
        elif 'file_test_lang' in request.files:
            f = request.files['file_test_lang']
            f.save(secure_filename(f'{lang}-en-data/test.{lang}'))
        elif 'file_train_en' in request.files:
            f = request.files['file_train_en']
            f.save(secure_filename(f'{lang}-en-data/train.en'))
        elif 'file_val_en' in request.files:
            f = request.files['file_val_en']
            f.save(secure_filename(f'{lang}-en-data/val.en'))
        elif 'file_test_en' in request.files:
            f = request.files['file_test_en']
            f.save(secure_filename(f'{lang}-en-data/test.en'))
        return render_template('upload.html')
    else:
        return render_template('upload.html')

@app.route('/train',methods=['GET','POST'])
def train():
    if request.method == 'POST':
        # 选择语种
        lang = request.values.get('language')
        print(lang)
        if not lang:
            return '请选择语种'
        
        # 选择cpu还是gpu
        cpu_or_gpu = request.values.get('cpu_or_gpu')
        print(cpu_or_gpu)
        device = torch.device('cpu')
        if cpu_or_gpu == 'gpu':
            device = 'cuda'
        
        # 选择训练还是测试
        train_or_test = request.values.get('train_or_test')
        if train_or_test == 'train':
            subprocess.Popen(f'python3 train.py {lang} {device} > log 2>&1', shell=True)
            return redirect(url_for('train_log'))
            
        elif train_or_test == 'test':
            # subprocess.run(f'python3 generate.py {lang} {device}', shell=True)
            with open('result_text.txt', 'r') as f:
                x = f.read().split('\n')
            return render_template("test_log.html", x=x)
    else:
        return render_template('train.html')

@app.route('/train_log',methods=['GET'])
def train_log():
    with open('log') as f:
        x = f.read().split('\n')
    return render_template("train_log.html", x=x)

if __name__ == '__main__':
   app.run(debug=True)