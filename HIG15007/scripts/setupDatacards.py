#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import argparse
import os

# Need this later
def RenameSyst(cmb, syst, old, new):
    if old in syst.name():
        oldname = syst.name()
        syst.set_name(new)
        # Should change the ch::Parameter names too
        cmb.RenameParameter(oldname, new)

parser = argparse.ArgumentParser()
parser.add_argument('--output', '-o', default='./output/LIMITS', help="""
    Output directory""")

args = parser.parse_args()
cb = ch.CombineHarvester()

##########################################################################
# Set input shape files
##########################################################################
shapefile = '/afs/cern.ch/user/y/ytakahas/work/Combine/CMSSW_7_1_5/src/CombineHarvester/HIG15007/shapes/datacard_sm_svfit_mass.root'
#shapefile = '/afs/cern.ch/user/y/ytakahas/work/Combine/CMSSW_7_1_5/src/CombineHarvester/HIG15007/shapes/datacard_sm_mva2.root'
#shapefile = '/afs/cern.ch/user/y/ytakahas/work/Combine/CMSSW_7_1_5/src/CombineHarvester/HIG15007/shapes/datacard_sm_mva2div1.root'
#shapefile = '/afs/cern.ch/user/y/ytakahas/work/Combine/CMSSW_7_1_5/src/CombineHarvester/HIG15007/shapes/datacard_sm_mva2_separatetraining.root'
#shapefile = '/afs/cern.ch/user/y/ytakahas/work/Combine/CMSSW_7_1_5/src/CombineHarvester/HIG15007/shapes/datacard_sm_mva2div1_separatetraining.root'

##########################################################################
# Set the processes and categories
##########################################################################
sig_procs = ['HiggsGGH', 'HiggsVBF']

bkg_procs = {
    'mt': ['W', 'QCD', 'ZTT', 'ZL', 'ZJ', 'TT', 'VV'],
}

