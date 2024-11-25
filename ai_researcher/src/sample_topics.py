import json
import tqdm

sampled_id_maps = {}
conferences = ['acl', 'iclr', 'hfdaily', 'cvpr']
# Load conference_id_map.json
acl_id_map = json.load(open('../acl_id_map.json'))
iclr_id_map = json.load(open('../iclr_id_map.json'))
hfdaily_id_map = json.load(open('../hfdaily_id_map.json'))
cvpr_id_map = json.load(open('../cvpr_id_map.json'))
# Combine the id maps
id_maps = {**acl_id_map, **iclr_id_map, **hfdaily_id_map, **cvpr_id_map}

# # Randomly sample the dict to get a smaller dict
# import random
# sampled_id_maps = dict(random.sample(id_maps.items(), 40))
# print(sampled_id_maps)

# # Print all the topics in a list
# print([topic for topic, value in sampled_id_maps.items()])


# # Save the sampled dict
# with open('../sampled_id_maps.json', 'w') as f:
#     json.dump(sampled_id_maps, f, indent=4)


# Generate id maps with given topics

acl_topic_list=["topic_27","topic_6","topic_10","topic_25","topic_31","topic_23","topic_11"]
cvpr_topic_list=["cvpr_topic_7","cvpr_topic_1","cvpr_topic_11","cvpr_topic_2","cvpr_topic_9","cvpr_topic_12","cvpr_topic_6"]
iclr_topic_list=["iclr_topic_34","iclr_topic_64","iclr_topic_19","iclr_topic_53","iclr_topic_32","iclr_topic_90"]

# Filter the id_maps to contain only the topics in the acl_topic_list, cvpr_topic_list, and iclr_topic_list
filtered_id_maps = {}
for topic in acl_topic_list:
    if topic in id_maps:
        filtered_id_maps[topic] = id_maps[topic]
for topic in cvpr_topic_list:
    if topic in id_maps:
        filtered_id_maps[topic] = id_maps[topic]
for topic in iclr_topic_list:
    if topic in id_maps:
        filtered_id_maps[topic] = id_maps[topic]

# Save the filtered dict
with open('../filtered_id_maps.json', 'w') as f:
    json.dump(filtered_id_maps, f, indent=4)