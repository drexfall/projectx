#-----------------------------------------Importing Modules-----------------------------------------------------------------------------------------------------------------------------------#
#kivy layouts
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition, WipeTransition, CardTransition,SlideTransition
#kivy widgets
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
#kivy others
from kivy.properties import NumericProperty
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.atlas import Atlas
from kivy.app import App
#basic math algorithm
import solve

Window.size = (320, 470)
Window.top  = 200
Window.left  = 500

#-----------------------------------------False Variables-------------------------------------------------------------------------------------------------------------------------------------#
radian_toggle                   = 0
inverse_toggle                  = 0
base                            = ''
theme                           = 0
entry_list                      = []
clipbut                         = []
hover_var                       = 0
inverse_var                     = 0
button_variable_list            =[]
drop_button_variable_list       =[]
current_page                    = 'standard'
key_pressed                     = ''
scroll_position                 =[]
scroll_bar                      = []
width_calc                      = 0
#-----------------------------------------Text Lists------------------------------------------------------------------------------------------------------------------------------------------#
shift_keys                      ={'`':'~', '1':'!', '4':'$', '5':'%', '6':'^', '7':'&', '8':'x', '9':'(', '0':')', '=':'+', '\\':'|', '.':'>', ',':'<'}

button_text_standard_inverse    =(                                     'Del'   ,   'AC',
                                    '÷'     ,   '1'     ,   '2'     ,   '3'     ,   '%' ,         
                                    'x'     ,   '4'     ,   '5'     ,   '6'     ,   'a²' ,
                                    '+'     ,   '7'     ,   '8'     ,   '9'     ,   '√a' ,
                                    '-'     ,   '('     ,   '0'     ,   ')'     ,   'a!' ,
                                                            '.'                        )
button_text_scientific_inverse  =(                          'INV'   ,   'Deg'   ,   'Del',  'AC',
                                    'sin'   ,   'cos'   ,   'tan'   ,   'cosec' ,   'sec',  'cot',                        
                                    '÷'     ,   '1'     ,   '2'     ,   '3'     ,   'π'  ,  'log',        
                                    'x'     ,   '4'     ,   '5'     ,   '6'     ,   'e'  ,  'a²',
                                    '+'     ,   '7'     ,   '8'     ,   '9'     ,   'a!' ,  '⌈a⌉',
                                    '-'     ,   '('     ,   '0'     ,   ')'     ,   '|a|',  '⌊a⌋',
                                               '±'     ,   '.'      ,   '%'                  )
mode_dropdown_text              =('standard',
                                  'scientific',
                                  'algebraic',
                                  'converter')
#-----------------------------------------Functions------------------------------------------------------------------------------------------------------------------------------------------#        
    
def on_mouse_pos(self,pos,**kwargs):
    global c
    
    for x in button_variable_list :
        
        if x.collide_point(*pos) and hover_var==0:
            Window.set_system_cursor('arrow')
            x.background_color =(0.5, 0.5, 0.5, 0.3)   

        else:
            x.background_color =(0, 0, 0, 0)
    
    for x in entry_list :
        
        if x.parent.parent.collide_point(*pos):
            Window.set_system_cursor('ibeam')
            
      
def drop_event(self,*largs):
    global hover_var
    hover_var = 1
    self.drop.open(self.btn2)
    
    for x in button_variable_list:
        x.disabled=True
        x.background_color =(0,0,0,0)
          
def drop_close(self,*largs):
    global hover_var
    hover_var = 0
    for x in button_variable_list:
        x.disabled=False
        x.background_color =(0, 0, 0, 1)

def clipfunc(self,func):
    
    if func == 'copy':
        if entry_list[0].selection_text == '':
            entry_list[0].copy(entry_list[0].text)
        else:
            entry_list[0].copy()

    elif func =='cut':
        if entry_list[0].selection_text == '':
            entry_list[0].copy(entry_list[0].text)
            entry_list[0].text = ''
        else:
            entry_list[0].cut()
            
    elif func =='paste':
        entry_list[0].paste()
        
