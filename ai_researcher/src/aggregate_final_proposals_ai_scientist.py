

# Load all json files in the directory
import json
import os

# Process ai-researcher proposals

def load_json_files(directory):
    json_objects = []
    for file in os.listdir(directory):
        if file.endswith(".json"):
            with open(directory + file) as f:
                json_objects.append((file, json.load(f)))
    return json_objects

conference = 'acl'

# Load acl_id_map.json
with open(f'../{conference}_id_map.json') as f:
    conference_id_map = json.load(f)

import tqdm
for topic, value in tqdm.tqdm(conference_id_map.items(), desc='topics'):
    cache_name = topic
    arxiv_id = value[0]

    json_objects = load_json_files(f"../experiment_result/ai_scientist_all_data/{conference}_output_plans/{arxiv_id}_ideas_ai_scientist/")

    proposals = {
        'target_paper': '',
        'ideas': []
    }
    for name, json_object in tqdm.tqdm(json_objects, desc=cache_name):
        print(name)
        if len(list(json_object['full_experiment_plan'].values())) > 1 and 'Problem Statement' in json_object['full_experiment_plan'] and 'Motivation' in json_object['full_experiment_plan'] and 'Proposed Method' in json_object['full_experiment_plan'] and 'Step-by-Step Experiment Plan' in json_object['full_experiment_plan']:
            idea_dict = {
                'generated_by': 'ai_scientist',
                'Type': 'prompting',
                'Problem': json_object['full_experiment_plan']['Problem Statement'],
                'Motivation': json_object['full_experiment_plan']['Motivation'],
                'Proposed Method': json_object['full_experiment_plan']['Proposed Method'],
                'Experiment Plan': json_object['full_experiment_plan']['Step-by-Step Experiment Plan'],
            }
        else:
            idea_dict = {
                'generated_by': 'ai_scientist',
                'Type': 'prompting',
                'Problem': list(json_object['full_experiment_plan'].values())[0]['Problem Statement'],
                'Motivation': list(json_object['full_experiment_plan'].values())[0]['Motivation'],
                'Proposed Method': list(json_object['full_experiment_plan'].values())[0]['Proposed Method'],
                'Experiment Plan': list(json_object['full_experiment_plan'].values())[0]['Step-by-Step Experiment Plan'],
            }
        proposals['ideas'].append(idea_dict)

    # Create directory f'../cache_results_test/final_proposals/{cache_name}
    os.makedirs(f'../cache_results_test/final_proposals/{cache_name}', exist_ok=True)
    with open(f'../cache_results_test/final_proposals/{cache_name}/ai_scientist.json', 'w') as f:
        json.dump(proposals, f, indent=4)