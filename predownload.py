# choose language
import sys
lang = sys.argv[1]
wiki_directory = 'train'
import sentencepiece as spm
import os
import subprocess

# download Helsinki-NLP/opus-mt-de-en(need git lfs) and extract embedding.
subprocess.run(f'git lfs install', shell=True)
subprocess.run(f'pip3 install -r requirements/requirements_model.txt', shell=True)
subprocess.run(f'git clone https://huggingface.co/Helsinki-NLP/opus-mt-de-en', shell=True)
subprocess.run(f'python _download_huggingface_mt_model.py', shell=True)

# download wikidump
if not os.path.exists(f'{lang}wiki-latest-pages-articles.xml.bz2'):
    subprocess.run(f'rm {lang}wiki-latest-pages-articles.xml.bz2', shell=True)
    subprocess.run(f'wget --no-check-certificate https://dumps.wikimedia.org/{lang}wiki/latest/{lang}wiki-latest-pages-articles.xml.bz2', shell=True)
    subprocess.run(f'python -m wikiextractor.WikiExtractor -b 1024M -o wiki_data {lang}wiki-latest-pages-articles.xml.bz2', shell=True)
    subprocess.run(f'mkdir {wiki_directory}', shell=True)
    subprocess.run(f'cp wiki_data/AA/wiki_00 train/train.{lang}', shell=True)


# train sentencePiece tokenzier
source_input_path = os.path.join(wiki_directory, f'train.{lang}')
print(source_input_path)
subprocess.run(f'mkdir {lang}-tokenizer', shell=True)
spm.SentencePieceTrainer.train(f'--input={source_input_path} --model_prefix={lang}-tokenizer/spm --vocab_size=50000 --character_coverage=1.0 --hard_vocab_limit=false')