class Text(TextInput):
    minimum_width = NumericProperty(1)

    def on_cursor(self, instance, newPos):
        self.width = max(self.minimum_width,self.parent.width)

        if not (isinstance(self.parent, ScrollView) and self.multiline):
            return super(Text, self).on_cursor(instance, newPos)
        if newPos[0] == 0:
            self.parent.scroll_x = 0
        else:
            over_width = self.width - self.parent.width
            if over_width <= 0.0:
                return super(Text, self).on_cursor(instance, newPos)
            view_start = over_width * self.parent.scroll_x
            view_end = view_start + self.parent.width
            offset = self.cursor_offset()
            desired_view_start = offset - 5
            desired_view_end = offset + self.padding[0] + self.padding[2] + self.cursor_width + 5
            if desired_view_start < view_start:
                self.parent.scroll_x = max(0, desired_view_start / over_width)
            elif desired_view_end > view_end:
                self.parent.scroll_x = min(1, (desired_view_end - self.parent.width) / over_width)
        return super(Text, self).on_cursor(instance, newPos)

    def insert_text(self, substring, from_undo=False):
        global key_pressed
        
        if len(substring)>1 and substring.isnumeric() == True:
            for x in substring:
                self.insert_text(x)

    
        button_text = substring

        if button_text in ('=','\r','\n'):

            self.text=solve.Basic(self.text)[0]
            key_pressed = '='
            
            return
        
        elif button_text == 'AC':
            self.text = ''
        elif button_text == 'Del':
            print(key_pressed)
            if key_pressed in ('=','\r','\n'):
                self.text =''
            else:
                self.do_backspace()

        elif (button_text == '0' ) and self.text=='0':
            button_text=''
            
        if button_text == '/':
                button_text = '÷'
                
        if key_pressed in ['÷','x','+','-','','.'] and button_text in ['÷','x','+','-','','.']:
            if key_pressed == button_text:
                button_text = ''

            elif key_pressed != button_text:
                self.insert_text('Del')
            
        
        if button_text in ['0','1','2','3','4','5','6','7','8','9','!','%','(',')','+','-','÷','x','.']:
            if key_pressed in ('=','\r','\n'):
                self.text = ''
            key_pressed = button_text
            return super(Text, self).insert_text(button_text, from_undo=from_undo)

  
            
    def on_text(self, instance, newText):

        width_calc = 0

        for line_label in self._lines_labels:

            width_calc = max(width_calc, line_label.width + 90)   

        self.minimum_width = width_calc
        self.focus = True
        self.parent.scroll_x = 1

        if len(self.text)>15 and self.text.isnumeric() == False:
            self.font_size = '25sp'
        else:
            self.font_size='75sp'

    
    def keyboard_on_key_up(self,window,keycode):

        if (key_pressed == '=' and keycode[1] == 'backspace') or keycode[1] == 'delete':
            self.insert_text('AC')
        key, key_str = keycode
        k = self.interesting_keys.get(key)
        if k:
            key = (None, None, k, 1)
            self._key_up(key)

        
    def on_touch_up(self, touch):

        if self.collide_point(*touch.pos):
            
            if touch.button == 'scrollup': 
                self.calc_plus()
            elif touch.button == 'scrolldown': 
                self.calc_minus()
        try:
            touch.push()
            self.transform_touch(touch)
            for child in self.content.children:
                if ref(child) in touch.grab_list:
                    touch.grab_current = child
                    break
            return super(TextInputCutCopyPaste, self).on_touch_up(touch)
        except:
            touch.pop()
                
    def calc_plus(self):
        self.do_cursor_movement('cursor_left')
        if self.parent.scroll_x !=0:
            self.parent.scroll_x -= 0.05
    def calc_minus(self):
        self.do_cursor_movement('cursor_right')
        if self.parent.scroll_x !=1:
            self.parent.scroll_x += 0.05

