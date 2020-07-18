import requests
import sys
import json
from collections import deque

def pred_save_submit_to_leaderboard(preds, filename):
    output_path = f"./output/{filename}"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("pd\n")
        for p in preds:
            f.write(str(p) + "\n")
    
    submit_results_to_leaderboard(output_path)

def submit_results_to_leaderboard(filepath):
    SUBMISSION_URL = 'http://capstone-leaderboard.centralus.cloudapp.azure.com'

    with open(filepath, 'r') as inputfile:
        alias = inputfile.readline().strip()
        labels = [lbl.strip() for lbl in inputfile]

    req = {
        'netid': "pd10",
        'alias': alias,
        'results': [{
            'error': None,
            'dataset': 'hygiene',
            'results': labels
        }]
    }
    response = requests.post(SUBMISSION_URL + '/api', json=req)
    jdata = response.json()
    if jdata['submission_success'] is not True:
        raise BaseException(jdata)
    else:
        print("Submission completed successfully!")

def get_topic_words(base_topic_words):
    api_url = "https://tuna.thesaurus.com/pageData/"

    confirmed_topic_words = set()
    working_list = deque(base_topic_words)

    while(len(working_list) > 0 and len(confirmed_topic_words) <= 30):
        curr_word = working_list.popleft()
        word_data = requests.get(api_url + curr_word).json()

        try:
            rel_words = _get_related_words(word_data["data"]["definitionData"]["definitions"][0])
        except:
            rel_words = []

        for w in rel_words:
            if w not in confirmed_topic_words:
                working_list.append(w)
        
        confirmed_topic_words.add(curr_word)
    
    return confirmed_topic_words

def _get_related_words(word_def):
    synonyms = {syn["term"] for syn in word_def["synonyms"] if int(syn["similarity"]) >= 50}
    antonyms = {ant["term"] for ant in word_def["antonyms"]}

    return synonyms.union(antonyms)