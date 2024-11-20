# Importing necessary libraries
import json

import os
import pandas as pd

import re
import openai
from keybert import KeyBERT
from keybert.llm import OpenAI
from keybert import KeyLLM


def load_json(path):
    with open(path, 'r', encoding="utf-8") as fcc_file:
        json_data = json.load(fcc_file)
        return json_data


if __name__ == '__main__':
    # Initializing the Sentence Transformer model using BERT with mean-tokens pooling
    #model = SentenceTransformer('bert-base-nli-mean-tokens')
    local_data_source=['Human', 'Pork', 'Eggs', 'Chicken', 'Beef', 'Fruits', 'Seafood', 'Mutton', 'Vegetable']
    # Create your LLM
    client=openai.OpenAI(api_key="XXXX")
    llm = OpenAI(client)

    # Load it in KeyLLM
    kw_model = KeyLLM(llm)


    # List of global words
    list_gl_words = []
    words_raw=[]
    pmc_list=[]
    url_list=[]
    path_global_data = os.listdir("final_output")
    #path_global_data = path_global_data[:5]
    keybert_model = KeyBERT()
    df=pd.DataFrame()
    for f in path_global_data:
        pp = os.path.join("final_output", f)
        json_data_gl = load_json(pp)
        list_keyphrases=[]
        list_raw_keywords=[]
        # Check if 'isolate_source' exists and handle missing keys
        if "isolate_source" in json_data_gl:
            words_gl = json_data_gl["isolate_source"]
            pmc = json_data_gl["PMCID"]

            url=  json_data_gl["url"]


            word = re.sub(r'[^\w\s]', ' ', str(words_gl))
            list_raw_keywords.append(word)
            key = kw_model.extract_keywords(str(word))
            url_list.append(url)
            pmc_list.append(pmc)
            list_keyphrases.append(key)
            print(word,key)

        else:
            print(f"Warning: 'isolate_source' key not found in {f}")
            url=""
            pmc=""
            list_raw_keywords=[]
            list_keyphrases=[]



        words_raw.extend(list_raw_keywords)

        for obj in list_keyphrases:
            list_gl_words.extend(obj)
    print(len(pmc_list))
    print(len(url_list))
    print(len(words_raw))
    print(len(list_gl_words))

    df['pmc_id'] = pmc_list
    df['url']= url_list
    df['raw_isolate_source'] = words_raw
    df["clean_isolate_source"] = list_gl_words

    df.to_excel("topic_words_sources.xlsx")
