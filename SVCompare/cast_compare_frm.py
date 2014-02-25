# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class frm_compare
###########################################################################

class frm_compare ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 550,650 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		self.mnubar_main = wx.MenuBar( 0 )
		self.mnu_file = wx.Menu()
		self.mnubar_main.Append( self.mnu_file, u"File" ) 
		
		self.SetMenuBar( self.mnubar_main )
		
		bs_main = wx.BoxSizer( wx.VERTICAL )
		
		fgSizer2 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer2.AddGrowableCol( 0 )
		fgSizer2.AddGrowableRow( 4 )
		fgSizer2.SetFlexibleDirection( wx.BOTH )
		fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		fgSizer3 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer3.AddGrowableCol( 1 )
		fgSizer3.SetFlexibleDirection( wx.HORIZONTAL )
		fgSizer3.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"Reference Cast:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )
		fgSizer3.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.fp_ref = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"CNV Files|*.cnv|CALC files|*.cnv", wx.DefaultPosition, wx.Size( -1,-1 ), wx.FLP_CHANGE_DIR|wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST|wx.FLP_OPEN|wx.FLP_USE_TEXTCTRL )
		self.fp_ref.SetMinSize( wx.Size( 200,-1 ) )
		self.fp_ref.SetMaxSize( wx.Size( 500,-1 ) )
		
		fgSizer3.Add( self.fp_ref, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		ch_color_refChoices = [ u"Yellow", u"Purple", u"Black", u"Green", u"White", u"MVP", u"Launch MVP" ]
		self.ch_color_ref = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ch_color_refChoices, 0 )
		self.ch_color_ref.SetSelection( 0 )
		fgSizer3.Add( self.ch_color_ref, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"Comparison Cast:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )
		fgSizer3.Add( self.m_staticText1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.fp_comp = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"Select a file", u"CNV Files|*.cnv|CALC files|*.cnv", wx.DefaultPosition, wx.DefaultSize, wx.FLP_CHANGE_DIR|wx.FLP_DEFAULT_STYLE|wx.FLP_FILE_MUST_EXIST|wx.FLP_OPEN|wx.FLP_USE_TEXTCTRL )
		fgSizer3.Add( self.fp_comp, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		ch_color_compChoices = [ u"Yellow", u"Purple", u"Black", u"Green", u"White", u"MVP", u"Launch MVP" ]
		self.ch_color_comp = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, ch_color_compChoices, 0 )
		self.ch_color_comp.SetSelection( 0 )
		fgSizer3.Add( self.ch_color_comp, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		fgSizer2.Add( fgSizer3, 1, wx.EXPAND, 5 )
		
		bSizer3 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Latitude (ddd.xx)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		bSizer3.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.txt_lat = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( 200,-1 ), 0 )
		bSizer3.Add( self.txt_lat, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"N", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )
		bSizer3.Add( self.m_staticText5, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
		
		
		fgSizer2.Add( bSizer3, 1, wx.EXPAND, 5 )
		
		self.chk_save_output = wx.CheckBox( self, wx.ID_ANY, u"Save Output", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.chk_save_output, 0, wx.ALL, 5 )
		
		self.btn_run = wx.Button( self, wx.ID_ANY, u"Run Comparison", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer2.Add( self.btn_run, 0, wx.ALIGN_CENTER, 5 )
		
		self.txt_output = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.Size( -1,-1 ), wx.HSCROLL|wx.TE_MULTILINE|wx.TE_READONLY )
		self.txt_output.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 76, 90, 90, False, wx.EmptyString ) )
		
		fgSizer2.Add( self.txt_output, 2, wx.ALL|wx.EXPAND, 5 )
		
		
		bs_main.Add( fgSizer2, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bs_main )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.btn_run.Bind( wx.EVT_BUTTON, self.btn_run_click )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def btn_run_click( self, event ):
		event.Skip()
	

