## example usage
idea_cache_dir="../cache_results_test/ideas_dedup/"
project_proposal_cache_dir="../cache_results_test/project_proposals/"
cache_names=("tailored_visions")
seed=2024

for cache_name in "${cache_names[@]}"; do
    echo "Running experiment_plan_gen.py with cache_name: $cache_name"
    python src/experiment_plan_gen.py \
    --engine "gpt-4o" \
    --idea_cache_dir "$idea_cache_dir" \
    --cache_name "$cache_name" \
    --experiment_plan_cache_dir "$project_proposal_cache_dir" \
    --idea_name "all" \
    --seed $seed \
    --method "prompting" 
done
