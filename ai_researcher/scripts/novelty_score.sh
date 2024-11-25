
# # ACL

# for j in {0..5}
# do
#     start=$((j * 5 + 1))
#     end=$((start + 4))
#     for i in $(seq $start $end)
#     do
#         echo "Running novelty_check.py with cache_name: topic_$i"
#         python src/novelty_check.py --topic topic_$i --conference acl &
#     done
#     wait
# done

# echo "Running novelty_check.py with cache_name: topic_31"
# python src/novelty_check.py --topic topic_31


# # CVPR

# for j in {0..2}
# do
#     start=$((j * 4 + 1))
#     end=$((start + 3))
#     for i in $(seq $start $end)
#     do
#         echo "Running novelty_check.py with cache_name: cvpr_topic_$i"
#         python src/novelty_check.py --topic cvpr_topic_$i --conference cvpr &
#     done
#     wait
# done

# # HFDAILY

# for j in {0..5}
# do
#     start=$((j * 3 + 1))
#     end=$((start + 2))
#     for i in $(seq $start $end)
#     do
#         echo "Running novelty_check.py with cache_name: hfdaily_topic_$i"
#         python src/novelty_check.py --topic hfdaily_topic_$i --conference hfdaily &
#     done
#     wait
# done

# ICLR

for j in {0..4}
do
    start=$((j * 20 + 1))
    end=$((start + 19))
    for i in $(seq $start $end)
    do
        echo "Running novelty_check.py with cache_name: iclr_topic_$i"
        python src/novelty_check.py --topic iclr_topic_$i --conference iclr &
    done
    wait
done


for i in $(seq 101 109)
do
    echo "Running novelty_check.py with cache_name: iclr_topic_$i"
    python src/novelty_check.py --topic iclr_topic_$i --conference iclr &
done
wait