#-----------------------------------------Standard Mode Page----------------------------------------------------------------------------------------------------------------------------------#
class Main(BoxLayout):
    def focus_time(self,x=None,y=None):
        
        self.entry.insert_text('4')
        self.entry.do_backspace()
        self.entry.unfocus_on_touch = False
    def __init__(self,**kwargs):
        super(Main,self).__init__(**kwargs)
        self.orientation='vertical'
        self.float = RelativeLayout(size_hint=(1,0.8))
        self.box1 = ScrollView(size_hint=(1,1),
                               effect_cls = 'ScrollEffect',
                               bar_width = 0,
                               do_scroll_y = False
                               )
        self.entry = Text(
                          size_hint= (None,1),
                           base_direction='rtl',
                           padding=[20,70,20,0],
                           font_size='75sp')
        

        entry_list.append(self.entry)
        self.box1.add_widget(self.entry)

        for width,name,index in ((.05,'copy',0),(.15,'cut',1),(.25,'paste',2)):
            self.but = Button(text = name,
                               size_hint = (0.1,0.15),
                              font_size = '10sp',
                               pos_hint={'x':width, 'y':.8})
            x = self.but
            x.bind(on_release=lambda x=x:clipfunc(self,func=x.text))
            self.float.add_widget(self.but,index=index)
            clipbut.append(self.but)

        self.float.add_widget(self.box1,index = 3)
        self.add_widget(self.float)
        Clock.schedule_once(self.focus_time,1)
        self.entry.bind(on_touch_up = self.focus_time)

        self.butgrid=StackLayout(orientation='lr-tb',size_hint=(1,1),pos_hint ={"x":0.01, "y":0.05})
        self.butgrid.cols=5
        self.butgrid.rows=6
        self.add_widget(self.butgrid)

        button_text_var = 0
        for x in range(27):

            if x == 0:
                self.drop = DropDown(**kwargs)
                self.drop.container.spacing = [-5,-5]
                self.btn1 = None
                dropvar = self.btn1
                self.btn2 = Button(text='standard',size_hint=(0.396,0.165),background_color =(0,0,0,1))
                for index in range(4):
                    if mode_dropdown_text[index] != self.btn2.text:
                        
                        dropvar = Button(text =mode_dropdown_text[index], size_hint_y = None, height=30,background_color =(0,0,0,1)) 
                        dropvar.bind(on_release = lambda dropvar=dropvar: self.drop.select(dropvar.text)) 
                        self.drop.add_widget(dropvar)
                        drop_button_variable_list.append(dropvar)
                
                self.btn2.bind(on_release=lambda self:drop_event(self.parent.parent))
                button_variable_list.append(self.btn2)

                self.butgrid.add_widget(self.btn2)
                self.drop.bind(on_press=lambda instance, x: setattr(self.btn2, 'text', x))

                self.drop.bind(on_dismiss=drop_close)

            elif x == 1:
                self.btn = Button(size_hint=(0.196,0.165),background_color =(0, 0, 0, 1),
                                  disabled=True)
                self.butgrid.add_widget(self.btn)
            elif x == 24:
                self.btnChange = Button(text='...',
                                  size_hint=(0.39,0.165),background_color =(0, 0, 0, 0))
                button_variable_list.append(self.btnChange)
                self.butgrid.add_widget(self.btnChange)

            elif x == 26:
                self.btn = Button(text='=',
                                  size_hint=(0.39,0.165),background_color =(0, 0, 0, 0))
                self.btn.bind(on_release=lambda self:self.parent.parent.entry.insert_text('='))
                button_variable_list.append(self.btn)
                self.butgrid.add_widget(self.btn)
            else:
                self.btn = Button(text=button_text_standard_inverse[button_text_var],
                                  size_hint=(0.196,0.165),
                                  background_color =(0, 0, 0, 0),
                                  background_normal='atlas://Themes/theme/button',
                                  background_down='atlas://Themes/theme/button_pressed')
                button_variable_list.append(self.btn)
                zbut=self.btn
                zbut.bind(on_release=lambda zbut=zbut:self.entry.insert_text(zbut.text))
                self.butgrid.add_widget(self.btn)

                button_text_var+=1


