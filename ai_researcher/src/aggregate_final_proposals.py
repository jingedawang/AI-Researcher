

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

# Load acl_id_map.json
with open(f'../acl_id_map.json') as f:
    acl_id_map = json.load(f)

import tqdm
for topic, value in tqdm.tqdm(acl_id_map.items(), desc='topics'):
    cache_name = topic
    arxiv_id = value[1]

    json_objects = load_json_files(f"../cache_results_test/project_proposals/{cache_name}/")

    proposals = {
        'target_paper': json_objects[0][1]['topic_description'].split('.', 1)[0],
        'ideas': []
    }
    for name, json_object in tqdm.tqdm(json_objects, desc=cache_name):
        print(name)
        if len(list(json_object['full_experiment_plan'].values())) > 1 and 'Problem Statement' in json_object['full_experiment_plan'] and 'Motivation' in json_object['full_experiment_plan'] and 'Proposed Method' in json_object['full_experiment_plan'] and 'Step-by-Step Experiment Plan' in json_object['full_experiment_plan']:
            idea_dict = {
                'generated_by': 'ai_researcher',
                'Type': 'prompting',
                'Problem': json_object['full_experiment_plan']['Problem Statement'],
                'Motivation': json_object['full_experiment_plan']['Motivation'],
                'Proposed Method': json_object['full_experiment_plan']['Proposed Method'],
                'Experiment Plan': json_object['full_experiment_plan']['Step-by-Step Experiment Plan'],
            }
        else:
            idea_dict = {
                'generated_by': 'ai_researcher',
                'Type': 'prompting',
                'Problem': list(json_object['full_experiment_plan'].values())[0]['Problem Statement'],
                'Motivation': list(json_object['full_experiment_plan'].values())[0]['Motivation'],
                'Proposed Method': list(json_object['full_experiment_plan'].values())[0]['Proposed Method'],
                'Experiment Plan': list(json_object['full_experiment_plan'].values())[0]['Step-by-Step Experiment Plan'],
            }
        proposals['ideas'].append(idea_dict)

    # Create directory f'../cache_results_test/final_proposals/{cache_name}
    os.makedirs(f'../cache_results_test/final_proposals/{cache_name}', exist_ok=True)
    with open(f'../cache_results_test/final_proposals/{cache_name}/ai_researcher.json', 'w') as f:
        json.dump(proposals, f, indent=4)

    arxid_id = '2304.11406'
    # Process our proposals
    json_objects = load_json_files(f"../experiment_result/project_proposals/{arxid_id}/")
    proposals = {
        'target_paper': '',
        'ideas': []
    }
    import tqdm
    for name, json_object in tqdm.tqdm(json_objects, desc=arxid_id):
        print(name)
        # print(json_object)
        if len(list(json_object['final_proposal']['final_proposal'].values())) > 1 and 'Problem Statement' in json_object['final_proposal']['final_proposal'] and 'Motivation' in json_object['final_proposal']['final_proposal'] and 'Proposed Method' in json_object['final_proposal']['final_proposal'] and 'Step-by-Step Experiment Plan' in json_object['final_proposal']['final_proposal']:
            idea_dict = {
                'generated_by': 'ours',
                'Type': 'prompting',
                'Problem': json_object['final_proposal']['final_proposal']['Problem Statement'],
                'Motivation': json_object['final_proposal']['final_proposal']['Motivation'],
                'Proposed Method': json_object['final_proposal']['final_proposal']['Proposed Method'],
                'Experiment Plan': json_object['final_proposal']['final_proposal']['Step-by-Step Experiment Plan'],
            }
        else:
            idea_dict = {
                'generated_by': 'ours',
                'Type': 'prompting',
                'Problem': list(json_object['final_proposal']['final_proposal'].values())[0]['Problem Statement'],
                'Motivation': list(json_object['final_proposal']['final_proposal'].values())[0]['Motivation'],
                'Proposed Method': list(json_object['final_proposal']['final_proposal'].values())[0]['Proposed Method'],
                'Experiment Plan': list(json_object['final_proposal']['final_proposal'].values())[0]['Step-by-Step Experiment Plan'],
            }
        proposals['ideas'].append(idea_dict)

    with open(f'../cache_results_test/final_proposals/{cache_name}/ours.json', 'w') as f:
        json.dump(proposals, f, indent=4)