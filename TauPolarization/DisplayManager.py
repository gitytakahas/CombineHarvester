import ROOT
import copy

def createRatioCanvas(name, errorBandFillColor=14, errorBandStyle=3354):
    cv = ROOT.TCanvas(name.replace('.pdf', ''), name.replace('.pdf', ''), 10, 10, 600, 600)

    # this is the tricky part...
    # Divide with correct margins
    cv.Divide(1, 2, 0.0, 0.0)

    # Set Pad sizes
    cv.GetPad(1).SetPad(0.0, 0.32, 1., 1.0)
    cv.GetPad(2).SetPad(0.0, 0.00, 1., 0.34)

    cv.GetPad(1).SetFillStyle(4000)
    cv.GetPad(2).SetFillStyle(4000)

    # Set pad margins 1
    cv.cd(1)
    ROOT.gPad.SetTopMargin(0.08)
    ROOT.gPad.SetLeftMargin(0.12)
    ROOT.gPad.SetBottomMargin(0.03)
    ROOT.gPad.SetRightMargin(0.1)

    # Set pad margins 2
    cv.cd(2)
    ROOT.gPad.SetBottomMargin(0.35)
    ROOT.gPad.SetLeftMargin(0.12)
    ROOT.gPad.SetRightMargin(0.1)

    bogyHist = ROOT.TH1F("PseudoHist", "", 1, 1., 2.)
    bogyHist.SetFillColor(errorBandFillColor)
    bogyHist.SetFillStyle(errorBandStyle)
    bogyHist.SetLineColor(0)

    cv.cd(1)
    return cv


class DisplayManager(object):

    def __init__(self, name, ratio, xmin=0.42, ymin=0.6):

        if ratio:
            self.canvas = createRatioCanvas(name.replace('pdf', ''))
        else:
            self.canvas = ROOT.TCanvas(name.replace('.pdf', ''))

        self.name = name
        self.draw_ratio = ratio
        self.histo = None
        self.histos = []
        self.pullRange = 0.5


    def Draw(self, histo, histos):

        self.histo = histo
        self.histo.DrawStack('HIST', None, None, None, None, 2)

        self.histos = histos

        pull_histos = []

        if self.draw_ratio:
            self.canvas.cd(2)

            for ihist in range(1, len(self.histos)):
                histPull = copy.deepcopy(self.histos[ihist])
                pull_histos.append(histPull)
                histPull.Divide(self.histos[0])
                histPull.UseCurrentStyle()

                histPull.SetLineColor(self.histos[ihist].GetLineColor())
                histPull.SetMarkerColor(self.histos[ihist].GetLineColor())
                histPull.SetMarkerSize(self.histos[ihist].GetMarkerSize())
                histPull.SetLineStyle(self.histos[ihist].GetLineStyle())
                histPull.SetLineWidth(self.histos[ihist].GetLineWidth())

                histPull.GetYaxis().SetRangeUser(-self.pullRange + 1., self.pullRange + 1.)

                # defaultYtoPixel = 408.  # height in pixels of default canvas
                defaultYtoPixel = self.canvas.GetPad(1).YtoPixel(0.)
                pad2YtoPixel = float(self.canvas.GetPad(2).YtoPixel(0))
                pad2XaxisFactor = defaultYtoPixel / pad2YtoPixel

#                print 'Pad size : ', self.histos[0].GetXaxis().GetLabelSize(), pad2XaxisFactor
                histPull.GetXaxis().SetLabelSize(self.histos[0].GetXaxis().GetLabelSize()*pad2XaxisFactor)
                histPull.GetXaxis().SetLabelOffset(self.histos[0].GetXaxis().GetLabelOffset()*pad2XaxisFactor)
                histPull.GetXaxis().SetTitleSize(self.histos[0].GetXaxis().GetTitleSize()*pad2XaxisFactor)
                histPull.GetXaxis().SetTitleOffset(self.histos[0].GetXaxis().GetTitleOffset()/pad2XaxisFactor*2.5)

                histPull.GetYaxis().SetLabelSize(self.histos[0].GetYaxis().GetLabelSize()*pad2XaxisFactor)
                histPull.GetYaxis().SetLabelOffset(self.histos[0].GetYaxis().GetLabelOffset()*pad2XaxisFactor)
                histPull.GetYaxis().SetTitleSize(self.histos[0].GetYaxis().GetTitleSize()*pad2XaxisFactor)
                histPull.GetYaxis().SetTitleOffset(0.8*self.histos[0].GetYaxis().GetTitleOffset()/pad2XaxisFactor)

#                histos[0].GetYaxis().SetTitleOffset(1.15)

                histPull.GetYaxis().CenterTitle()
                histPull.GetXaxis().SetTickLength(histPull.GetXaxis().GetTickLength()*pad2XaxisFactor)
                histPull.GetYaxis().SetNdivisions(306)

                print 'check : ', 0.8*self.histos[0].GetYaxis().GetTitleOffset()/pad2XaxisFactor
                histPull.GetYaxis().SetTitleOffset(0.55)
                histPull.GetYaxis().SetTitle("Ratio")
                histPull.GetXaxis().SetTitle("Neutral Charge Asymmetry")
                histPull.GetXaxis().SetTitleOffset(1.2)
                histPull.SetTitle('')
                if ihist == 1:
                    histPull.Draw("ep")
                else:
                    histPull.Draw("same ep")

                line = ROOT.TLine(histPull.GetXaxis().GetXmin(), 1, histPull.GetXaxis().GetXmax(), 1)
                line.SetLineStyle(2)
                line.Draw()

            # This is a little bit ugly though ...

            for i, h in enumerate(self.histos):
                h.GetXaxis().SetLabelSize(0)

            self.canvas.cd(1)

        self.canvas.Update()
        self.canvas.Print(self.name)
        self.canvas.Print(self.name.replace('pdf','gif'))
