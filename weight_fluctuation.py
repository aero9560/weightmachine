from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import threading
from HX711 import *
global w
#w=0.0
global hx
global weight
hx = AdvancedHX711(27, 17, 198227, 114496, Rate.HZ_80)
def core():   
        global w
        global weight
        global hx
        hx.setUnit(Mass.Unit.KG)
        hx.zero()
        '''m = float(hx.weight(1))
        x = abs(m)
        w = float('{:.1f}'.format(x))
        weight = Label(root,text=w,font = ('', 100))
        weight.place(x=300,y=200)'''
        while True:
            
            m = float(hx.weight(1))
            x = abs(m)
            w = float('{:.1f}'.format(x))
            #b.when_pressed = reset1
            #weight = Label(root,text="Weight :- " + '{:.2f}'.format(w) + "Kg",font = ('', 100))
            weight = Label(root,text=w,font = ('', 100))
            weight.place(x=300,y=200)
            weight.focus_set()
            #weight.forget()
            weight.update()
           


root = Tk()
root.geometry("800x500")
root.title("Weight scale")
sbtn = Button(root, text=' End  ', font=('', 40), pady=40)
sbtn.place(x=325, y=0)
sbtn.focus_set()
weight = Label(root,text="",font = ('', 100))
weight.place(x=300,y=200)
weight.focus_set()
#t1 = threading.Thread(target=core)
#t1.start()
root.after(100,core)

root.mainloop()