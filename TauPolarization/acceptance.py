import copy, math
from numpy import array
#from CMGTools.H2TauTau.proto.plotter.categories_TauMu import cat_Inc
from ROOT import TFile, TH1F, TTree, gROOT, gStyle
from DisplayManager import DisplayManager
from officialStyle import officialStyle

gROOT.SetBatch(True)
officialStyle(gStyle)
gStyle.SetOptTitle(0)
gStyle.SetOptStat(0)

colours = [1, 2, 4, 6, 8, 13, 15]
styles = [1, 2, 4, 3, 5, 1, 1]

def applyHistStyle(h, i):
    h.SetLineColor(colours[i])
    h.SetMarkerColor(colours[i])
    h.SetMarkerSize(0)
    h.SetLineStyle(styles[i])
    h.SetLineWidth(2)
    h.SetStats(False)


def comparisonPlots(hists, titles, isLog=False, pname='sync.pdf', isRatio=True, isLegend=True):

    display = DisplayManager(pname, isLog, isRatio, 0.42, 0.65)
    display.draw_legend = isLegend

    display.Draw(hists, titles)


def sproducer(key, name, ivar, tree, weight_exp):

    hist = TH1F('h_' + key + '_' + name, 
                'h_' + key + '_' + name, 
                ivar['nbin'], ivar['xmin'], ivar['xmax'])

    hist.Sumw2()
    exp = '(' + ivar['sel'] + ')*' + weight_exp
        
    tree.Draw(ivar['var'] + ' >> ' + hist.GetName(), exp)
    hist.GetXaxis().SetTitle(ivar['title'])
    hist.GetYaxis().SetTitle('a.u.')
        
    return copy.deepcopy(hist)



gROOT.Macro('./functionmacro.C+g')
from ROOT import returnNLOweight

#inc_cut = '&&'.join([cat_Inc])
#inc_cut += '&& l2_decayModeFinding && l1_charge != l2_charge && mt < 40'
inc_cut = '(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_pt>20) && l1_charge != l2_charge  && mt < 40'

separate = {
    'Ainc':'1',
    'Binc_mu_iso':'(l1_reliso05<0.1)',
    'Cinc_mu_iso_id':'(l1_reliso05<0.1 && l1_muonid_medium>0.5)',
    'Dinc_mu_iso_id_pt':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19)',
    'Einc_mu_iso_id_pt_veto':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton)',
    'Finc_mu_iso_id_pt_veto_taudm':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding)',
    'Ginc_mu_iso_id_pt_veto_taudmid':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5)',
    'Hinc_mu_iso_id_pt_veto_taudmid_antimu':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5)',
    'Iinc_mu_iso_id_pt_veto_taudmid_antimu_antie':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5)',
    'Jinc_mu_iso_id_pt_veto_taudmid_antimu_antie_pt':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_pt>20)',
    'Kinc_mu_iso_id_pt_veto_taudmid_antimu_antie_pt_OS':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_pt>20) && l1_charge != l2_charge',
    'Linc_mu_iso_id_pt_veto_taudmid_antimu_antie_pt_OS_mt':inc_cut,
#    'full':inc_cut
    }
    

mH = 500

file = TFile('HiggsSUSYGG' + str(mH) + '/H2TauTauTreeProducerTauMu/tree.root')
tree = file.Get('tree')

h_w = TH1F('wacc_' + str(mH), 'wacc_' + str(mH), 60,1,61)
h_w.GetXaxis().SetTitle('tan#beta')
h_w.GetYaxis().SetTitle('#Delta(acceptance)')
h_w.Sumw2()

#h_nw = TH1F('nwacc_' + str(mH), 'nwacc_' + str(mH), 60,1,61)
#h_nw.Sumw2()


for key, sel in sorted(separate.iteritems()):
   
    hname = 'h_' + key
    h = TH1F(hname, hname, 2,0,2)
    h.Sumw2()

    exp = '(' + sel + ' && l2_gen_match==5)*weight'
#    exp = '(' + sel + ')*weight'
    tree.Draw('1 >> ' + hname, exp)

    noweight = h.GetSumOfWeights()
#    noweight_err = 0.
#    noweight = h.IntegralAndError(0,2,noweight_err)

#    for tanb in [1, 10, 15, 20, 25, 30, 50]:
    for tanb in [30]:
#    for tanb in range(1, 61):

        exp_new = '(' + sel + ' && l2_gen_match==5)*weight*returnNLOweight(' + str(mH) + ', ' + str(tanb) + ', pthiggs)'
#        exp_new = '(' + sel + ')*weight*returnNLOweight(' + str(mH) + ', ' + str(tanb) + ', pthiggs)'
        tree.Draw('1 >> ' + hname, exp_new)
        weight = h.GetSumOfWeights()

#        weight_err = 0.
#        weight = h.IntegralAndError(0,2,weight_err)

        print '-'*30
        print key, 'tanb = ', tanb, ' : No reweight =', '{0:.0f}'.format(noweight), 'weight =', '{0:.0f}'.format(weight), '=> dA = ', '{0:.3f}'.format((weight-noweight)/noweight)
    
        h_w.SetBinContent(tanb, (weight-noweight)/noweight)
        h_w.SetBinError(tanb, 0)

