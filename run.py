import subprocess
lang = 'my'
# Baseline
# subprocess.run(f'python _token_matching_random_all_emb.py {lang}', shell=True)
# subprocess.run(f'python _concat_emb.py {lang}-fasttext-model.vec_underline_token_match_random_all_emb > en-{lang}-concat-emb', shell=True)
# subprocess.run(f'python _change_NMT_embedding.py en-{lang}-concat-emb', shell=True)

# MI-PC
# subprocess.run(f'python _token_matching.py {lang}', shell=True)
# subprocess.run(f'python _concat_emb.py {lang}-fasttext-model.vec_underline_token_match > en-{lang}-concat-emb', shell=True)
# subprocess.run(f'python _change_NMT_embedding.py en-{lang}-concat-emb', shell=True)

# Top-1-PC
# subprocess.run(f'python _token_matching-dic-avg-emb.py {lang}', shell=True)
# subprocess.run(f'python _concat_emb.py {lang}-fasttext-model.vec_underline_token_match_and_dic_avg > en-{lang}-concat-emb', shell=True)
# subprocess.run(f'python _change_NMT_embedding.py en-{lang}-concat-emb', shell=True)

# Mean-PC
subprocess.run(f'python _token_matching-dic-avg-emb_all.py {lang}', shell=True)
subprocess.run(f'python _concat_emb.py {lang}-fasttext-model.vec_underline_token_match_and_dic_avg > en-{lang}-concat-emb', shell=True)
subprocess.run(f'python _change_NMT_embedding.py en-{lang}-concat-emb', shell=True)

# train
# subprocess.run(f'python -u train.py {lang}', shell=True)
