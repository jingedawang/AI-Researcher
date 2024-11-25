import time
from openai import OpenAI, AzureOpenAI
import anthropic
from utils import call_api
import argparse
import json
import os
from lit_review_tools import parse_and_execute, format_papers_for_printing, print_top_papers_from_paper_bank, dedup_paper_bank
from utils import cache_output, format_plan_json
from self_improvement import get_related_works
import random 
from tqdm import tqdm
import retry
random.seed(2024)

def paper_query(idea, topic_description, openai_client, model, seed):
    # prompt = "You are a professor in Natural Language Processing. You need to evaluate the novelty of a proposed research idea on the topic of: " + topic_description + ".\n\n"
    prompt = "You are a professor in Natural Language Processing. You need to evaluate the novelty of a proposed research idea.\n"

    prompt += "The idea is:\n" + idea + "\n\n"
    prompt += "You want to do a round of paper search in order to find out whether the proposed project has already been done. "
    prompt += "You should propose some keywords for using the Semantic Scholar API to find the most relevant papers to this proposed idea. Formulate your query as: KeywordQuery(\"keyword\"). Give me 1 - 3 queries, the keyword can be a concatenation of multiple keywords (just put a space between every word) but please be concise and try to cover all the main aspects.\n"
    prompt += "The query keywords should be specific to the proposed research idea, in order to find whether there are similar ideas in the literature. try to include language model to find relevant papers within NLP. "
    prompt += "Your query (just return the queries with no additional text, put each one in a new line without any other explanation):"
    prompt_messages = [{"role": "user", "content": prompt}]
    response, cost = call_api(openai_client, model, prompt_messages, temperature=0., max_tokens=100, seed=seed, json_output=False)
    
    return prompt, response, cost

def paper_scoring(paper_lst, idea, topic_description, openai_client, model, seed):
    ## use gpt4 to score each paper 
    prompt = "You are a research assistant whose job is to read the below set of papers and score each paper based on how similar the paper is to the proposed idea.\n"
    prompt += "The proposed idea is: " + idea.strip() + ".\n"
    prompt += "The topic is " + topic_description.strip() + " and it should be related to large language models and NLP broadly.\n"
    prompt += "The papers are:\n" + format_papers_for_printing(paper_lst) + "\n"
    prompt += "Please score each paper from 1 to 10 based on the similarity and relevance to the proposed idea. 10 means the paper is essentially the same as the proposed idea; 1 means the paper is not even relevant to the topic; 5 means the paper shares some similarity but some key details are different.\n"
    prompt += "Write the response in JSON format with \"paperID: score\" as the key and value for each paper.\n"
    
    prompt_messages = [{"role": "user", "content": prompt}]
    response, cost = call_api(openai_client, model, prompt_messages, temperature=0., max_tokens=4000, seed=seed, json_output=True)
    return prompt, response, cost

def novelty_score(experiment_plan, related_paper, openai_client, model, seed):
    prompt = "You are a professor specialized in Natural Language Processing. You have a project proposal and want to find related works to cite in the paper. Your job is to decide whether the given paper is directly relevant to the project and should be cited as similar work.\n"
    prompt += "The project proposal is:\n" + json.dumps(experiment_plan).strip() + ".\n"
    prompt += "The paper is:\n" + format_papers_for_printing([related_paper], include_score=False, include_id=False) + "\n"
    prompt += "The project proposal and paper abstract are considered a match if both the research problem and the approach are the same. For example, if they are both trying to improve code generation accuracy and both propose to use retrieval augmentation. Note that the method details do not matter, you should only focus on the high-level concepts and judge whether they are directly relevant.\n"
    prompt += "You should first specify what is the proposed research problem and approach. If answering yes, your explanation should be the one-sentence summary of both the abstract and the proposal and their similarity (e.g., they are both about probing biases of language models via fictional characters). If answering no, give the short summaries of the abstract and proposal separately, then highlight their differences. Then end your response with a binary judgment, saying either \"Yes\" or \"No\". Change to a new line after your explanation and just say Yes or No with no punctuation in the end.\n"
    # print (prompt)

    prompt_messages = [{"role": "user", "content": prompt}]
    response, cost = call_api(openai_client, model, prompt_messages, temperature=0., max_tokens=1000, seed=seed, json_output=False)
    return prompt, response, cost


