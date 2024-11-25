import json

conferences = ['acl', 'cvpr', 'hfdaily', 'iclr']
conference_prefixs = ['', 'cvpr_', 'hfdaily_', 'iclr_']

conference_index = 1

# Load topic_1.json to topic_20.json
def load_novelty_score_summary(topic_num):
    with open(f'novelty_score_summarys_original_faiss_55_all/{conference_prefixs[conference_index]}topic_{topic_num}.json') as f:
        topic = json.load(f)
    return topic

win_count = 0
equal_count = 0
loss_count = 0
ours_mean = 0
ai_researcher_mean = 0

# Load all topic json files
for i in range(1, 32):
    novelty_score_summaries = load_novelty_score_summary(i)
    values = list(novelty_score_summaries[conferences[conference_index]].values())[0]
    if 'ai_researcher' in values and 'ours' in values:
        ai_researcher_mean += values['ai_researcher']
        ours_mean += values['ours']
        if values['ai_researcher'] > values['ours']:
            loss_count += 1
        elif values['ai_researcher'] == values['ours']:
            equal_count += 1
        else:
            win_count += 1
    else:
        print(f'Topic {i} is not found')

print(f'Win count: {win_count}')
print(f'Equal count: {equal_count}')
print(f'Loss count: {loss_count}')
print(f'Ours mean: {ours_mean / (win_count + equal_count + loss_count)}')
print(f'AI Researcher mean: {ai_researcher_mean / (win_count + equal_count + loss_count)}')
