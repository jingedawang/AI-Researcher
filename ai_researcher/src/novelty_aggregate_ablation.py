import os
import json


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

conferences = ['acl', 'iclr', 'hfdaily', 'cvpr']
# Load conference_id_map.json
acl_id_map = json.load(open('../acl_id_map.json'))
iclr_id_map = json.load(open('../iclr_id_map.json'))
hfdaily_id_map = json.load(open('../hfdaily_id_map.json'))
cvpr_id_map = json.load(open('../cvpr_id_map.json'))
# Combine the id maps
conference_id_maps = {**acl_id_map, **iclr_id_map, **hfdaily_id_map, **cvpr_id_map}
# conference_id_maps = {**acl_id_map, **hfdaily_id_map, **cvpr_id_map}

# Load filtered_id_maps.json
filtered_id_maps = json.load(open('../filtered_id_maps.json'))
# Filter the conference_id_maps to contain only the topics in the filtered_id_maps
id_maps = {}
for topic, value in filtered_id_maps.items():
    if topic in conference_id_maps:
        id_maps[topic] = conference_id_maps[topic]


topic_novelty = {}
# Get all the files in the project_proposals directory
proposals_dir = '../experiment_result/ours_v2_ablation/without_plan_but_retrieve'
for topic, value in id_maps.items():
    arxiv_id = value[0]
    conference = topic.split('_', 1)[0]
    if conference == 'topic':
        conference = 'acl'

    topic_novelty[topic] = {
        'step_0': {
            'count': 0,
            'novel_count': 0
        },
        'step_1': {
            'count': 0,
            'novel_count': 0
        },
        'step_2': {
            'count': 0,
            'novel_count': 0
        },
        'step_3': {
            'count': 0,
            'novel_count': 0
        }
    }

    for step in ['step_0', 'step_1', 'step_2', 'step_3']:
        ours_proposals = load_json_files(f'{proposals_dir}/{conference}/{arxiv_id}/{step}_final_proposal_wi_method_decom_v2/')
        if ours_proposals and len(ours_proposals) > 0:
            for filename, proposal_object in ours_proposals:
                if 'novelty' not in proposal_object:
                    print(f'Novelty not found in {topic}/{filename}')
                    continue
                topic_novelty[topic][step]['count'] += 1
                if proposal_object['novelty'] == 'yes':
                    topic_novelty[topic][step]['novel_count'] += 1
            if topic_novelty[topic][step]['count'] > 0:
                topic_novelty[topic][step]['novel_ratio'] = topic_novelty[topic][step]['novel_count'] / topic_novelty[topic][step]['count']
            else:
                topic_novelty[topic][step]['novel_ratio'] = 0
        else:
            print(f'No proposals found in {proposals_dir}/{conference}/{arxiv_id}/{step}_final_proposal_wi_method_decom_v2/')

with open('../novelty_ablation_summary_without_plan_but_retrieve.json', 'w') as f:
    json.dump(topic_novelty, f, indent=4)

novel_count_for_each_step = {
    'step_0': 0,
    'step_1': 0,
    'step_2': 0,
    'step_3': 0
}
novel_ratio_for_each_step = {
    'step_0': 0,
    'step_1': 0,
    'step_2': 0,
    'step_3': 0
}

available_topics = 0
for topic, value in topic_novelty.items():
    if value['step_0']['count'] > 0 and value['step_1']['count'] > 0 and value['step_2']['count'] > 0 and value['step_3']['count'] > 0:
        novel_count_for_each_step['step_0'] += value['step_0']['novel_count']
        novel_count_for_each_step['step_1'] += value['step_1']['novel_count']
        novel_count_for_each_step['step_2'] += value['step_2']['novel_count']
        novel_count_for_each_step['step_3'] += value['step_3']['novel_count']
        novel_ratio_for_each_step['step_0'] += value['step_0']['novel_ratio']
        novel_ratio_for_each_step['step_1'] += value['step_1']['novel_ratio']
        novel_ratio_for_each_step['step_2'] += value['step_2']['novel_ratio']
        novel_ratio_for_each_step['step_3'] += value['step_3']['novel_ratio']
        available_topics += 1
    else:
        print(f'Novelty results not completed for {topic}')

novel_count_for_each_step['step_0'] /= available_topics
novel_count_for_each_step['step_1'] /= available_topics
novel_count_for_each_step['step_2'] /= available_topics
novel_count_for_each_step['step_3'] /= available_topics
novel_ratio_for_each_step['step_0'] /= available_topics
novel_ratio_for_each_step['step_1'] /= available_topics
novel_ratio_for_each_step['step_2'] /= available_topics
novel_ratio_for_each_step['step_3'] /= available_topics

print(f'Average novelty count for each step: {novel_count_for_each_step}')
print(f'Average novelty ratio for each step: {novel_ratio_for_each_step}')