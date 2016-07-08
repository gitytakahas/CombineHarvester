# setup output directory
rm -rf output
python setup.py

# perform fitting
cd output/sm_cards/LIMITS;
text2workspace.py ztt_mt_1_13TeV.txt -o workspace.root -m 90 -P CombineHarvester.CombinePdfs.ZTTModel:zttModel

#combine -M MaxLikelihoodFit workspace.root --robustFit 1 --rMin 0 --rMax 5 --redefineSignalPOIs r --freezeNuisances x
#combine -M MaxLikelihoodFit workspace.root --robustFit 1 --rMin 0 --rMax 5
#combine -M MultiDimFit workspace.root --algo singles --redefineSignalPOIs r,x --robustFit 1

# for 1D scan
#combine -M MultiDimFit workspace.root --algo grid -P CMS_ztt_rate_mFakeTau_13TeV --redefineSignalPOIs CMS_ztt_rate_mFakeTau_13TeV,x --points 50 --setPhysicsModelParameterRanges x=0,1 --robustFit 1 -n .nominal

# combine -M MultiDimFit workspace.root --algo grid -P CMS_ztt_rate_mFakeTau_13TeV --redefineSignalPOIs x --points 50 --setPhysicsModelParameterRanges x=0,1 --robustFit 1 -n .nominal

combine -M MultiDimFit workspace.root --algo grid --redefineSignalPOIs x --points 50 --setPhysicsModelParameterRanges x=0,1 --robustFit 1 -n .nominal
combine -M MultiDimFit workspace.root --algo grid --redefineSignalPOIs x --points 50 --setPhysicsModelParameterRanges x=0,1 --robustFit 1 --freezeNuisanceGroups lumi -n .freeze.lumi
combine -M MultiDimFit workspace.root --algo grid --redefineSignalPOIs x --points 50 --setPhysicsModelParameterRanges x=0,1 --robustFit 1 --freezeNuisanceGroups lumi,syst -n .freeze.lumi.syst

# impact
#combineTool.py -M Impacts -d workspace.root -m 90 --doInitialFit --robustFit 1
#combineTool.py -M Impacts -d workspace.root -m 90 --robustFit 1 --doFits
#combineTool.py -M Impacts -d workspace.root -m 90 -o impacts.json

#plotImpacts.py -i impacts.json -o impacts

cd -

python plot1DScan.py -m output/sm_cards/LIMITS/higgsCombine.nominal.MultiDimFit.mH120.root --POI "x" -o nominal.es --no-input-label --logo 'CMS' --logo-sub 'Internal' --others "output/sm_cards/LIMITS/higgsCombine.freeze.lumi.MultiDimFit.mH120.root:Freeze Lumi:2" "output/sm_cards/LIMITS/higgsCombine.freeze.lumi.syst.MultiDimFit.mH120.root:Freeze Lumi-Syst:4" --breakdown "Lumi,Syst,Stat"
#python plot1DScan.py -m output/sm_cards/LIMITS/higgsCombine.nominal.MultiDimFit.mH120.root --POI "CMS_ztt_rate_mFakeTau_13TeV" -o nominal.es --no-input-label --logo 'CMS' --logo-sub 'Internal'


# produce post-fit distributions
#PostFitShapesFromWorkspace -d output/sm_cards/LIMITS/ztt_mt_1_13TeV.txt -o ztt_mt_90_shapes_1.root -m 90 -f output/sm_cards/LIMITS/mlfit.root:fit_s --postfit --sampling --print --workspace output/sm_cards/LIMITS/workspace.root

#python draw.py

