

acl_topic_list=("topic_1" "topic_6" "topic_10" "topic_25" "topic_31" "topic_23" "topic_11")
cvpr_topic_list=("cvpr_topic_7" "cvpr_topic_1" "cvpr_topic_11" "cvpr_topic_2" "cvpr_topic_9" "cvpr_topic_12" "cvpr_topic_6")
iclr_topic_list=("iclr_topic_34" "iclr_topic_64" "iclr_topic_19" "iclr_topic_53" "iclr_topic_32" "iclr_topic_90")


topics=("${acl_topic_list[@]}" "${cvpr_topic_list[@]}" "${iclr_topic_list[@]}")

# Run all the topics with a batch of 10 processes
# for i in {0..19}; do
#     echo "Running novelty_check_ablation.py with ${topics[$i]}"
#     python src/novelty_check_ablation.py --topic ${topics[$i]} &
#     if [ $((i % 10)) -eq 9 ]; then
#         wait
#     fi
# done

for i in {0..6}; do
    echo "Running novelty_check_ablation.py with ${topics[$i]}"
    python src/novelty_check_ablation.py --topic ${topics[$i]} &
done
wait

for i in {7..13}; do
    echo "Running novelty_check_ablation.py with ${topics[$i]}"
    python src/novelty_check_ablation.py --topic ${topics[$i]} &
done
wait

for i in {14..19}; do
    echo "Running novelty_check_ablation.py with ${topics[$i]}"
    python src/novelty_check_ablation.py --topic ${topics[$i]} &
done
wait