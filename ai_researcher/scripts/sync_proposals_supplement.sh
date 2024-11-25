

# Tranverse all the directories in ../experiment_result/project_proposals_20240928_original_faiss_55_all/$conference
# For each directory, name it {topic}, check if there is a ${step}_final_proposal_wi_method_decom folder in {topic}.
# If there is, check if ${step}_final_proposal_wi_method_decom folder is empty.
# If it is empty, copy the ~/projects/huxiang/experiment_result/ours_v2/$conference/{topic} folder to replace the current {topic} folder.
# conference=$1
# # Read arguments from the command line

rerun_topic_list=("2401.15024" "2310.01798" "2401.07004" "2312.01552" "2310.08041" "2310.08915" "2310.17884" "2402.17193" "2404.07424" "2310.01361" "2308.07074" "2310.00034" "2401.02412" "2310.08659" "2406.03699" "2409.06927" "2310.01801" "2402.19464" "2311.04892" "2310.06452" "2310.06117" "2310.06213" "2310.12931" "2306.05836" "2404.04442" "2310.03128" "2310.04668" "2401.12242" "2310.03731" "2310.04564" "2401.05861" "2404.14662" "2311.04661" "2310.00902" "2306.08568" "2306.08543" "2310.03016" "2306.08018" "2310.02992" "2310.07298" "2407.17029" "2310.00785" "2311.03734" "2307.02485" "2402.03744" "2404.08382" "2310.04363" "2310.04560" "2309.14393" "2312.03633" "2310.13289" "2308.08493" "2310.04451" "2310.02129" "2310.06987" "2310.01557")


for topic in ${rerun_topic_list[@]}
do
    echo "Copying ~/projects/huxiang/experiment_result/ours_v2/iclr/$topic/step_3_final_proposal_wi_method_decom_v2 to ../experiment_result/project_proposals_20240928_original_faiss_55_all/iclr/$topic/"
    mv ../experiment_result/project_proposals_20240928_original_faiss_55_all/iclr/$topic/step_3_final_proposal_wi_method_decom ../experiment_result/project_proposals_20240928_original_faiss_55_all/iclr/$topic/step_3_final_proposal_wi_method_decom_v1
    cp -r ~/projects/huxiang/experiment_result/ours_v2/iclr/$topic/step_3_final_proposal_wi_method_decom_v2 ../experiment_result/project_proposals_20240928_original_faiss_55_all/iclr/$topic/
    mv ../experiment_result/project_proposals_20240928_original_faiss_55_all/iclr/$topic/step_3_final_proposal_wi_method_decom_v2 ../experiment_result/project_proposals_20240928_original_faiss_55_all/iclr/$topic/step_3_final_proposal_wi_method_decom
done