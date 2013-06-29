import wx
import wx.xrc
from cast_compare_frm import frm_compare
# import sv_compare

class CompareFrame(frm_compare):
    def __init__(self, parent):
        frm_compare.__init__(self, parent)

    def btn_run_click(self, event):
        # print self.fp_ref.GetPath()
        # print self.ch_color_ref.GetStringSelection()
        # print float(self.txt_lat.GetValue()) + 10
        sv_compare.compare_casts(self.fp_ref.GetPath(), self.fp_comp.GetPath(),
            self.ch_color_ref.GetStringSelection(),
            self.ch_color_comp.GetStringSelection(),
            float(self.txt_lat.GetValue())

def main():
    app = wx.App(0)
    app.frame = CompareFrame(None)
    app.frame.Show()
    app.MainLoop()

if __name__ == '__main__':
	main()