bins = {
    'mt': [(0, 'mt_0jet_medium'),
           (1, 'mt_0jet_high'), 
           (2, 'mt_1jet_medium'),
           (3, 'mt_1jet_high_lowhiggspt'),
           (4, 'mt_1jet_high_highhiggspt'),
           (5, 'mt_vbf')]

    'mt': [ #(0, 'mt_0jet_medium')]
#           (1, 'mt_0jet_high')]
#           (2, 'mt_1jet_medium')]
#           (3, 'mt_1jet_high_lowhiggspt')]
#           (4, 'mt_1jet_high_highhiggspt')]
#           (5, 'mt_vbf')]


#    'mt':[
#        (0, 'mt_0jet_lowmva0'), 
#        (1, 'mt_0jet_highmva0'), 
#        (2, 'mt_1jet_novbf_lowmva0'), 
#        (3, 'mt_1jet_novbf_highmva0'), 
#        (4, 'mt_vbf_lowmva0'), 
#        (5, 'mt_vbf_highmva0'), 
#        ]
}

channels = ['mt']

##########################################################################
# Create CH entries and load shapes
##########################################################################
for chn in channels:
    ana = ['htt']
    era = ['13TeV']
    cb.AddObservations(['*'], ana, era, [chn], bins[chn])
    cb.AddProcesses(['*'], ana, era, [chn], bkg_procs[chn], bins[chn], False)
    cb.AddProcesses(['125'], ana, era, [chn], sig_procs, bins[chn], True)

##########################################################################
# Define systematic uncertainties
##########################################################################

signal = cb.cp().signals().process_set()

cb.cp().AddSyst(
    cb, 'CMS_eff_m', 'lnN', ch.SystMap('channel', 'process')
        (['mt'], signal + ['ZTT', 'ZLL', 'ZL', 'ZJ', 'TT', 'VV'], 1.03))


# Only create the eff_t lnN if we want this to be constrained,
# otherwise set a rateParam.
# Split tau ID efficiency uncertainty into part ("CMS_eff_t") that is correlated between channels
# and part ("CMS_eff_t_et", "CMS_eff_t_mt", "CMS_eff_t_tt") that is uncorrelated

cb.cp().AddSyst(
    cb, 'CMS_eff_t', 'lnN', ch.SystMap('channel', 'process')
    (['mt'], signal + ['ZTT', 'TT', 'VV'], 1.05))

# Split tau energy scale uncertainty into part ("CMS_scale_t") that is correlated between channels
# and part ("CMS_scale_t_et", "CMS_scale_t_mt", "CMS_scale_t_tt") that is uncorrelated

cb.cp().AddSyst(
    cb, 'CMS_scale_t_$CHANNEL_$ERA', 'shape', ch.SystMap('channel', 'process')
        (['mt'], signal + ['ZTT'], 1.0))

cb.cp().AddSyst(
    cb, 'CMS_$ANALYSIS_boson_scale_met', 'lnN', ch.SystMap('channel', 'process')
        (['mt'], ['ZTT', 'W', 'ZL', 'ZJ', 'ZLL'], 1.02))
cb.cp().AddSyst(
    cb, 'CMS_$ANALYSIS_boson_reso_met', 'lnN', ch.SystMap('channel', 'process')
        (['mt'], ['ZTT', 'W', 'ZL', 'ZJ', 'ZLL'], 1.02))
cb.cp().AddSyst(
    cb, 'CMS_$ANALYSIS_ewkTop_scale_met', 'lnN', ch.SystMap('channel', 'process')
        (['mt'], ['TT', 'VV'], 1.03))
cb.cp().AddSyst(
    cb, 'CMS_$ANALYSIS_ewkTop_reso_met', 'lnN', ch.SystMap('channel', 'process')
        (['mt'], ['TT', 'VV'], 1.01))

cb.cp().process(['QCD']).AddSyst(
    cb, 'CMS_$ANALYSIS_qcdSyst_$CHANNEL_$ERA', 'lnN', ch.SystMap('channel')
        (['mt'],      1.10))  # From Tyler's studies

cb.cp().process(['TT']).AddSyst(
    cb, 'CMS_$ANALYSIS_ttjXsec_$ERA', 'lnN', ch.SystMap('channel')
        (['mt'],  1.06))

cb.cp().process(['TT']).AddSyst(
    cb, 'CMS_$ANALYSIS_ttjExtrapol_$CHANNEL_$ERA', 'lnN', ch.SystMap('channel')
        (['mt'],  1.10))

cb.cp().process(['VV']).AddSyst(
    cb, 'CMS_$ANALYSIS_vvXsec_$ERA', 'lnN', ch.SystMap('channel')
        (['mt'],  1.10))

# Give each channel an independent extrap uncertainty
cb.cp().process(['W']).AddSyst(
    cb, 'CMS_$ANALYSIS_wjExtrapol_$CHANNEL_$ERA', 'lnN', ch.SystMap('channel')
        (['mt'],  1.20))

cb.cp().process(['ZJ', 'ZJ', 'ZLL']).AddSyst(
    cb, 'CMS_$ANALYSIS_zjXsec_$ERA', 'lnN', ch.SystMap('channel')
        (['mt'],  1.04))

# KIT cards only have one zllFakeTau param, but need at least three:
#  - e->tau fake rate
#  - mu->tau fake rate (CV: use 100% uncertainty for now, as no measurement of mu->tau fake-rate in Run 2 data available yet)
#  - jet->tau fake rate

cb.cp().process(['ZL']).AddSyst(
    cb, 'CMS_$ANALYSIS_rate_mFakeTau_$ERA', 'lnN', ch.SystMap('channel')
        (['mt'],  2.00))

cb.cp().process(['ZJ']).AddSyst(
    cb, 'CMS_$ANALYSIS_zjFakeTau_$ERA', 'lnN', ch.SystMap('channel')
        (['mt'],  1.30))

cb.cp().AddSyst(
    cb, 'lumi_$ERA', 'lnN', ch.SystMap('channel', 'process')
        (['mt'],  signal + ['ZTT', 'ZL', 'ZJ', 'TT', 'VV'],        1.027))

# Signal acceptance
cb.cp().process(['HiggsGGH']).AddSyst(
    cb, 'CMS_$ANALYSIS_pdf_$ERA', 'lnN', ch.SystMap()(1.031))

cb.cp().process(['HiggsVBF']).AddSyst(
    cb, 'CMS_$ANALYSIS_pdf_$ERA', 'lnN', ch.SystMap()(1.021))

cb.cp().process(['HiggsGGH']).AddSyst(
    cb, 'CMS_$ANALYSIS_QCDscale_$ERA', 'lnN', ch.SystMap()(1.081))

cb.cp().process(['HiggsVBF']).AddSyst(
    cb, 'CMS_$ANALYSIS_QCDscale_$ERA', 'lnN', ch.SystMap()(1.004))


##########################################################################
# Load the shapes
##########################################################################
for chn in channels:
    cb.cp().backgrounds().ExtractShapes(
        shapefile, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')

    cb.cp().signals().ExtractShapes(
        shapefile, '$BIN/$PROCESS$MASS', '$BIN/$PROCESS$MASS_$SYSTEMATIC')

##########################################################################
# Create bin-by-bin
##########################################################################
bbb = ch.BinByBinFactory()
bbb.SetPattern('CMS_$ANALYSIS_$BIN_$ERA_$PROCESS_bin_$#')
bbb.SetAddThreshold(0.1)
bbb.SetMergeThreshold(0.5)  # For now we merge, but to be checked
bbb.SetFixNorm(True)
bbb.MergeAndAdd(cb.cp().backgrounds(), cb)


##########################################################################
# Set nuisance parameter groups
##########################################################################
# Start by calling everything syst and allsyst
cb.SetGroup('allsyst', ['.*'])
cb.SetGroup('syst', ['.*'])

# Then set lumi, and remove from both of the above
cb.SetGroup('lumi', ['lumi_.*'])
cb.RemoveGroup('syst', ['lumi_.*'])
cb.RemoveGroup('allsyst', ['lumi_.*'])

# Now we can split into:
#    - stat + syst + tauid + lumi   ..or..
#    - stat + allsyst + lumi

cb.PrintAll()


##########################################################################
# Write the cards
##########################################################################
writer = ch.CardWriter('$TAG/datacard.txt',
                       '$TAG/shapes.root')
writer.SetWildcardMasses([])  # We don't use the $MASS property here
writer.SetVerbosity(1)
x = writer.WriteCards('%s' % args.output, cb)  # All cards combined
print x
x['%s/datacard.txt' % args.output].PrintAll()
for chn in channels:  # plus a subdir per channel
    writer.WriteCards('%s/%s' % (args.output, chn), cb.cp().channel([chn]))
