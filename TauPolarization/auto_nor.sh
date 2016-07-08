echo
echo "setup datacards ..."

rm -rf output
python setup.py


cd output/sm_cards/LIMITS;
text2workspace.py ztt_mt_1_13TeV.txt -o workspace.root -m 90 -P CombineHarvester.CombinePdfs.ZTTModel_nor:zttModel

echo
echo "perform fitting ..."

combine -M MaxLikelihoodFit workspace.root --robustFit 1 --rMin 0 --rMax 5 --redefineSignalPOIs x

#echo
#echo "making parabolla ..."
#
combine -M MultiDimFit workspace.root --algo grid --redefineSignalPOIs x --points 50 --setPhysicsModelParameterRanges x=0,1 --robustFit 1 -n .nominal
combine -M MultiDimFit workspace.root --algo grid --redefineSignalPOIs x --points 50 --setPhysicsModelParameterRanges x=0,1 --robustFit 1 --freezeNuisanceGroups lumi -n .freeze.lumi
combine -M MultiDimFit workspace.root --algo grid --redefineSignalPOIs x --points 50 --setPhysicsModelParameterRanges x=0,1 --robustFit 1 --freezeNuisanceGroups lumi,syst -n .freeze.lumi.syst
#
#
#echo
#echo "making impact plots ..."
#
#combineTool.py -M Impacts -d workspace.root -m 90 --doInitialFit --robustFit 1 --redefineSignalPOIs x 
#combineTool.py -M Impacts -d workspace.root -m 90 --robustFit 1 --doFits --redefineSignalPOIs x 
#combineTool.py -M Impacts -d workspace.root -m 90 -o impacts.json --redefineSignalPOIs x 

cd -


echo "draw histograms"
PostFitShapesFromWorkspace -d output/sm_cards/LIMITS/ztt_mt_1_13TeV.txt -o ztt_mt_90_shapes_1.root -m 90 -f output/sm_cards/LIMITS/mlfit.root:fit_s --postfit --sampling --print --workspace output/sm_cards/LIMITS/workspace.root

python draw.py

#
#echo "draw parabolla"
python plot1DScan.py -m output/sm_cards/LIMITS/higgsCombine.nominal.MultiDimFit.mH120.root --POI "x" -o nominal.es --no-input-label --logo 'CMS' --logo-sub 'Internal' --others "output/sm_cards/LIMITS/higgsCombine.freeze.lumi.Multi
#DimFit.mH120.root:Freeze Lumi:2" "output/sm_cards/LIMITS/higgsCombine.freeze.lumi.syst.MultiDimFit.mH120.root:Freeze Lumi-Syst:4" --breakdown "Lumi,Syst,Stat"
#
#echo "impact plot"
#plotImpacts.py -i output/sm_cards/LIMITS/impacts.json -o impacts