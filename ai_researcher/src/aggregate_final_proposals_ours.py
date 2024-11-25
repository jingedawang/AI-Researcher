

# Load all json files in the directory
import json
import os

# Process ai-researcher proposals

def load_json_files(directory):
    if not os.path.exists(directory):
        return None
    json_objects = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            with open(directory + file) as f:
                json_objects.append((file, json.load(f)))
    return json_objects

import tqdm

def process_proposals(cache_name, arxiv_id, conference):
    # Process our proposals
    json_objects = load_json_files(f"../experiment_result/project_proposals_20240928_original_faiss_55_all/{conference}/{arxiv_id}/step_3_final_proposal_wi_method_decom/")
    if not json_objects:
        print(f'No proposals found for {arxiv_id}')
        return
    proposals = {
        'target_paper': '',
        'ideas': []
    }
    for name, json_object in tqdm.tqdm(json_objects, desc=arxiv_id):
        # print(json_object['final_proposal'])
        if json_object and 'final_proposal' in json_object and json_object['final_proposal'] and 'final_proposal' in json_object['final_proposal'] and json_object['final_proposal']['final_proposal']:
            if len(list(json_object['final_proposal']['final_proposal'].keys())) == 1:
                print(f'Found len 1 in {arxiv_id}/{name}')
                exit()
        if json_object and 'final_proposal' in json_object and json_object['final_proposal'] and 'final_proposal' in json_object['final_proposal'] and json_object['final_proposal']['final_proposal'] and 'Problem Statement' in json_object['final_proposal']['final_proposal'] and 'Motivation' in json_object['final_proposal']['final_proposal'] and 'Proposed Method' in json_object['final_proposal']['final_proposal'] and 'Step-by-Step Experiment Plan' in json_object['final_proposal']['final_proposal']:
            idea_dict = {
                'generated_by': 'ours',
                'Type': 'prompting',
                'Problem': json_object['final_proposal']['final_proposal']['Problem Statement'],
                'Motivation': json_object['final_proposal']['final_proposal']['Motivation'],
                'Proposed Method': json_object['final_proposal']['final_proposal']['Proposed Method'],
                'Experiment Plan': json_object['final_proposal']['final_proposal']['Step-by-Step Experiment Plan'],
            }
            proposals['ideas'].append(idea_dict)
        else:
            print(f'final_proposal not found in {arxiv_id}/{name}')

    with open(f'../cache_results_test/final_proposals/{cache_name}/ours.json', 'w') as f:
        json.dump(proposals, f, indent=4)


conference = 'iclr'
# Load acl_id_map.json
with open(f'../{conference}_id_map.json') as f:
    conference_id_map = json.load(f)


for topic, value in conference_id_map.items():
    cache_name = topic
    arxiv_id = value[0]
    process_proposals(cache_name, arxiv_id, conference)