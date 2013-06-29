import wx
import wx.xrc
import os
from cast_compare_frm import frm_compare
if os.name != 'nt':
    import sv_compare
import os.path

#size 550x641

class CompareFrame(frm_compare):
    def __init__(self, parent):
        frm_compare.__init__(self, parent)

    def btn_run_click(self, event):
        # print self.fp_ref.GetPath()
        # print self.ch_color_ref.GetStringSelection()
        # print float(self.txt_lat.GetValue()) + 10
        self.txt_output.SetValue('')
        path = os.path.split(self.fp_ref.GetPath())[0]
        ref_color = self.ch_color_ref.GetStringSelection()
        comp_color = self.ch_color_comp.GetStringSelection()
        if ref_color == comp_color:
            result = wx.MessageDialog(self, 'Do you really want both colors to be the same?', 
                style=wx.YES_NO | wx.ICON_QUESTION).ShowModal()
            if result == wx.ID_NO:
                return

        save_output = self.chk_save_output.GetValue()
        results = sv_compare.compare_files(self.fp_ref.GetPath(),
            self.fp_comp.GetPath(), ref_color, comp_color,
            float(self.txt_lat.GetValue()), save_output)

        self.txt_output.SetValue(results[0] + '\n' + results[1])
        if save_output:
            outfile = open(os.path.join(path, sv_compare.save_name(ref_color,
                comp_color, 'txt')), 'w')
            outfile.writelines(results)


def main():
    app = wx.App(0)
    app.frame = CompareFrame(None)
    app.frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
