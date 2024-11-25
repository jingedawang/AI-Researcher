

# Tranverse all the directories in ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference
# For each directory, name it {topic}, check if there is a ${step}_final_proposal_wi_method_decom folder in {topic}.
# If there is, check if ${step}_final_proposal_wi_method_decom folder is empty.
# If it is empty, copy the ~/projects/huxiang/experiment_result/ours_v2/$conference/{topic} folder to replace the current {topic} folder.
# conference=$1
# # Read arguments from the command line
# step=$2
conferences=("acl" "cvpr" "iclr" "hfdaily")
steps=("step_0" "step_1" "step_2" "step_3")
# echo "conference: $conference"
# echo "step: $step"
for conference in ${conferences[@]}
do
    for step in ${steps[@]}
    do
        for topic in $(ls ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference)
        do
            if [ -d ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/${step}_final_proposal_wi_method_decom ]
            then
                if [ ! "$(ls -A ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/${step}_final_proposal_wi_method_decom)" ]
                then
                    # Check if ~/projects/huxiang/experiment_result/ours_v2/$conference/$topic/${step}_final_proposal_wi_method_decom is not empty
                    if [ "$(ls -A ~/projects/huxiang/experiment_result/ours_v2/$conference/$topic/${step}_final_proposal_wi_method_decom)" ]
                    then
                        echo "Removing ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/${step}_final_proposal_wi_method_decom"
                        rm -r ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/${step}_final_proposal_wi_method_decom
                        echo "Copying ~/projects/huxiang/experiment_result/ours_v2/$conference/$topic/${step}_final_proposal_wi_method_decom to ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/${step}_final_proposal_wi_method_decom"
                        cp -r ~/projects/huxiang/experiment_result/ours_v2/$conference/$topic/${step}_final_proposal_wi_method_decom ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/${step}_final_proposal_wi_method_decom
                    else
                        echo "Directory ~/projects/huxiang/experiment_result/ours_v2/$conference/$topic/${step}_final_proposal_wi_method_decom is empty"
                    fi
                else
                    # Tranverse all the files in ~/projects/huxiang/experiment_result/ours_v2/$conference/$topic/${step}_final_proposal_wi_method_decom,
                    # For each file, check if it also exists in ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/${step}_final_proposal_wi_method_decom.
                    # If not, copy the file to ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/${step}_final_proposal_wi_method_decom/
                    for file in $(ls ~/projects/huxiang/experiment_result/ours_v2/$conference/$topic/${step}_final_proposal_wi_method_decom)
                    do
                        if [ ! -f ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/${step}_final_proposal_wi_method_decom/$file ]
                        then
                            echo "Copying ~/projects/huxiang/experiment_result/ours_v2/$conference/$topic/${step}_final_proposal_wi_method_decom/$file to ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/${step}_final_proposal_wi_method_decom/"
                            cp ~/projects/huxiang/experiment_result/ours_v2/$conference/$topic/${step}_final_proposal_wi_method_decom/$file ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/${step}_final_proposal_wi_method_decom/
                        fi
                    done
                fi
            else
                echo "Directory ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/${step}_final_proposal_wi_method_decom does not exist"
                if [ -d ~/projects/huxiang/experiment_result/ours_v2/$conference/$topic/${step}_final_proposal_wi_method_decom ]
                then
                    echo "Copying ~/projects/huxiang/experiment_result/ours_v2/$conference/$topic/${step}_final_proposal_wi_method_decom to ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/"
                cp -r ~/projects/huxiang/experiment_result/ours_v2/$conference/$topic/${step}_final_proposal_wi_method_decom ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference/$topic/
                else
                    echo "Directory ~/projects/huxiang/experiment_result/ours_v2/$conference/$topic/${step}_final_proposal_wi_method_decom does not exist"
                fi
            fi
        done
    done
done

