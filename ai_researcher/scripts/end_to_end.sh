# Stop if any command fails
set -e

conference="hfdaily"
# Read acl_topic_descriptions.txt and get topic_description in each line and save it to file named by line number
line_number=1
while IFS= read -r line; do
    # Check if "../cache_results_test/lit_review/${conference}_topic_$line_number.json" doesn't exist
    if [ ! -f "../cache_results_test/lit_review/${conference}_topic_$line_number.json" ]; then
        echo "Running lit_review.py $line_number ..."
        python src/lit_review.py \
        --engine "gpt-4o" \
        --mode "topic" \
        --topic_description "$line" \
        --cache_name "../cache_results_test/lit_review/${conference}_topic_$line_number.json" \
        --max_paper_bank_size 50
    fi
    
    
    # grounded idea generation
    topic=${conference}_topic_$line_number
    ideas_n=5 ## batch size
    if [ ! -f "../cache_results_test/seed_ideas/$topic.json" ]; then
        for seed in {1..20}; do
            echo "Running grounded_idea_gen.py on: $topic with seed $seed"
            python src/grounded_idea_gen.py \
            --engine "gpt-4o" \
            --paper_cache "../cache_results_test/lit_review/$topic.json" \
            --idea_cache "../cache_results_test/seed_ideas/$topic.json" \
            --grounding_k 10 \
            --method "prompting" \
            --ideas_n $ideas_n \
            --seed $seed \
            --RAG "True"
        done
    fi

    # idea deduplication
    cache_dir="../cache_results_test/seed_ideas/"

    if [ ! -f "../cache_results_test/seed_ideas/${topic}_similarity_matrix.npy" ]; then
        echo "Running analyze_ideas_semantic_similarity.py with cache_name: $topic"
        python src/analyze_ideas_semantic_similarity.py \
        --cache_dir "$cache_dir" \
        --cache_name "$topic" \
        --save_similarity_matrix
    fi

    if [ ! -f "../cache_results_test/ideas_dedup/$topic.json" ]; then
        echo "Running dedup_ideas.py with cache_name: $topic"
        python src/dedup_ideas.py \
        --cache_dir "$cache_dir" \
        --cache_name "$topic" \
        --dedup_cache_dir "../cache_results_test/ideas_dedup" \
        --similarity_threshold 0.8
    fi

    # project proposal generation
    idea_cache_dir="../cache_results_test/ideas_dedup/"
    project_proposal_cache_dir="../cache_results_test/project_proposals/"
    seed=2024

    if [ ! -d $project_proposal_cache_dir$topic ]; then
        echo "Running experiment_plan_gen.py with cache_name: $topic"
        python src/experiment_plan_gen.py \
        --engine "gpt-4o" \
        --idea_cache_dir "$idea_cache_dir" \
        --cache_name "$topic" \
        --experiment_plan_cache_dir "$project_proposal_cache_dir" \
        --idea_name "all" \
        --seed $seed \
        --method "prompting"
    fi

    line_number=$((line_number + 1))
done < ../${conference}_topic_descriptions.txt
















# # project proposal ranking
# # skipped here to save costs
# experiment_plan_cache_dir="../cache_results_test/project_proposals/"
# ranking_score_dir="../cache_results_test/ranking/"
# cache_names=("factuality_prompting_method")
# seed=2024

# for cache_name in "${cache_names[@]}"; do
#     echo "Running tournament_ranking.py with cache_name: $cache_name"
#     python3 src/tournament_ranking.py \
#     --engine claude-3-5-sonnet-20240620 \
#     --experiment_plan_cache_dir "$experiment_plan_cache_dir" \
#     --cache_name "$cache_name" \
#     --ranking_score_dir "$ranking_score_dir" \
#     --max_round 5 
# done



# # project proposal filtering
# # skipped here to save costs
# cache_dir="../cache_results_test/project_proposals/"
# passed_cache_dir="../cache_results_test/project_proposals_passed/"
# cache_names=("factuality_prompting_method")
# seed=2024

# # Iterate over each cache name and run the Python script
# for cache_name in "${cache_names[@]}"; do
#     echo "Running filter_ideas.py with cache_name: $cache_name"
#     python3 src/filter_ideas.py \
#     --engine "claude-3-5-sonnet-20240620" \
#     --cache_dir "$cache_dir" \
#     --cache_name "$cache_name" \
#     --passed_cache_dir "$passed_cache_dir" \
#     --score_file "../cache_results_test/ranking/$cache_name/round_5.json" 
# done
