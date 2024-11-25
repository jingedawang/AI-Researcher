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


topic_novelty = {}
# Get all the files in the project_proposals directory
ai_researcher_proposals_dir = '../cache_results_test/project_proposals_20240928_original_faiss_55_all/'
ours_proposals_dir = '../experiment_result/project_proposals_20240928_original_faiss_55_all'
for topic, value in conference_id_maps.items():
    arxiv_id = value[0]
    conference = topic.split('_', 1)[0]
    if conference == 'topic':
        conference = 'acl'

    topic_novelty[topic] = {
        'ours': {
            'count': 0,
            'novel_count': 0
        },
        'ai_researcher': {
            'count': 0,
            'novel_count': 0
        }
    }
    ai_researcher_proposals = load_json_files(f'{ai_researcher_proposals_dir}/{topic}/')
    if ai_researcher_proposals and len(ai_researcher_proposals) > 0:
        for filename, proposal_object in ai_researcher_proposals:
            if 'novelty' not in proposal_object:
                print(f'Novelty not found in {topic}/{filename}')
                continue
            topic_novelty[topic]['ai_researcher']['count'] += 1
            if proposal_object['novelty'] == 'yes':
                topic_novelty[topic]['ai_researcher']['novel_count'] += 1
        if topic_novelty[topic]['ai_researcher']['count'] > 0:
            topic_novelty[topic]['ai_researcher']['novel_ratio'] = topic_novelty[topic]['ai_researcher']['novel_count'] / topic_novelty[topic]['ai_researcher']['count']
        else:
            topic_novelty[topic]['ai_researcher']['novel_ratio'] = 0
    
    ours_proposals = load_json_files(f'{ours_proposals_dir}/{conference}/{arxiv_id}/step_3_final_proposal_wi_method_decom/')
    if ours_proposals and len(ours_proposals) > 0:
        for filename, proposal_object in ours_proposals:
            if 'novelty' not in proposal_object:
                print(f'Novelty not found in {topic}/{filename}')
                continue
            topic_novelty[topic]['ours']['count'] += 1
            if proposal_object['novelty'] == 'yes':
                topic_novelty[topic]['ours']['novel_count'] += 1
        if topic_novelty[topic]['ours']['count'] > 0:
            topic_novelty[topic]['ours']['novel_ratio'] = topic_novelty[topic]['ours']['novel_count'] / topic_novelty[topic]['ours']['count']
        else:
            topic_novelty[topic]['ours']['novel_ratio'] = 0
    else:
        print(f'No proposals found in {ours_proposals_dir}/{conference}/{arxiv_id}/step_3_final_proposal_wi_method_decom/')

with open('../novelty_summary.json', 'w') as f:
    json.dump(topic_novelty, f, indent=4)

available_topics = 0
ours_novel_count = 0
ai_researcher_novel_count = 0
ours_count_win_count = 0
ai_researcher_count_win_count = 0
count_tie_count = 0
ours_ratio_win_count = 0
ai_researcher_ratio_win_count = 0
ratio_tie_count = 0
for topic, value in topic_novelty.items():
    if value['ours']['count'] > 0 and value['ai_researcher']['count'] > 0:
        available_topics += 1
        ours_novel_count += value['ours']['novel_count']
        ai_researcher_novel_count += value['ai_researcher']['novel_count']
        if value['ours']['novel_ratio'] > value['ai_researcher']['novel_ratio']:
            ours_ratio_win_count += 1
        elif value['ours']['novel_ratio'] < value['ai_researcher']['novel_ratio']:
            ai_researcher_ratio_win_count += 1
        else:
            ratio_tie_count += 1
        if value['ours']['novel_count'] > value['ai_researcher']['novel_count']:
            ours_count_win_count += 1
        elif value['ours']['novel_count'] < value['ai_researcher']['novel_count']:
            ai_researcher_count_win_count += 1
        else:
            count_tie_count += 1
    else:
        print(f'No novelty result found for {topic}')

print(f'Ours count win count: {ours_count_win_count}')
print(f'AI Researcher count win count: {ai_researcher_count_win_count}')
print(f'Count tie count: {count_tie_count}')
print(f'Ours beat AI Researcher in count: {ours_count_win_count / (ours_count_win_count + ai_researcher_count_win_count + count_tie_count)}')
print(f'Ours ratio win count: {ours_ratio_win_count}')
print(f'AI Researcher ratio win count: {ai_researcher_ratio_win_count}')
print(f'Ratio tie count: {ratio_tie_count}')
print(f'Ours beat AI Researcher in ratio: {ours_ratio_win_count / (ours_ratio_win_count + ai_researcher_ratio_win_count + ratio_tie_count)}')
print(f'Available topics: {available_topics}')
print(f'Ours novel count: {ours_novel_count / available_topics}')
print(f'AI Researcher novel count: {ai_researcher_novel_count / available_topics}')
