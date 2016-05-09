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

shapes_dir = os.environ['CMSSW_BASE'] + '/src/CombineHarvester/HIG15007/shapes'

cb = ch.CombineHarvester()

##########################################################################
# Set the processes and categories
##########################################################################
sig_procs = ['HiggsGGH', 'HiggsVBF']

bkg_procs = {
    'mt': ['W', 'QCD', 'ZTT', 'ZL', 'ZJ', 'TT', 'VV'],
}

bins = {
    'mt': [(0, 'mt_0jet'), (1, 'mt_low_1jet'), (2, 'mt_high_1jet'), (3, 'mt_vbf')],
}

channels = ['mt']

##########################################################################
# Set input shape files
##########################################################################
files = {
    'mt': {
        'CERN':'datacard_sm_svfit_mass.root'
    },
}

inputs = {
    'mt': 'CERN',
}

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

cb.cp().AddSyst(
    cb, 'CMS_eff_m', 'lnN', ch.SystMap('channel', 'process')
        (['mt'], ['ZTT', 'ZLL', 'ZL', 'ZJ', 'TT', 'VV'], 1.03))


# Only create the eff_t lnN if we want this to be constrained,
# otherwise set a rateParam.
# Split tau ID efficiency uncertainty into part ("CMS_eff_t") that is correlated between channels
# and part ("CMS_eff_t_et", "CMS_eff_t_mt", "CMS_eff_t_tt") that is uncorrelated

cb.cp().AddSyst(
    cb, 'CMS_eff_t', 'lnN', ch.SystMap('channel', 'process')
    (['mt'], ['ZTT', 'TT', 'VV'], 1.05))

# Always create the terms that decorrelate the channels
cb.cp().AddSyst(
    cb, 'CMS_eff_t_$CHANNEL', 'lnN', ch.SystMap('channel', 'process')
        (['mt'], ['ZTT', 'TT', 'VV'], 1.03))


# Split tau energy scale uncertainty into part ("CMS_scale_t") that is correlated between channels
# and part ("CMS_scale_t_et", "CMS_scale_t_mt", "CMS_scale_t_tt") that is uncorrelated

#cb.cp().AddSyst(
#    cb, 'CMS_scale_t_$CHANNEL_$ERA', 'shape', ch.SystMap('channel', 'process')
#        (['mt'], ['ZTT'], 1.0))

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
        (['mt'],  ['ZTT', 'ZL', 'ZJ', 'TT', 'VV'],        1.027))

# Signal acceptance
cb.cp().process(['ZTT']).AddSyst(
    cb, 'CMS_$ANALYSIS_pdf_$ERA', 'lnN', ch.SystMap()(1.015))
cb.cp().process(['ZTT']).AddSyst(
    cb, 'CMS_$ANALYSIS_QCDscale_$ERA', 'lnN', ch.SystMap()(1.005))


##########################################################################
# Load the shapes
##########################################################################
for chn in channels:
    cb.cp().backgrounds().ExtractShapes(
        '%s/%s/%s' % (shapes_dir, inputs[chn], files[chn][inputs[chn]]), 
        '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')

    cb.cp().signals().ExtractShapes(
        '%s/%s/%s' % (shapes_dir, inputs[chn], files[chn][inputs[chn]]), 
        '$BIN/$PROCESS$MASS', '$BIN/$PROCESS$MASS_$SYSTEMATIC')



##########################################################################
# Tau ES modifcations
##########################################################################
# Now we manipulate the tau ES a bit
# First rename to a common 'CMS_scale_t'
cb.ForEachSyst(lambda sys: RenameSyst(cb, sys, 'CMS_scale_t', 'CMS_scale_t'))

# Then scale the constraint to 2.5%/3%:
tau_es_scaling = 2.5/3.0

cb.cp().syst_name(['CMS_scale_t']).ForEachSyst(lambda sys: sys.set_scale(tau_es_scaling))


def ChannelSpecificTauES(sys, scale=1.0):
    sys.set_name('CMS_scale_t_' + sys.channel())
    sys.set_scale(scale)

# Now clone back to a channel specific one scaled to 1.5%
ch.CloneSysts(cb.cp().syst_name(['CMS_scale_t']), cb,
              lambda sys: ChannelSpecificTauES(sys, 0.5))

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

# Then tauid, and remove it only from syst
cb.SetGroup('tauid', ['CMS_eff_t'])
cb.RemoveGroup('syst', ['CMS_eff_t'])

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
