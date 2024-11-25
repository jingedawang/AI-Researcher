## example usage
python src/lit_review.py \
 --engine "gpt-4o" \
 --mode "topic" \
 --topic_description "Tailored Visions: Enhancing Text-to-Image Generation with Personalized Prompt Rewriting. Despite significant progress in the field, it is still challenging to create personalized visual representations that align closely with the desires and preferences of individual users. This process requires users to articulate their ideas in words that are both comprehensible to the models and accurately capture their vision, posing difficulties for many users. In this paper, we tackle this challenge by leveraging historical user interactions with the system to enhance user prompts. We propose a novel approach that involves rewriting user prompts based on a newly collected large-scale text-to-image dataset with over 300k prompts from 3115 users. Our rewriting model enhances the expressiveness and alignment of user prompts with their intended visual outputs. Experimental results demonstrate the superiority of our methods over baseline approaches, as evidenced in our new offline evaluation method and online tests. Our code and dataset are available at this https URL." \
 --cache_name "../cache_results_test/lit_review/tailored_visions.json" \
 --max_paper_bank_size 50 \
 --print_all