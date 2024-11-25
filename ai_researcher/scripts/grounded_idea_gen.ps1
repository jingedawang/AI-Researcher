for ($seed=1; $seed -le 60; $seed++) {
    # Print current seed
    Write-Host "Seed: $seed"
    python .\src\grounded_idea_gen.py --engine gpt-4o --paper_cache ..\cache_results_test\lit_review\ours.json --idea_cache ..\cache_results_test\seed_ideas\tailored_visions.json --grounding_k 10 --method prompting --ideas_n 5 --seed $seed --RAG True
}