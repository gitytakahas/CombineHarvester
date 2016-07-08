# setup output directory
rm -rf output
python setup_norm.py

# perform fitting
cd output/sm_cards/LIMITS;
text2workspace.py ztt_mt_1_13TeV.txt -o workspace.root -m 90 -P CombineHarvester.CombinePdfs.ZTTModel:zttModel --X-allow-no-background 

combine -M MaxLikelihoodFit workspace.root --robustFit 1 --freezeNuisances r=1
cd -

# produce post-fit distributions
PostFitShapesFromWorkspace -d output/sm_cards/LIMITS/ztt_mt_1_13TeV.txt -o ztt_mt_90_shapes_1.root -m 90 -f output/sm_cards/LIMITS/mlfit.root:fit_s --postfit --sampling --print --workspace output/sm_cards/LIMITS/workspace.root