@retry.retry(tries=3, delay=2)
def novelty_check(idea_name, idea, topic_description, openai_client, model, seed):
    paper_bank = {}
    total_cost = 0
    all_queries = []

    ## get KeywordSearch queries
    _, queries, cost = paper_query(idea, topic_description, openai_client, model, seed)
    total_cost += cost
    # print ("queries: \n", queries)
    all_queries = queries.strip().split("\n")
    ## also add the idea name as an additional query
    all_queries.append("KeywordQuery(\"{}\")".format(idea_name + " NLP"))

    for query in all_queries:
        paper_lst = parse_and_execute(query.strip())
        if paper_lst is None:
            continue
        paper_bank.update({paper["paperId"]: paper for paper in paper_lst})

        ## score each paper
        prompt, response, cost = paper_scoring(paper_lst, idea, topic_description, openai_client, model, seed)
        total_cost += cost
        response = json.loads(response.strip())

        ## initialize all scores to 0 then fill in gpt4 scores
        for k,v in response.items():
            if k in paper_bank:
                paper_bank[k]["score"] = v
        
        ## the missing papers will have a score of 0 
        for k,v in paper_bank.items():
            if "score" not in v:
                v["score"] = 0
            
        # print (paper_bank)
        print_top_papers_from_paper_bank(paper_bank, top_k=10)
        print ("-----------------------------------\n")
    
    ## the missing papers will have a score of 0 
    for k,v in paper_bank.items():
        if "score" not in v:
            v["score"] = 0
    
    ## rank all papers by score
    data_list = [{'id': id, **info} for id, info in paper_bank.items()]
    sorted_papers = sorted(data_list, key=lambda x: x['score'], reverse=True)
    sorted_data = dedup_paper_bank(sorted_data)

    ## novelty score
    prompt, novelty, cost = novelty_score(sorted_papers, idea, openai_client, model, seed)
    # print (prompt, novelty)

    return novelty, sorted_papers, total_cost, all_queries

import requests
def search_papers_according_to_query(search_query, rank_doc=None, topk=10, ip_address="http://20.2.82.55:5002/"):
    """
    Args:
        search_query (str): The search query.
        rank_doc (str): The document to rank against.
        topk (int): The number of top results to return.
    Returns:
        list: A list of topk search results with scores.
    """
    if rank_doc is None:
        rank_doc = search_query
    # 构建请求URL
    url = f"{ip_address}paper_search_v2?search_query={search_query}&rank_doc={rank_doc}&topk={topk}"
    # 发送POST请求
    response = requests.post(url)
    # 解析JSON响应
    result = response.json()
    return result

