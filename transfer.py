import subprocess
import sys
lang = sys.argv[1]

# eflomal alignment
import nltk
import string
punc = string.punctuation
nltk.download('punkt')
from nltk.tokenize import word_tokenize
L1, L2 = [], []
for line, line2 in zip(open(f'{lang}-en-data/train.en'), open(f'{lang}-en-data/train.{lang}')):
    if line == '\n' or line2 == '\n':
        continue
    L1.append(line.strip())
    L2.append(line2.strip())
    
# generate eflomal format data
with open(f'eflomal_data.{lang}-en', 'w') as f:
    for l1, l2 in zip(L1, L2):
        l1 = word_tokenize(l1)
        l1 = ' '.join(l1)
        l2 = word_tokenize(l2)
        l2 = ' '.join(l2)
        f.write(l2 + ' ||| ' + l1 + '\n')

subprocess.run(f'python eflomal/align.py -i eflomal_data.{lang}-en --model 3 -f {lang}-en.fwd -r {lang}-en.rev', shell=True)
subprocess.run(f'./atools -c grow-diag-final-and -i {lang}-en.fwd -j {lang}-en.rev > {lang}-en.sym', shell=True)

# generate bilingual dic
subprocess.run(f'python _get_eflomal_dic.py {lang}', shell=True)
subprocess.run(f'python _get_eflomal_dic_all.py {lang}', shell=True)

# generate dummy embedding
subprocess.run(f'python _generate_dummy_embedding_underline.py {lang}', shell=True)

# choose one embedding transfer
# Mean-PC
subprocess.run(f'python _token_matching-dic-avg-emb_all.py {lang}', shell=True)
subprocess.run(f'python _concat_emb.py {lang}-fasttext-model.vec_underline_token_match_and_dic_avg > en-{lang}-concat-emb', shell=True)
subprocess.run(f'python _change_NMT_embedding.py en-{lang}-concat-emb', shell=True)