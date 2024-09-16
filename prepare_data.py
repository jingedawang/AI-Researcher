import os
import requests
import json

def test_search_endpoint():
    # 定义测试数据
    search_query = "ResearchAgent"
    rank_doc = "ResearchAgent"
    topk = 5

    # 构建请求URL
    url = f"http://localhost:5002/paper_search?search_query={search_query}&rank_doc={rank_doc}&topk={topk}"

    # 发送POST请求
    response = requests.post(url)

    # 检查响应状态码
    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}"

    # 解析JSON响应
    result = response.json()

    # 检查返回的JSON格式是否符合预期
    assert isinstance(result, list), "Expected result to be a list"
    assert len(result) <= topk, f"Expected at most {topk} results, but got {len(result)}"

    # 打印结果
    print("Test passed!")
    print("Response:", json.dumps(result, indent=2))


def search_papers_according_to_query(search_query, rank_doc=None, topk=10, ip="localhost"):
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
    url = f"http://{ip}:5002/paper_search?search_query={search_query}&rank_doc={rank_doc}&topk={topk}"
    # 发送POST请求
    response = requests.post(url)
    # 解析JSON响应
    result = response.json()
    return result

if __name__ == "__main__":

    dir_path = "C:/Users/meritzyf/Downloads/exp_dataset/acl"
    # Load all the json files in the directory
    json_files = [pos_json for pos_json in os.listdir(dir_path) if pos_json.endswith('.json')]

    # Load the json files
    papers = []
    import tqdm
    for file in tqdm.tqdm(json_files):
        with open(os.path.join(dir_path, file), 'r') as f:
            paper = json.load(f)
            title = paper['title']
            abstract = paper['abstract']
            results = search_papers_according_to_query(search_query=f"{title}. {abstract}", topk=30, ip='20.2.82.55')
            paper['retrieved_papers'] = []
            for result in results:
                title_and_abstract = result[0]
                score = result[1]
                # Get the title and abstract
                # 'Title:LaMP: When Large Language Models Meet Personalization, Abstract:  This paper highlights the importance of personalization in large language\nmodels and introduces the LaMP benchmark -- a novel benchmark for training and\nevaluating language models for producing personalized outputs. LaMP offers a\ncomprehensive evaluation framework with diverse language tasks and multiple\nentries for each user profile. It consists of seven personalized tasks,\nspanning three text classification and four text generation tasks. We\nadditionally propose two retrieval augmentation approaches that retrieve\npersonal items from each user profile for personalizing language model outputs.\nTo this aim, we study various retrieval models, including term matching,\nsemantic matching, and time-aware methods. Extensive experiments on LaMP for\nzero-shot and fine-tuned language models demonstrate the efficacy of the\nproposed retrieval augmentation approach and highlight the impact of\npersonalization in various natural language tasks.\n'
                title = title_and_abstract.split('Title:')[1].split('Abstract:')[0].strip()
                abstract = title_and_abstract.split('Title:')[1].split('Abstract:')[1].strip()
                paper['retrieved_papers'].append({'title': title, 'abstract': abstract, 'score': score})
            papers.append(paper)
    
    # Save the papers
    with open('acl.json', 'w') as f:
        json.dump(papers, f, indent=2)