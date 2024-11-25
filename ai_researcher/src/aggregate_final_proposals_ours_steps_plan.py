

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

def process_proposals(cache_name, arxiv_id, conference, step):
    step_alias = f'{step}_without_plan_and_retrieve'
    # Process our proposals
    json_objects = load_json_files(f"../experiment_result/ours_v2_ablation/without_plan_and_retrieve/{conference}/{arxiv_id}/{step}_final_proposal_wi_method_decom_v2/")
    if not json_objects:
        print(f'No proposals found for {cache_name}/{step}')
        return
    proposals = {
        'target_paper': '',
        'ideas': []
    }
    for name, json_object in tqdm.tqdm(json_objects, desc=cache_name):
        # print(json_object['final_proposal'])
        if json_object and 'final_proposal' in json_object and json_object['final_proposal'] and 'final_proposal' in json_object['final_proposal'] and json_object['final_proposal']['final_proposal']:
            if len(list(json_object['final_proposal']['final_proposal'].keys())) == 1:
                print(f'Found len 1 in {arxiv_id}/{name}')
                exit()
        if json_object and 'final_proposal' in json_object and json_object['final_proposal'] and 'final_proposal' in json_object['final_proposal'] and json_object['final_proposal']['final_proposal'] and 'Problem Statement' in json_object['final_proposal']['final_proposal'] and 'Motivation' in json_object['final_proposal']['final_proposal'] and 'Proposed Method' in json_object['final_proposal']['final_proposal'] and 'Step-by-Step Experiment Plan' in json_object['final_proposal']['final_proposal']:
            idea_dict = {
                'generated_by': step_alias,
                'Type': 'prompting',
                'Problem': json_object['final_proposal']['final_proposal']['Problem Statement'],
                'Motivation': json_object['final_proposal']['final_proposal']['Motivation'],
                'Proposed Method': json_object['final_proposal']['final_proposal']['Proposed Method'],
                'Experiment Plan': json_object['final_proposal']['final_proposal']['Step-by-Step Experiment Plan'],
            }
            proposals['ideas'].append(idea_dict)
        else:
            print(f'final_proposal not found in {arxiv_id}/{name}')

    with open(f'../cache_results_test/final_proposals/{cache_name}/{step_alias}.json', 'w') as f:
        json.dump(proposals, f, indent=4)


with open(f'../filtered_id_maps.json') as f:
    id_map = json.load(f)

for step in ['step_0', 'step_1', 'step_2', 'step_3']:
    for topic, value in id_map.items():
        conference = topic.split('_')[0]
        if conference == 'topic':
            conference = 'acl'

        cache_name = topic
        arxiv_id = value[0]
        process_proposals(cache_name, arxiv_id, conference, step)