#-----------------------------------------Scientific Mode Page--------------------------------------------------------------------------------------------------------------------------------#
class Scientific(BoxLayout):
    def focus_time(self,x=None,y=None):
        
        self.entry.insert_text('4')
        self.entry.do_backspace()
        self.entry.unfocus_on_touch = False
    def __init__(self,**kwargs):
        
        super(Scientific, self).__init__(**kwargs)

        self.orientation='vertical'
        self.float = RelativeLayout(size_hint=(1,0.8))
        self.box1 = ScrollView(size_hint=(1,1),
                               effect_cls = 'ScrollEffect',
                               bar_width = 0,
                               do_scroll_y = False
                               )
        self.entry = Text(
                          size_hint= (None,1),
                           base_direction='rtl',
                           padding=[20,70,20,0],
                           font_size='75sp')
        

        entry_list.append(self.entry)
        self.box1.add_widget(self.entry)

        for width,name,index in ((.05,'copy',0),(.15,'cut',1),(.25,'paste',2)):
            self.but = Button(text = name,
                               size_hint = (0.1,0.15),
                              font_size = '10sp',
                               pos_hint={'x':width, 'y':.8})
            x = self.but
            x.bind(on_release=lambda x=x:clipfunc(self,func=x.text))
            self.float.add_widget(self.but,index=index)
            clipbut.append(self.but)

        self.float.add_widget(self.box1,index = 3)
        self.add_widget(self.float)
        Clock.schedule_once(self.focus_time,1.5)
        self.entry.bind(on_touch_up = self.focus_time)

        self.butgrid=StackLayout(orientation='lr-tb',size_hint=(1,1),pos_hint ={"x":0.01, "y":0.05})
        self.butgrid.cols=6
        self.butgrid.rows=7
        self.add_widget(self.butgrid)
        
        button_text_var = 0
        for x in range(40):
            if x==0:
                self.drop = DropDown(**kwargs)
                self.btn1 = None
                dropvar = self.btn1
                self.btn2 = Button(text='scientific',size_hint=(0.330,0.141),background_color =(0,0,0,1))
                for index in range(4):
                    if mode_dropdown_text[index] != self.btn2.text:
                        
                        dropvar = Button(text =mode_dropdown_text[index], size_hint_y = None, height=30,background_color =(0,0,0,1)) 
                        dropvar.bind(on_release = lambda dropvar=dropvar: self.drop.select(dropvar.text)) 
                        self.drop.add_widget(dropvar)
                        drop_button_variable_list.append(dropvar)

                self.btn2.bind(on_release=lambda self:drop_event(self.parent.parent))
                button_variable_list.append(self.btn2)

                self.butgrid.add_widget(self.btn2)
                self.drop.bind(on_press=lambda instance, x: setattr(self.btn2, 'text', x))

                self.drop.bind(on_dismiss=drop_close)

            elif x == 35:
                self.btnChange = Button(text='...',
                                  size_hint=(0.163,0.141),background_color =(0, 0, 0, 0))
                button_variable_list.append(self.btnChange)
                self.butgrid.add_widget(self.btnChange)

            elif x == 39:
                self.btn = Button(text='=',
                                  size_hint=(0.30,0.141),background_color =(0, 0, 0, 0))
                self.btn.bind(on_release=lambda self:self.parent.parent.entry.insert_text('='))
                button_variable_list.append(self.btn)
                self.butgrid.add_widget(self.btn)
            else:
                self.btn = Button(text=button_text_scientific_inverse[button_text_var],
                                  size_hint=(0.163,0.141),
                                  background_color =(0, 0, 0, 0),
                                  background_normal='atlas://Themes/theme/button',
                                  background_down='atlas://Themes/theme/button_pressed')
                button_variable_list.append(self.btn)
                zbut=self.btn
                zbut.bind(on_release=lambda zbut=zbut:self.entry.insert_text(zbut.text))
                self.butgrid.add_widget(self.btn)

                button_text_var+=1

#-----------------------------------------Algebraic Mode Page--------------------------------------------------------------------------------------------------------------------------------#
class Algebraic(BoxLayout):
    def __init__(self,**kwargs):

        super(Algebraic, self).__init__(**kwargs)
        self.orientation='vertical'
        self.entry = TextInput(base_direction='rtl',
                               padding=[0,70,0,0],
                               font_size='75sp',
                               size_hint_x= None,
                                width=320,
                               multiline=False,
                               cursor=(0,0),
                               focus = True,
                               scroll_x=1)
        self.entry.bind(on_touch_up=lambda y,x: cursor_position_func(cur = self.entry.cursor_col))
        self.add_widget(self.entry)

        self.butgrid=StackLayout(orientation='lr-tb',size_hint=(1,1),pos_hint ={"x":0.01, "y":0.05})
        self.butgrid.cols=5
        self.butgrid.rows=6
        self.add_widget(self.butgrid)
        
        button_text_var = 0
        for x in range(27):
            if x == 0:
                self.drop = DropDown(**kwargs)
                self.btn1 = None
                dropvar = self.btn1
                
                for index in range(4):
                    
                    dropvar = Button(text =mode_dropdown_text[index], size_hint_y = None, height=30,background_color =(0,0,0,1)) 
                    dropvar.bind(on_release = lambda dropvar=dropvar: self.drop.select(dropvar.text)) 
                    self.drop.add_widget(dropvar)
                    drop_button_variable_list.append(dropvar)
                self.btn2 = Button(text="scientific",size_hint=(0.396,0.165),background_color =(0,0,0,1))
                self.btn2.bind(on_release=self.drop.open)
                self.add_widget(self.btn2)
                self.drop.bind(on_select=lambda instance, x: setattr(self.btn2, 'text', x))

            elif x == 1:
                    self.btn = Button(size_hint=(0.196,0.165),background_color =(0, 0, 0, 1),
                                      disabled=True)
                    self.butgrid.add_widget(self.btn)
            elif x == 24:
                self.btnChange = Button(text='...',
                                  size_hint=(0.39,0.165),background_color =(0, 0, 0, 0))
                button_variable_list.append(self.btnChange)
                self.butgrid.add_widget(self.btnChange)

            elif x == 26:
                self.btn = Button(text='=',
                                  size_hint=(0.39,0.165),background_color =(0, 0, 0, 0))
                button_variable_list.append(self.btn)
                self.butgrid.add_widget(self.btn)
            else:
                self.btn = Button(text=button_text_scientific_inverse[button_text_var],
                                  size_hint=(0.196,0.165),
                                  background_color =(0, 0, 0, 0),
                                  background_normal='atlas://Themes/theme/button',
                                  background_down='atlas://Themes/theme/button_pressed')
                button_variable_list.append(self.btn)
                zbut=self.btn
                zbut.bind(on_press=lambda zbut=zbut:self.solve_area(but=zbut))
                self.butgrid.add_widget(self.btn)

                button_text_var+=1

