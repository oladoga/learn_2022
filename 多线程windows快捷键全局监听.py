# _*_ coding:UTF-8 _*_  
import win32con
import ctypes
import ctypes.wintypes
import threading
import win32clipboard as winClipboard
import pyautogui

RUN=False #用来传递运行一次的参数
EXIT = False #用来传递退出的参数

user32 = ctypes.windll.user32  #加载user32.dll
id1=105 #注册热键的唯一id，用来区分热键
id2=106


class Hotkey(threading.Thread):
    def init(self):
        self.FLAGz = 0  #创建一个Thread.threading的扩展类   

    def calc(self,num):
        

        num_final =float(num) 
        self.result =round((num * 1.2),2)
        return self.result


    def get_clipboard_data(self):
        winClipboard.OpenClipboard()
        self.num = winClipboard.GetClipboardData()
        try:
            float(self.num)
            print(self.num)
            winClipboard.CloseClipboard()
            return float(self.num)
            
        except:
            winClipboard.CloseClipboard()
            pass


    def put_result_on_clipboard(self,text):
        winClipboard.OpenClipboard()
        winClipboard.EmptyClipboard()
        winClipboard.SetClipboardText(text, winClipboard.CF_TEXT )
        winClipboard.CloseClipboard()

    def run(self):  
        global EXIT  #定义全局变量，这个可以在不同线程间共用。
        global RUN  #定义全局变量，这个可以在不同线程间共用。

        if not user32.RegisterHotKey(None, id1, 0, win32con.VK_F9):   # 注册快捷键F9并判断是否成功，该热键用于执行一次需要执行的内容。  
            print ("Unable to register id"), id1 # 返回一个错误信息

        if not user32.RegisterHotKey(None, id2, 0, win32con.VK_F10):   # 注册快捷键F10并判断是否成功，该热键用于结束程序，且最好这么结束，否则影响下一次注册热键。  
            print ("Unable to register id"), id2

        #以下为检测热键是否被按下，并在最后释放快捷键  
        try:  
            msg = ctypes.wintypes.MSG()  

            while True:
                if user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:

                    if msg.message == win32con.WM_HOTKEY:  
                        if msg.wParam == id1:
                            pyautogui.hotkey('ctrl','c')

                            number = self.get_clipboard_data()
                            if self.FLAGz == 0:
                                if number != None:
                                    calculated_Num =  self.calc(number)
                                    print(calculated_Num)
                                    self.put_result_on_clipboard(str(calculated_Num))
                                    self.FLAGz = 1
                            else:
                                self.FLAGz = 0
                                pyautogui.alert('你还没有按F10粘贴，请重新去F9复制！')
                                

                    
                        elif msg.wParam == id2:
                            pyautogui.hotkey('ctrl','v')
                            self.FLAGz = 0
                            
                            
                            
                    user32.TranslateMessage(ctypes.byref(msg))  
                    user32.DispatchMessageA(ctypes.byref(msg))

        finally:
            user32.UnregisterHotKey(None, id1)                             
            user32.UnregisterHotKey(None, id2)


hotkey = Hotkey() 
hotkey.init ()
hotkey.start()  

while(True):
    if RUN==True:
        RUN=False

