#!/usr/bin/env python

import CombineHarvester.CombineTools.ch as ch
import os

cb = ch.CombineHarvester()

aux_shapes   = '/afs/cern.ch/user/y/ytakahas/work/Higgs13TeV/CMSSW_7_6_3_patch2/src/CMGTools/H2TauTau/TauPolarization/'

procs = {
  'sig'  : ['ZTT_left', 'ZTT_right'],
  'bkg'  : ['VV','TT','QCD','W','ZJ','ZL']
}

cats = [(1, 'mt_inclusivemt40_cp')]
#cats = [(1, 'mt_inclusivemt40')]

cb.AddObservations(  ['*'], ['ztt'], ["13TeV"], ['mt'],               cats         )
cb.AddProcesses(     ['*'], ['ztt'], ["13TeV"], ['mt'], procs['bkg'], cats, False  )
cb.AddProcesses(     ['90'], ['ztt'], ["13TeV"], ['mt'], procs['sig'], cats, True   )

print '>> Adding systematic uncertainties...'

cb.cp().process(procs['sig'] + ['ZJ', 'ZL', 'TT', 'VV']).AddSyst(
    cb, 'CMS_eff_m', 'lnN', ch.SystMap()(1.03))

cb.cp().process(procs['sig'] + ['ZJ', 'ZL', 'TT', 'VV']).AddSyst(
    cb, 'lumi_13TeV', 'lnN', ch.SystMap()(1.027))

cb.cp().AddSyst(
    cb, 'CMS_eff_t', 'lnN', ch.SystMap('channel', 'process')
    (['mt'], procs['sig'] + ['ZTT'], 1.05))

cb.cp().AddSyst(
    cb, 'CMS_scale_t_$CHANNEL_$ERA', 'shape', ch.SystMap('channel', 'process')
        (['mt'], procs['sig'], 1.0))

cb.cp().AddSyst(
    cb, 'CMS_$ANALYSIS_boson_scale_met', 'lnN', ch.SystMap('channel', 'process')
        (['mt'], ['ZTT', 'W', 'ZL', 'ZJ'], 1.02))
cb.cp().AddSyst(
    cb, 'CMS_$ANALYSIS_boson_reso_met', 'lnN', ch.SystMap('channel', 'process')
        (['mt'], ['ZTT', 'W', 'ZL', 'ZJ'], 1.02))
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

cb.cp().process(procs['sig'] + ['ZJ', 'ZJ']).AddSyst(
    cb, 'CMS_$ANALYSIS_zjXsec_$ERA', 'lnN', ch.SystMap('channel')
        (['mt'],  1.04))

cb.cp().process(['ZL']).AddSyst(
    cb, 'CMS_$ANALYSIS_rate_mFakeTau_$ERA', 'lnN', ch.SystMap('channel')
#        (['mt'],  1.001))
        (['mt'],  2.00))
#        (['mt'],  1.50))

cb.cp().process(['ZJ']).AddSyst(
    cb, 'CMS_$ANALYSIS_zjFakeTau_$ERA', 'lnN', ch.SystMap('channel')
        (['mt'],  1.30))

#
#cb.cp().process(['TT']).AddSyst(
#    cb, 'TTnorm', 'lnN', ch.SystMap()(1.10))
#
#cb.cp().process(['VV']).AddSyst(
#    cb, 'VVnorm', 'lnN', ch.SystMap()(1.30))
#
#cb.cp().process(['QCD']).AddSyst(
#    cb, 'QCDnorm', 'lnN', ch.SystMap()(1.05))
#
#cb.cp().process(procs['sig'] + ['ZJ', 'ZL']).AddSyst(
#    cb, 'DYxs', 'lnN', ch.SystMap()(1.03))

# still need shape uncertainties

print '>> Extracting histograms from input root files...'
file = aux_shapes + 'htt_mt.inputs-sm-13TeV_mviscut.root'
#file = aux_shapes + 'htt_mt.inputs-sm-13TeV_normal.root'
#file = aux_shapes + 'htt_mt.inputs-sm-13TeV_truncate.root'

cb.cp().backgrounds().ExtractShapes(
    file, '$BIN/$PROCESS', '$BIN/$PROCESS_$SYSTEMATIC')

cb.cp().signals().ExtractShapes(
    file, '$BIN/$PROCESS$MASS', '$BIN/$PROCESS$MASS_$SYSTEMATIC')


print '>> Generating bbb uncertainties...'
bbb = ch.BinByBinFactory()
bbb.SetAddThreshold(0.0).SetFixNorm(True)
bbb.AddBinByBin(cb.cp().process(procs['sig'] + ['W', 'QCD', 'ZJ', 'ZL']), cb)

##########################################################################
# Set nuisance parameter groups
##########################################################################
# Start by calling everything syst and allsyst
cb.SetGroup('syst', ['.*'])

# Then set lumi, and remove from both of the above
cb.SetGroup('lumi', ['lumi_.*'])
cb.RemoveGroup('syst', ['lumi_.*'])


print '>> Setting standardised bin names...'
ch.SetStandardBinNames(cb)
cb.PrintAll()

writer = ch.CardWriter('$TAG/$ANALYSIS_$CHANNEL_$BINID_$ERA.txt',
                       '$TAG/common/$ANALYSIS_$CHANNEL.input.root')
writer.SetVerbosity(1)
writer.WriteCards('output/sm_cards/LIMITS', cb)

print '>> Done!'
