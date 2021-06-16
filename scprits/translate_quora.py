#!/usr/bin/env python
# coding: utf-8
import os, gzip, csv, sys, time, logging, json
from easynmt import util, EasyNMT

#from easynmt import EasyNMT
import pandas as pd
import numpy as np
from collections import defaultdict
import nltk
from itertools import islice
import json

source_file = '/workspace/data/Quora/quora_duplicate_questions.tsv'
target_lang = "fr"
quora_translated_dataset_path = '/workspace/data/Quora/quora_duplicate_questions_%s.tsv' %target_lang

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
        stream=sys.stdout,
    )
    nltk.download('punkt')
    model = EasyNMT('opus-mt')

    if not os.path.exists(source_file):
        print("Download file to", source_file)
        util.http_get('http://qim.fs.quoracdn.net/quora_duplicate_questions.tsv', source_file)


    #Read pairwise file
    sentences = {}
    duplicates = defaultdict(lambda: defaultdict(bool))
    rows = []
    with open(source_file, encoding='utf8') as fIn:
        reader = csv.DictReader(fIn, delimiter='\t', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            id1 = row['qid1']
            id2 = row['qid2']
            question1 = row['question1'].replace("\r", "").replace("\n", " ").replace("\t", " ")
            question2 = row['question2'].replace("\r", "").replace("\n", " ").replace("\t", " ")
            is_duplicate = row['is_duplicate']
            if question1 == "" or question2 == "":
                continue
            sentences[id1] = question1
            sentences[id2] = question2

            rows.append({'qid1': int(id1), 'qid2': int(id2), 'question1': question1, 'question2': question2, 'is_duplicate': is_duplicate})


    #indices = np.unravel_index(indices, (2,sentences_df.shape[0]))
    print("Unique sentences : %s"% len(sentences))

    ######## Multi-Process-Translation
    # You can pass a target_devices parameter to the start_multi_process_pool() method to define how many processes to start
    # and on which devices the processes should run
    process_pool = model.start_multi_process_pool()


    #Do some warm-up
    model.translate_multi_process(process_pool, list(sentences.values())[0:100], source_lang='en', target_lang=target_lang, show_progress_bar=False)

    def chunks(data, SIZE=10000):
       it = iter(data)
       for i in range(0, len(data), SIZE):
          yield {k:data[k] for k in islice(it, SIZE)}
    # Start translation speed measure - Multi process
    start_time = time.time()
    i = 0
    for sentences_to_trans in  chunks(sentences, 1000):
        print("Chunk %s"%i)
        translations_multi_p = model.translate_multi_process(process_pool,list(sentences_to_trans.values()) , source_lang='en', target_lang=target_lang, show_progress_bar=True)
        sentences_translated = {k: s for ((k,v), s) in zip(sentences_to_trans.items(), translations_multi_p)}
        with open('/workspace/data/Quora/tmp/%s.json'%i, 'w') as f:
            json.dump(sentences_translated, f)
        i += 1
    end_time = time.time()
    print("Multi-Process translation done after {:.2f} sec. {:.2f} sentences / second".format(end_time - start_time, len(list(sentences.values())) / (end_time - start_time)))
    model.stop_multi_process_pool(process_pool)
    # Start translation speed measure - Multi process
    # Start translation speed measure - Multi process
    #start_time = time.time()
    #translations_multi_p = model.translate_multi_process(process_pool, list(sentences.values()), source_lang='en', target_lang=target_lang, show_progress_bar=True)
    #end_time = time.time()
    #print("Multi-Process translation done after {:.2f} sec. {:.2f} sentences / second".format(end_time - start_time, len(list(sentences.values())) / (end_time - start_time)))
    #model.stop_multi_process_pool(process_pool)
    # Build original dict translated
    #sentences_translated = {int(k): s for ((k,v), s) in zip(sentences.items(), translations_multi_p)}
    # build table with translated sentences
    #sentences_df = pd.DataFrame(rows, columns=['qid1','qid2','question1','question2','is_duplicate'])
    #sentences_df['question1_translated'] = sentences_df['qid1'].map(sentences_translated)
    #sentences_df['question2_translated'] = sentences_df['qid2'].map(sentences_translated)    # Save the compressed csv
    #sentences_df.to_csv(quora_translated_dataset_path, sep = '\t', index=True)
