#!/usr/bin/env python
# coding: utf-8
import os, gzip, csv, sys, time, logging
from easynmt import util, EasyNMT
import pandas as pd
import numpy as np
import nltk

nli_dataset_path = '/workspace/data/NLI/AllNLI.tsv.gz'
target_lang = "fr"
nli_translated_dataset_path = '/workspace/data/NLI/AllNLI_%s.tsv.gz' %target_lang
nb_pairs_max = 1e8

if __name__ == '__main__':
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
        stream=sys.stdout,
    )
    nltk.download('punkt')
    model = EasyNMT('opus-mt')

    data = []
    # Download datasets if needed
    if not os.path.exists(nli_dataset_path):
        util.http_get('https://sbert.net/datasets/AllNLI.tsv.gz', nli_dataset_path)
    with gzip.open(nli_dataset_path, 'rt', encoding='utf8') as fIn:
        reader = csv.DictReader(fIn, delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in reader:
            if len(data) > nb_pairs_max:
                break
            data.append(row)

    sentences_df = pd.DataFrame(data[1:], columns=data[1])
    print(sentences_df.head())

    # To translate the set of the unique sentences, get unique :
    all_sentences = sentences_df[['sentence1','sentence2']].to_numpy().flatten()
    unique_sentences, indices = np.unique(all_sentences, return_inverse=True)
    #indices = np.unravel_index(indices, (2,sentences_df.shape[0]))
    print("Number of pairs : %s"% sentences_df.shape[0])
    print("Unique sentences : %s"% len(unique_sentences))

    ######## Multi-Process-Translation
    # You can pass a target_devices parameter to the start_multi_process_pool() method to define how many processes to start
    # and on which devices the processes should run
    process_pool = model.start_multi_process_pool()


    #Do some warm-up
    model.translate_multi_process(process_pool, unique_sentences[0:100], source_lang='en', target_lang=target_lang, show_progress_bar=False)

    # Start translation speed measure - Multi process
    start_time = time.time()
    translations_multi_p = model.translate_multi_process(process_pool, unique_sentences, source_lang='en', target_lang=target_lang, show_progress_bar=True)
    end_time = time.time()
    print("Multi-Process translation done after {:.2f} sec. {:.2f} sentences / second".format(end_time - start_time, len(unique_sentences) / (end_time - start_time)))
    model.stop_multi_process_pool(process_pool)

    # Rebuild translated sentences inside the dataframe
    sentences_df[['sentence1_translated', 'sentence2_translated']] = np.array(translations_multi_p)[indices].reshape((sentences_df.shape[0], 2))

    # Save the compressed csv
    sentences_df[['split','dataset','filename','sentence1_translated', 'sentence2_translated','label']].to_csv(nli_translated_dataset_path, compression='gzip', sep='\t',index=False)
