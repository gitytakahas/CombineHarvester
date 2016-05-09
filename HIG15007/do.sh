# setup output directory
rm -rf output
python scripts/setupDatacards.py

# perform fitting
cd output/LIMITS/mt;
text2workspace.py datacard.txt -o workspace.root -m 125

combine -M MaxLikelihoodFit workspace.root --robustFit 1 -t -1 --expectSignal 1
cd -

# produce post-fit distributions
PostFitShapesFromWorkspace -d output/LIMITS/mt/datacard.txt -o htt_mt_shapes.root -m 125 -f output/LIMITS/mt/mlfit.root:fit_s --postfit --sampling --print --workspace output/LIMITS/mt/workspace.root