comparisonPlots([h_w], ['#Delta Acceptance'], False, 'Plots/compare_' + str(mH) + '_acc.pdf', False, False)



vardict = {
    'pthiggs':{'tree':'tree', 'var':'pthiggs', 'nbin':35, 'xmin':0, 'xmax':300, 'title':"Higgs p_{T} (GeV)", 'sel':'1'},
#    'l1_pt':{'tree':'tree', 'var':'l1_pt', 'nbin':35, 'xmin':0, 'xmax':300, 'title':"muon p_{T} (GeV)", 'sel':'(l1_reliso05<0.1 && l1_muonid_medium>0.5)'},
#    'l2_pt':{'tree':'tree', 'var':'l2_pt', 'nbin':35, 'xmin':0, 'xmax':300, 'title':"tau p_{T} (GeV)", 'sel':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5)'},
#    'l2_byIsolationMVArun2v1DBoldDMwLTraw':{'tree':'tree', 'var':'l2_byIsolationMVArun2v1DBoldDMwLTraw', 'nbin':35, 'xmin':-1, 'xmax':1, 'title':"tau MVA iso (BDT score)", 'sel':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding)'},
#    'n_jets':{'tree':'tree', 'var':'n_jets', 'nbin':10, 'xmin':0, 'xmax':10, 'title':"Number of jets", 'sel':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding)'},
#    'mt':{'tree':'tree', 'var':'mt', 'nbin':35, 'xmin':0, 'xmax':300, 'title':"m_{T} (GeV)", 'sel':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_pt>20) && l1_charge != l2_charge'},
    'svfit_mass':{'tree':'tree', 'var':'svfit_mass', 'nbin':35, 'xmin':0, 'xmax':1200, 'title':"SVfit mass (GeV)", 'sel':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_pt>20) && l1_charge != l2_charge && mt < 40'},
    'svfit_transverse_mass':{'tree':'tree', 'var':'svfit_transverse_mass', 'nbin':35, 'xmin':0, 'xmax':1200, 'title':"SVfit transverse mass (GeV)", 'sel':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_pt>20) && l1_charge != l2_charge && mt < 40'},
    'mt_total':{'tree':'tree', 'var':'mt_total', 'nbin':35, 'xmin':0, 'xmax':1200, 'title':"m_T total (GeV)", 'sel':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_pt>20) && l1_charge != l2_charge && mt < 40'},

#    'n_bjets':{'tree':'tree', 'var':'n_bjets', 'nbin':10, 'xmin':0, 'xmax':10, 'title':"Number of b-jets", 'sel':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_pt>20) && l1_charge != l2_charge && mt < 40'},
#    'met_pt':{'tree':'tree', 'var':'met_pt', 'nbin':35, 'xmin':0, 'xmax':500, 'title':"MVA MET (GeV)", 'sel':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_pt>20) && l1_charge != l2_charge && mt < 40'},
#    'pfmet_pt':{'tree':'tree', 'var':'pfmet_pt', 'nbin':35, 'xmin':0, 'xmax':500, 'title':"PF MET (GeV)", 'sel':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_pt>20) && l1_charge != l2_charge && mt < 40'},
#    'mvis':{'tree':'tree', 'var':'mvis', 'nbin':35, 'xmin':0, 'xmax':600, 'title':"visible Mass (GeV)", 'sel':'(l1_reliso05<0.1 && l1_muonid_medium>0.5 && l1_pt>19) && (!veto_dilepton && !veto_thirdlepton && !veto_otherlepton && l2_decayModeFinding && l2_byIsolationMVArun2v1DBoldDMwLT>3.5 && l2_againstMuon3>1.5 && l2_againstElectronMVA6>0.5 && l2_pt>20) && l1_charge != l2_charge && mt < 40'},
    }




for vkey, ivar in vardict.iteritems():

    hist_noweight = sproducer('noweight', vkey, ivar, tree, 'weight')
    hists = [copy.deepcopy(hist_noweight)]
    titles = ['PY8']

    for tanb in [1, 15, 50]:

        wexp = 'weight*returnNLOweight(' + str(mH) + ', ' + str(tanb) + ', pthiggs)'
        hist_weight = sproducer('weight_tb' + str(tanb), 
                                vkey, ivar, tree, wexp)

        hists.append(copy.deepcopy(hist_weight))
        titles.append('MSSM (tanb = ' + str(tanb) + ')')
   
    for ii, ihist in enumerate(hists):
        applyHistStyle(ihist, ii)
        ihist.Scale(1./ihist.GetSumOfWeights())
        ihist.SetMaximum(ihist.GetBinContent(ihist.GetMaximumBin())*1.2)

    comparisonPlots(hists, titles, False, 'Plots/compare_' + str(mH) + '_' + vkey + '.pdf')