def compute_novelty_for_an_idea(cache_dir, cache_name, topic_description, source: str, client, engine='gpt-4o', seed=2024, check_n=5):
    if not os.path.isdir(cache_dir + cache_name):
        print(f"Cache directory {cache_dir + cache_name} does not exist")
        return None
    filenames = os.listdir(cache_dir + cache_name)
    # # Use only 10 files for testing
    # filenames = filenames[:10]
    if len(filenames) == 0:
        print(f"No files found in {cache_dir + cache_name}")
        return None
    novel_idea = 0
    for filename in tqdm(filenames, desc=f'Computing novelty for {cache_name} with {source}'):
        cache_file = os.path.join(cache_dir + cache_name + "/" + filename)
        print(f'Processing {cache_file}')
        with open(cache_file, "r") as f:
            idea_file = json.load(f)
        if source == 'ai_researcher':
            idea_name = idea_file["idea_name"]
            if len(idea_file["full_experiment_plan"].keys()) == 1:
                idea = list(idea_file["full_experiment_plan"].values())[0]
            else:
                idea = idea_file["full_experiment_plan"]
        elif source == 'ours':
            idea_name = list(idea_file['initial_proposal'].keys())[0]
            if not idea_file['final_proposal']:
                print(f'Found null final proposal for {cache_name}/{filename}')
                continue
            if idea_file['final_proposal']['final_proposal'] and len(idea_file['final_proposal']['final_proposal'].keys()) == 1:
                idea = list(idea_file['final_proposal'].values())[0]
            else:
                idea = idea_file["final_proposal"]['final_proposal']

        if "novelty_papers" not in idea_file:
            # print ("Retrieving related works...")

            original_paper_bank = search_papers_according_to_query(topic_description.strip(), topk=5)
            paper_bank = search_papers_according_to_query(json.dumps(idea).strip(), topk=5)
            paper_bank = original_paper_bank + paper_bank
            # print(f'paper_bank: {[(paper["title"], paper["score"]) for paper in paper_bank]}')
            # paper_bank, total_cost, all_queries = get_related_works(idea_name, idea, topic_description, client, engine, seed)
            # output = format_papers_for_printing(paper_bank[ : 10])
            # print ("Top 10 papers: ")
            # print (output)
            # print ("Total cost: ", total_cost)

            ## save the paper bank
            if not os.path.exists(cache_dir + cache_name + "/"):
                os.makedirs(cache_dir + cache_name + "/")
            # idea_file["novelty_queries"] = all_queries
            idea_file["novelty_papers"] = paper_bank
            cache_output(idea_file, cache_file)

        # if "novelty" not in idea_file:
        related_papers = idea_file["novelty_papers"]

        # # Remove 'Title' field
        # if idea:
        #     if 'Title' in idea:
        #         idea.pop('Title', None)

        novel = True 
        # print ("checking through top {} papers".format(str(check_n)))

        for i in range(10):
            if 'novelty_score' not in idea_file["novelty_papers"][i] or 'novelty_judgment' not in idea_file["novelty_papers"][i]:
                prompt, response, cost = novelty_score(idea, related_papers[i], client, engine, seed)
                idea_file["novelty_papers"][i]["novelty_score"] = response.strip()
                final_judgment = response.strip().split()[-1].lower()
                idea_file["novelty_papers"][i]["novelty_judgment"] = final_judgment
            else:
                final_judgment = idea_file["novelty_papers"][i]["novelty_judgment"]
            # print ("novelty judgment: ", final_judgment)
            # print ("\n\n")
            
            if final_judgment == "yes":
                novel = False
            
            # print (format_papers_for_printing([related_papers[i]]))
            # print (response)
            # print (cost)
        idea_file["novelty"] = "yes" if novel else "no"

        if idea_file["novelty"] == "yes":
            novel_idea += 1
        
        cache_output(idea_file, cache_file)
        # print ("Novelty judgment: ", idea_file["novelty"])

    print ("Novelty rate: {} / {} = {}%".format(novel_idea, len(filenames), novel_idea / len(filenames) * 100))
    return novel_idea / len(filenames)

def clean_novelty_cache(cache_dir):
    filenames = os.listdir(cache_dir)
    for filename in filenames:
        cache_file = os.path.join(cache_dir + filename)
        with open(cache_file, "r") as f:
            idea_file = json.load(f)
        if "novelty" in idea_file:
            del idea_file["novelty"]
        if "novelty_queries" in idea_file:
            del idea_file["novelty_queries"]
        if "novelty_papers" in idea_file:
            del idea_file["novelty_papers"]
        cache_output(idea_file, cache_file)