#-----------------------------------------Converter Page--------------------------------------------------------------------------------------------------------------------------------#
class Converter(BoxLayout):

    def __init__(self,**kwargs):
        super(Converter,self).__init__()
        self.btnChange = Button(text = 'Hi')
        self.add_widget(self.btnChange)

#-----------------------------------------Settings Page---------------------------------------------------------------------------------------------------------------------------------------#
class Settings(BoxLayout):
    def __init__(self,**kwargs):

        super(Settings, self).__init__(**kwargs)
        self.btnChange = Button(text='...',
                        size_hint=(0.39,0.165),
                          background_color =(0, 0, 0, 0))

        self.add_widget(self.btnChange)

#-----------------------------------------Screen Setup Area-------------------------------------------------------------------------------------------------------------------------------------#
class ScreenSetup(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenSetup, self).__init__(**kwargs)

        self.main_screen = Screen(name="standard")
        self.settings_screen = Screen(name="settings")
        self.scientific_screen = Screen(name="scientific")
        self.algebraic_screen = Screen(name="algebraic")
        self.converter_screen = Screen(name="converter")
        
        self.add_widget(self.main_screen)
        self.add_widget(self.settings_screen)
        self.add_widget(self.scientific_screen)
        self.add_widget(self.algebraic_screen)
        self.add_widget(self.converter_screen)

        main = Main()
        main.btnChange.bind(on_press=self.change_screen_settings)
        scientific = Scientific()
        scientific.btnChange.bind(on_press=self.change_screen_settings)
        algebraic = Algebraic()
        algebraic.btnChange.bind(on_press=self.change_screen_settings)
        converter = Converter()
        converter.btnChange.bind(on_press=self.change_screen_settings)
        
        for x in drop_button_variable_list :
            x.bind(on_press=lambda x=x:self.change_screen_drop(screen_mode=x.text))
            
        self.main_screen.add_widget(main)
        self.scientific_screen.add_widget(scientific)
        self.algebraic_screen.add_widget(algebraic)
        self.converter_screen.add_widget(converter)
        
        settings = Settings()
        settings.btnChange.bind(on_press=self.change_screen_settings)
        self.settings_screen.add_widget(settings)

        
    def change_screen_settings(self, *args):
        global current_page
        
        
        
        if self.current!='settings':
            self.transition=CardTransition(duration=0.2,direction = 'right',mode='push')
            current_page = self.current
            self.current = "settings"
        else:
            self.transition=CardTransition(duration=0.2,direction = 'left',mode='pop')
            self.current = current_page
    def change_screen_drop(self, screen_mode, *args):
        global current_page
        self.transition=WipeTransition(duration=0.2)
        self.current = screen_mode
        current_page = screen_mode

#-----------------------------------------Actual App Calling----------------------------------------------------------------------------------------------------------------------------------#            
class MyApp(App):
    def build(self):

        Window.bind(mouse_pos= lambda self,pos:on_mouse_pos(self,pos))
        Window.bind(on_resize = lambda self,x,y :entry_list[0].parent.parent.parent.focus_time())
        Window.bind(on_maximize = lambda self :entry_list[0].parent.parent.parent.focus_time())
        return ScreenSetup()
        
MyApp().run()
