import os, numpy, math, copy, math
from array import array
from ROOT import gStyle, TCanvas, TLegend
from officialStyle import officialStyle
from DisplayManager import DisplayManager
from DataMCPlot import *

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)

def comparisonPlots(hist, hists, pname='sync.pdf', isRatio=True):

    display = DisplayManager(pname, isRatio, 0.42, 0.65)
    display.Draw(hist, hists)



filedict = {
    'inclusive':{'filename':'ztt_mt_90_shapes_1.root'},
    }

process = {
#    'TotalSig':{'name':'TotalSig', 'isSignal':1, 'order':1001},
    'QCD':{'name':'QCD', 'isSignal':0, 'order':3},
    'TT':{'name':'TT', 'isSignal':0, 'order':4},
    'VV':{'name':'VV', 'isSignal':0, 'order':5},
    'W':{'name':'W', 'isSignal':0, 'order':6},
    'ZJ':{'name':'ZJ', 'isSignal':0, 'order':7},
    'ZL':{'name':'ZL', 'isSignal':0, 'order':8},
#    'ZTT':{'name':'ZTT', 'isSignal':0, 'order':1},
    'ZTT_left':{'name':'ZTT_left', 'isSignal':0, 'order':1},
    'ZTT_right':{'name':'ZTT_right', 'isSignal':0, 'order':2},
    'data':{'name':'data_obs', 'isSignal':0, 'order':2999},
}


for key, ifile in filedict.iteritems():

    file = TFile(ifile['filename'])

    for dtype in ['postfit', 'prefit']:
#    for dtype in ['postfit']:

        print '-'*80
        print dtype, key

        hist = DataMCPlot('h_mass_' + dtype + '_' + key)        
        hist.legendBorders = 0.6, 0.6, 0.88, 0.88

        hists = []
        rhist = None

        for ii, val in process.iteritems():
            _h_ = file.Get(ifile['filename'].replace('90_shapes_', '').replace('.root', '') + '_13TeV_' + dtype + '/' + val['name'])
            _h_.SetName(val['name'])
            _h_.GetXaxis().SetLabelColor(1)
            _h_.GetXaxis().SetLabelSize(0.0)


            hist.AddHistogram(_h_.GetName(), _h_, val['order'])
        
            if val['name'] in ['data_obs']:
                hist.Hist(_h_.GetName()).stack = False
                
                hists.append(_h_)
            else:
                if rhist==None:
                    rhist = copy.deepcopy(_h_)
                    rhist.GetXaxis().SetLabelSize(0.05)
                    rhist.GetXaxis().SetLabelColor(1)
                    rhist.GetXaxis().SetTitle('Neutral-Charge asymmetry')
                else:
                    rhist.Add(_h_)


        hist.Group('electroweak', ['W', 'ZL', 'ZJ', 'VV'])
        hists.insert(0, rhist)

        canvas = TCanvas()
        hist.DrawStack('HIST', None, None, None, None, 2)

#        canvas.Print('plots/' + dtype + '_' + key + '.gif')
#        canvas.Print('plots/' + dtype + '_' + key + '.pdf')

        print hist
        comparisonPlots(hist, hists, 'all_' + dtype + '.pdf')


        if dtype=='postfit':
            nL = hist.Hist('ZTT_left').Yield()
            nR = hist.Hist('ZTT_right').Yield()
            pol = ( nR - nL ) / ( nR + nL )
            error = math.sqrt( ( 1. - pol*pol) / ( nR + nL ) )
            print " --- obs. Polarisation with these cuts = ", pol, " +/- ", error