import concurrent.futures

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--engine', type=str, default='gpt-4o', help='api engine; https://openai.com/api/')
    parser.add_argument('--check_n', type=int, default=5, help="number of top papers to check for novelty")
    parser.add_argument('--retrieve', action='store_true', help='whether to do the paper retrieval')
    parser.add_argument('--novelty', action='store_true', help='whether to do the novelty check')
    parser.add_argument('--seed', type=int, default=2024, help="seed for GPT-4 generation")
    parser.add_argument('--topic', type=str, default=None, help="topic to check novelty")
    parser.add_argument('--conference', type=str, default='acl', help="conference to check novelty")
    parser.add_argument('--clean_cache', action='store_true', help='whether to clean novelty cache')
    args = parser.parse_args()

    with open("../keys.json", "r") as f:
        keys = json.load(f)

    ANTH_KEY = keys["anthropic_key"]
    OAI_KEY = keys["api_key"]
    ORG_ID = keys["organization_id"]
    S2_KEY = keys["s2_key"]
    
    client = AzureOpenAI(
        azure_endpoint="https://westlakeaustraliaeast.openai.azure.com/", 
        api_key=os.environ.get("AZURE_API_KEY"),
        api_version="2024-02-15-preview"
    )
    
    conference = args.conference

    cache_dir_for_ai_researcher = "../cache_results_test/project_proposals_20240928_original_faiss_55_all/"
    cache_dir_for_ours = f"../experiment_result/test/{conference}/"

    with open(f'../{conference}_id_map.json') as f:
        conference_id_map = json.load(f)
    
    # Clean novelty cache
    if args.clean_cache:
        for topic in tqdm(conference_id_map.keys(), desc=f'Cleaning novelty cache for {conference}'):
            clean_novelty_cache(cache_dir_for_ai_researcher + topic + "/")
            clean_novelty_cache(cache_dir_for_ours + conference_id_map[topic][0] + "/step_3_final_proposal_wi_method_decom/")
        print("Novelty cache cleaned")
        exit()

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        futures = {}
        for topic, value in conference_id_map.items():
            if args.topic:
                if topic != args.topic:
                    continue
            arxiv_id = value[0]
            topic_description = value[1]

            if os.path.exists(f'novelty_score_summarys_test/{topic}.json'):
                novelty_score_summary = json.load(open(f'novelty_score_summarys_test/{topic}.json'))
            else:
                novelty_score_summary = {
                    'acl': {},
                    'iclr': {},
                    'cvpr': {},
                    'hfdaily': {}
                }

            if topic not in novelty_score_summary[conference]:
                novelty_score_summary[conference][topic] = {
                    'arxiv_id': arxiv_id
                }
            if 'ai_researcher' not in novelty_score_summary[conference][topic]:
                future = executor.submit(compute_novelty_for_an_idea, cache_dir_for_ai_researcher, topic, topic_description, 'ai_researcher', client, args.engine)
                futures[future] = [topic, 'ai_researcher']
            if 'ours' not in novelty_score_summary[conference][topic]:
                future = executor.submit(compute_novelty_for_an_idea, cache_dir_for_ours, f'{arxiv_id}/step_3_final_proposal_wi_method_decom', topic_description, 'ours', client, args.engine)
                futures[future] = [topic, 'ours']
            json.dump(novelty_score_summary, open(f'novelty_score_summarys_test/{topic}.json', 'w'), indent=4, ensure_ascii=False)

        for future in concurrent.futures.as_completed(futures):
            topic, source = futures[future]

            if os.path.exists(f'novelty_score_summarys_test/{topic}.json'):
                novelty_score_summary = json.load(open(f'novelty_score_summarys_test/{topic}.json'))
            else:
                novelty_score_summary = {
                    'acl': {},
                    'iclr': {},
                    'cvpr': {},
                    'hfdaily': {}
                }

            # try:
            score = future.result()
            if score:
                novelty_score_summary[conference][topic][source] = score
                print(f'Novelty score for {conference} - {topic} - {source}: {score}')
                json.dump(novelty_score_summary, open(f'novelty_score_summarys_test/{topic}.json', 'w'), indent=4, ensure_ascii=False)
            # except Exception as e:
            #     print(f'Novelty score for {conference} - {topic} - {source} failed with error: {e}')
    
    # novelty_score_sum_ai_researcher = 0
    # novelty_score_sum_ours = 0
    # for topic, value in conference_id_map.items():
    #     novelty_score_sum_ai_researcher += novelty_score_summary[conference][topic]['ai_researcher']
    #     novelty_score_sum_ours += novelty_score_summary[conference][topic]['ours']
    # print("Average novelty score for ai_researcher: ", novelty_score_sum_ai_researcher / len(conference_id_map))
    # print("Average novelty score for ours: ", novelty_score_sum_ours / len(conference_id_map))