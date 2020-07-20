import requests
import sys
import numpy as np

def pred_save_submit_to_leaderboard(preds, filename):
    output_path = f"./output/{filename}"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("pd")
        for p in preds:
            f.write("\n" + str(p))
    
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


def calculate_f1_score(predicted_labels, actual_labels):
    pos_mask = predicted_labels[predicted_labels == 1]
    rec_mask = actual_labels[actual_labels == 1]
    precision = np.sum(actual_labels[pos_mask]) / len(predicted_labels[pos_mask])
    recall = np.sum(predicted_labels[rec_mask]) / len(actual_labels[rec_mask])

    return 2 * precision * recall / (precision + recall)