import os, numpy, math, copy, math
from array import array
from ROOT import gStyle, TCanvas, TLegend
from officialStyle import officialStyle

from DataMCPlot import *

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)


filedict = {
    '0jet':{'filename':'htt_shapes.root'},
    'low_1jet':{'filename':'htt_shapes.root'},
    'high_1jet':{'filename':'htt_shapes.root'},
    'vbf':{'filename':'htt_shapes.root'},
    }

process = {
#    'TotalSig':{'name':'TotalSig', 'isSignal':1, 'order':1001},
    'QCD':{'name':'QCD', 'isSignal':0, 'order':1},
    'TT':{'name':'TT', 'isSignal':0, 'order':2},
    'VV':{'name':'VV', 'isSignal':0, 'order':3},
    'W':{'name':'W', 'isSignal':0, 'order':4},
    'ZJ':{'name':'ZJ', 'isSignal':0, 'order':5},
    'ZL':{'name':'ZL', 'isSignal':0, 'order':6},
    'ZTT':{'name':'ZTT', 'isSignal':0, 'order':1},
    'HiggsGGH':{'name':'HiggsGGH', 'isSignal':1, 'order':2001},
    'HiggsVBF':{'name':'HiggsVBF', 'isSignal':1, 'order':2003},
    'data':{'name':'data_obs', 'isSignal':0, 'order':2999},
}


hists = []

for key, ifile in filedict.iteritems():

    file = TFile(ifile['filename'])

    for dtype in ['postfit', 'prefit']:

        print '-'*80
        print dtype, key

        hist = DataMCPlot('h_mass_' + dtype + '_' + key)        
        hist.legendBorders = 0.6, 0.6, 0.88, 0.88

        for ii, val in process.iteritems():
            _h_ = file.Get('mt_' + key + '_' + dtype + '/' + val['name'])
            _h_.SetName(val['name'])
            _h_.GetXaxis().SetTitle('Neutral-Charge asymmetry')

            hist.AddHistogram(_h_.GetName(), _h_, val['order'])
        
            if val['name'] in ['data_obs']:
                hist.Hist(_h_.GetName()).stack = False



        hist.Group('electroweak', ['W', 'ZL', 'ZJ', 'VV'])

        canvas = TCanvas()
        hist.DrawStack('HIST', None, None, None, None, 2)

        canvas.Print('plots/' + dtype + '_' + key + '.pdf')

        print hist

