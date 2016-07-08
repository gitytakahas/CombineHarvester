# setup output directory
rm -rf output
python setup.py

# perform fitting
cd output/sm_cards/LIMITS;
text2workspace.py ztt_mt_1_13TeV.txt -o workspace.root -m 90 -P CombineHarvester.CombinePdfs.ZTTModel:zttModel
#text2workspace.py ztt_mt_1_13TeV.txt -o workspace.root -m 90 -P CombineHarvester.CombinePdfs.ZTTModel_nor:zttModel

#combine -M MaxLikelihoodFit workspace.root --robustFit 1 --rMin 0 --rMax 5 --redefineSignalPOIs r --freezeNuisances x --freezeNuisanceGroups syst
#combine -M MaxLikelihoodFit workspace.root --robustFit 1 --rMin 0 --rMax 5 --redefineSignalPOIs r --freezeNuisances x
combine -M MaxLikelihoodFit workspace.root --robustFit 1 --rMin 0 --rMax 5 -t -1 --expectSignal 1
#combine -M MaxLikelihoodFit workspace.root --robustFit 1 --rMin 0 --rMax 5 -t -1 --expectSignal 1 --freezeNuisances r --redefineSignalPOIs x
#combine -M MaxLikelihoodFit workspace.root --robustFit 1 --rMin 0 --rMax 5 -t -1 --expectSignal 1
#combine -M MaxLikelihoodFit workspace.root --robustFit 1 --rMin 0 --rMax 5

#combine -M MaxLikelihoodFit workspace.root --robustFit 1 --rMin 0 --rMax 5 --redefineSignalPOIs r,CMS_ztt_rate_mFakeTau_13TeV
#combine -M MaxLikelihoodFit workspace.root --robustFit 1 --rMin 0 --rMax 5

#combine -M MultiDimFit workspace.root --algo singles --redefineSignalPOIs r,x --robustFit 1

cd -

# produce post-fit distributions
PostFitShapesFromWorkspace -d output/sm_cards/LIMITS/ztt_mt_1_13TeV.txt -o ztt_mt_90_shapes_1.root -m 90 -f output/sm_cards/LIMITS/mlfit.root:fit_s --postfit --sampling --print --workspace output/sm_cards/LIMITS/workspace.root

python draw.py

