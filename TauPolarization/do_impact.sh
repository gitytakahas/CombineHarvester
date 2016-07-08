# setup output directory
rm -rf output
python setup.py

# perform fitting
cd output/sm_cards/LIMITS;
text2workspace.py ztt_mt_1_13TeV.txt -o workspace.root -m 90 -P CombineHarvester.CombinePdfs.ZTTModel:zttModel

# impact
combineTool.py -M Impacts -d workspace.root -m 90 --doInitialFit --robustFit 1 --redefineSignalPOIs x 
combineTool.py -M Impacts -d workspace.root -m 90 --robustFit 1 --doFits --redefineSignalPOIs x 
combineTool.py -M Impacts -d workspace.root -m 90 -o impacts.json --redefineSignalPOIs x 

plotImpacts.py -i impacts.json -o impacts

cd -

