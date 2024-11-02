# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Oct 26 2018)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################
import sys
sys.path.append('/home/nubia/.local/lib/python3.9/site-packages/')
import wx
import wx.xrc

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame1 ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"TelVoice", pos = wx.DefaultPosition, size = wx.Size( 983,674 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText1 = wx.StaticText( self, wx.ID_ANY, u"MyLabel", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		bSizer8.Add( self.m_staticText1, 1, wx.ALL|wx.ALIGN_LEFT, 5 )

		self.m_button51 = wx.Button( self, wx.ID_ANY, u"刷新", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer8.Add( self.m_button51, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer8, 0, wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText2 = wx.StaticText( self, wx.ID_ANY, u"次数", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		bSizer2.Add( self.m_staticText2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textCtrl1 = wx.TextCtrl( self, wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer2.Add( self.m_textCtrl1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_slider1 = wx.Slider( self, wx.ID_ANY, 10, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL )
		bSizer2.Add( self.m_slider1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer6.Add( bSizer2, 0, wx.ALIGN_CENTER_VERTICAL, 5 )

		bSizer21 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText21 = wx.StaticText( self, wx.ID_ANY, u"时长（min）", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText21.Wrap( -1 )

		bSizer21.Add( self.m_staticText21, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_textCtrl11 = wx.TextCtrl( self, wx.ID_ANY, u"10", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer21.Add( self.m_textCtrl11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_slider11 = wx.Slider( self, wx.ID_ANY, 10, 0, 100, wx.DefaultPosition, wx.Size( 200,-1 ), wx.SL_HORIZONTAL )
		bSizer21.Add( self.m_slider11, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )


		bSizer6.Add( bSizer21, 0, wx.EXPAND, 5 )

		bSizer61 = wx.BoxSizer( wx.VERTICAL )

		self.m_button5 = wx.Button( self, wx.ID_ANY, u"终止测试", wx.DefaultPosition, wx.Size( -1,40 ), 0 )
		self.m_button5.SetFont( wx.Font( 9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "宋体" ) )
		self.m_button5.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		bSizer61.Add( self.m_button5, 0, wx.ALL|wx.ALIGN_RIGHT, 5 )


		bSizer6.Add( bSizer61, 1, wx.EXPAND, 5 )


		bSizer1.Add( bSizer6, 0, wx.EXPAND, 5 )

		bSizer10 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"类型：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		bSizer10.Add( self.m_staticText4, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_choice2Choices = [ u"语音", u"视频" ]
		self.m_choice2 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_choice2Choices, 0 )
		self.m_choice2.SetSelection( 0 )
		bSizer10.Add( self.m_choice2, 0, wx.ALL, 5 )

		self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"出声部位：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		bSizer10.Add( self.m_staticText5, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_choice1Choices = [ u"听筒", u"外放", u"混合" ]
		self.m_choice1 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_choice1Choices, 0 )
		self.m_choice1.SetSelection( 0 )
		bSizer10.Add( self.m_choice1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		self.m_staticText6 = wx.StaticText( self, wx.ID_ANY, u"网络：", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		bSizer10.Add( self.m_staticText6, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )

		m_choice3Choices = [ u"5G", u"4G" ]
		self.m_choice3 = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 100,-1 ), m_choice3Choices, 0 )
		self.m_choice3.SetSelection( 0 )
		bSizer10.Add( self.m_choice3, 0, wx.ALL, 5 )


		self.m_checkBox1 = wx.CheckBox( self, wx.ID_ANY, u"第三方APP兼容启动模式", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer10.Add( self.m_checkBox1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5 )
        
		bSizer1.Add( bSizer10, 0, wx.EXPAND, 5 )

		self.m_staticline3 = wx.StaticLine( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer1.Add( self.m_staticline3, 0, wx.EXPAND |wx.ALL, 5 )

		bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_button2 = wx.Button( self, wx.ID_ANY, u"电话", wx.DefaultPosition, wx.Size( 300,200 ), 0 )
		self.m_button2.SetFont( wx.Font( 50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer7.Add( self.m_button2, 0, wx.ALL, 5 )

		self.m_button21 = wx.Button( self, wx.ID_ANY, u"微信", wx.Point( -1,-1 ), wx.Size( 300,200 ), 0 )
		self.m_button21.SetFont( wx.Font( 50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer7.Add( self.m_button21, 0, wx.ALL, 5 )

		self.m_button211 = wx.Button( self, wx.ID_ANY, u"Link+", wx.Point( -1,-1 ), wx.Size( 300,200 ), 0 )
		self.m_button211.SetFont( wx.Font( 50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

		bSizer7.Add( self.m_button211, 0, wx.ALL, 5 )


		bSizer1.Add( bSizer7, 1, wx.EXPAND, 5 )

		bSizer71 = wx.BoxSizer( wx.VERTICAL )

		self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE  )
		bSizer71.Add( self.m_textCtrl3, 1, wx.ALL|wx.EXPAND, 5 )


		bSizer1.Add( bSizer71, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()

		self.Centre( wx.BOTH )

		# Connect Events
		self.m_button51.Bind( wx.EVT_BUTTON, self.redev )
		self.m_slider1.Bind( wx.EVT_SCROLL, self.timeScroll )
		self.m_slider11.Bind( wx.EVT_SCROLL, self.timeScroll2 )
		self.m_button5.Bind( wx.EVT_BUTTON, self.bStop )
		self.m_checkBox1.Bind( wx.EVT_CHECKBOX, self.app_check )
		self.m_button2.Bind( wx.EVT_BUTTON, self.bClick )
		self.m_button21.Bind( wx.EVT_BUTTON, self.bClick2 )
		self.m_button211.Bind( wx.EVT_BUTTON, self.bClick3 )

	def __del__( self ):
		pass


	# Virtual event handlers, overide them in your derived class
	def redev( self, event ):
		event.Skip()

	def timeScroll( self, event ):
		event.Skip()

	def timeScroll2( self, event ):
		event.Skip()

	def bStop( self, event ):
		event.Skip()
		
	def app_check( self, event ):
		event.Skip()
		
	def bClick( self, event ):
		event.Skip()

	def bClick2( self, event ):
		event.Skip()

	def bClick3( self, event ):
		event.Skip()

