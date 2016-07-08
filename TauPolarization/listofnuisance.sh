cd output/sm_cards/LIMITS/

for nui in CMS_eff_m CMS_eff_t CMS_ztt_boson_reso_met CMS_ztt_boson_scale_met CMS_ztt_ewkTop_reso_met CMS_ztt_ewkTop_scale_met CMS_ztt_qcdSyst_mt_13TeV CMS_ztt_rate_mFakeTau_13TeV CMS_ztt_ttjExtrapol_mt_13TeV CMS_ztt_ttjXsec_13TeV CMS_ztt_vvXsec_13TeV CMS_ztt_wjExtrapol_mt_13TeV CMS_ztt_zjFakeTau_13TeV CMS_ztt_zjXsec_13TeV lumi_13TeV
do
    echo $nui
    combine -M MaxLikelihoodFit workspace.root --robustFit 1 --rMin 0 --rMax 5 --redefineSignalPOIs $nui --freezeNuisances x | grep "Best"
  
done

cd -