from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import sys
import math
from HX711 import *
import RPi.GPIO as GPIO
from signal import pause
import sqlite3
from gpiozero import Button as gpiobutton
from escpos import printer
from time import *
from datetime import date
from datetime import datetime

#GPIO.cleanup()
# horizontal button
bth1 = gpiobutton(16)
bth2 = gpiobutton(21)
bth3 = gpiobutton(20)
bth4 = gpiobutton(13)
bth5 = gpiobutton(6)
# vertical button
btv1 = gpiobutton(26)
btv2 = gpiobutton(19)
btv3 = gpiobutton(4)

global frame_no
global commodity_name
global batch_no
global f0
global f1
global f2
global f3
global show_weight
global total_weight
global w
global hx
global dt_string
now = datetime.now()
dt_string = now.strftime("%b/%d/%Y %H:%M:%S")

total_weight = 0.0
hx = SimpleHX711(27, 17, 198227, 114496)
frame_no = 7


def thermal():
    global commodity_name
    global batch_no
    global dt_string
    global total_weight
    total= str(total_weight)
    p= printer.Usb(0x0525, 0xa700, in_ep=0x82, out_ep=0x01)
    p.set(align='center',density=8)
    p.image("Bijak.jpeg",high_density_vertical=True,high_density_horizontal=True)
    p.set(align='center',width=1,height=1,density=8)
    p.text("Shop\n")
    p.text("Address\n")
    p.text("Phone no.\n\n")
    p.text("DATE:")
    p.text(dt_string)
    p.text("\n")
    p.text("================================\n")
    p.text("Batch Code:")
    p.text(batch_no)
    p.text("\n")
    p.text("Commodity:")
    p.text(commodity_name)
    p.text("\n")
    p.text("Total Weight:")
    p.text(total)
    p.text("\n")
    p.text("================================\n")
    p.text("\n")
    p.text("\n")
    p.text("\n")
    p.text("\n")
    p.text("\n")
    p.text("\n")
    p.text("\n")
    p.cut()

def unsetbutton():
    def none():
        print("")
    bth1.when_pressed= none
    bth2.when_pressed= none
    bth3.when_pressed= none
    bth4.when_pressed= none
    bth5.when_pressed= none
    btv1.when_pressed= none
    btv2.when_pressed= none
    btv3.when_pressed= none
    
def zero1():
    hx.zero()

def save_record():
    global commodity_name
    global batch_no
    global total_weight
    conn = sqlite3.connect('weight_recor.db')
    c = conn.cursor()
    '''c.execute("""CREATE TABLE weight (
            Batch_no integer,
            Commodity text,
            Total_weight real 
            )""")'''
    c.execute ("INSERT INTO weight VALUES (:b_no, :comm, :total)",
              {
                  'b_no':batch_no,
                  'comm':commodity_name,
                  'total':total_weight
              }
               )
    
    conn.commit()
    conn.close()

def query(no):
    def destroy(n):
        global frame_no
        global w
        global total_weight
        if n == 0:
            bth1.when_pressed = lambda:query(frame_no)
            btv1.when_pressed = cleanAndExit
            btv2.when_pressed = batchcode
            btv3.when_pressed = zero1
            top.destroy()
        
        elif n == 3:
            btv1.when_pressed = batch
            btv2.when_pressed = lambda:total(w,total_weight)
            btv3.when_pressed = zero1
            bth1.when_pressed = lambda:query(frame_no)
            bth2.when_pressed = save_record
            bth3.when_pressed = thermal
            bth4.when_pressed = batchcode
            bth5.when_pressed = main
            top.destroy()
            
    conn = sqlite3.connect('weight_recor.db')
    c = conn.cursor()
    c.execute("SELECT *, oid FROM weight")
    records = c.fetchall()
    #print(records)
    print_records = ''
    for record in records:
        print_records += str(record) + "\n"
    
    top = Toplevel()
    top.geometry("1500x1200")
    top.title('Weight Records')
    query_label = Label(top, text = print_records , font=('', 30) )
    query_label.pack()
    btn = Button(top, text="Close",font=('', 50), command =lambda:destroy(no))
    btn.pack()
    unsetbutton()
    bth1.when_pressed =lambda:destroy(no)
    print(no)
    conn.commit()
    conn.close()
    
def total(a,b):
    global total_weight
    #print (type(total_weight)) 
    b = b + a
    b = float('{:.2f}'.format(b))
    total_weight = b
    #print(b)
    
    title = Label(f3, text='{:.2f}'.format(b) + "Kg", font=('', 70))
    title.place(x=400, y=700)
    
def commo_dity(cat):
    global commodity_name
    global total_weight
    global w
    global f2
    global f3
    global batch_no
    global frame_no
    frame_no = 3
    
    f2.destroy()
    commodity_name = cat
    f3 = Frame(root)
    f3.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)
    unsetbutton()
    weight1 = Label(f3,text="Weight:-",font = ('', 100))
    weight1.place(x=0,y=0)
    weight2 = Label(f3,text="KG",font = ('', 100))
    weight2.place(x=1200,y=0)
    
    my_label = Label(f3, text=f"Batch No.      :- {batch_no}", font=('', 50))
    my_label.place(x=250, y=175)
    my_label1 = Label(f3, text=f"Commodity. :-  {cat}", font=('', 50))
    my_label1.place(x=250, y=250)
    title = Label(f3, text='Total weight[Kg]', font=('', 70))
    title.place(x=250, y=500)
    back = Button(f3, text=' Back ', fg="red", font=('', 30), pady=20, command=batch)
    back.place(x=1475, y=0)
    btv1.when_pressed = batch
    
    add_weight = Button(f3, text='Add Weight ', fg="blue", font=('', 30), pady=20, command=lambda:total(w,total_weight))
    add_weight.place(x=1350, y=470)
    btv2.when_pressed = lambda:total(w,total_weight)
    
    reset_bt = Button(f3, text='Reset', font=('', 40), pady=20, command=zero1)
    reset_bt.place(x=1450, y=900)
    btv3.when_pressed = zero1
    
    record = Button(f3, text='Record', font=('', 50), pady=20, command=lambda:query(frame_no))
    record.place(x=0, y=900)
    bth1.when_pressed = lambda:query(frame_no)
    
    save = Button(f3, text='Save', font=('', 50), pady=20, command=save_record)
    save.place(x=270, y=900)
    bth2.when_pressed = save_record
    
    
    receipt = Button(f3, text='Receipt', font=('', 50), pady=20, command=thermal)
    receipt.place(x=470, y=900)
    bth3.when_pressed = thermal
    
    
    new = Button(f3, text='New Batch', font=('', 50), pady=20, command=batchcode)
    new.place(x=770, y=900)
    bth4.when_pressed = batchcode
    
    exit_bt = Button(f3, text='Exit', font=('', 50), pady=20, command=main)
    exit_bt.place(x=1170, y=900)
    bth5.when_pressed = main

def batch():
    global f1
    global f2
    global batch_no

    if batch_no == 0:
        messagebox.showwarning("Error", "Batch No. Not Submitted")
    else:
        # f0.destroy()
        f1.destroy()
        f3.destroy()
        
        f2 = Frame(root)
        f2.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)
        unsetbutton()
        weight1 = Label(f2,text="Weight:-",font = ('', 100))
        weight1.place(x=0,y=0)
        weight2 = Label(f2,text="KG",font = ('', 100))
        weight2.place(x=1200,y=0)
        
        my_label = Label(f2, text=f"Batch No.  {batch_no}", font=('', 70))
        my_label.place(x=350, y=175)
        my_label = Label(f2, text="Select Commodity", font=('', 70))
        my_label.place(x=250, y=350)

        back = Button(f2, text=' Back ', fg="red", font=('', 30), pady=20, command=batchcode)
        back.place(x=1475, y=0)
        btv1.when_pressed = batchcode
   
        potato = Button(f2, text='Potato', font=('', 50), pady=20, command=lambda: commo_dity("Potato"))
        potato.place(x=0, y=700)
        bth1.when_pressed = lambda: commo_dity("Potato")
        
        onion = Button(f2, text='Onion', font=('', 50), pady=20, command=lambda: commo_dity("onion"))
        onion.place(x=250, y=700)
        bth2.when_pressed = lambda: commo_dity("onion")
        
        eggplant = Button(f2, text='Eggplant', font=('', 50), pady=20, command=lambda: commo_dity("eggplant"))
        eggplant.place(x=480, y=700)
        bth3.when_pressed = lambda: commo_dity("eggplant")
        
        pumpkin = Button(f2, text='Pumpkin', font=('', 50), pady=20, command=lambda: commo_dity("pumpkin"))
        pumpkin.place(x=810, y=700)
        bth4.when_pressed = lambda: commo_dity("pumpkin")
        
        ladyfinger = Button(f2, text='Ladyfinger', font=('', 50), pady=20, command=lambda: commo_dity("ladyfinger"))
        ladyfinger.place(x=1130, y=700)
        bth5.when_pressed = lambda: commo_dity("ladyfinger")

def batchcode():
    global f0
    global f1
    global f2
    global f3
    global batch_no
    global show_weight
    global total_weight
    total_weight = 0.0
    def click(number):
        current = e.get()
        e.delete(0, END)
        e.insert(0, str(current) + str(number))

    def delete():
        text = e.get()
        e.delete(0, END)
        text = text[:-1]
        e.insert(0, text)

    def action():
        global batch_no
        batch_no = e.get()
    
    #show_weight = 0
    f0.destroy()
    f2.destroy()
    f3.destroy()
    batch_no = 0
     
    f1 = Frame(root)
    f1.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)
    weight1 = Label(f1,text="Weight:-",font = ('', 100))
    weight1.place(x=0,y=0)
    weight2 = Label(f1,text="KG",font = ('', 100))
    weight2.place(x=1200,y=0)
    my_label = Label(f1, text="Enter Batch No", font=('', 70))
    my_label.place(x=330, y=200)

    e = Entry(f1, width=15,font=('', 30), borderwidth=5)
    e.place(x=450, y=350)

    btn_del = Button(f1, text="Del",font=('', 30), pady=10, command=delete)
    btn_del.place(x=1000, y=350)
    btn_1 = Button(f1, text="1",font=('', 40), pady=20,padx=30, command=lambda: click(1))
    btn_1.place(x=450, y=720)
    btn_2 = Button(f1, text="2",font=('', 40), pady=20,padx=30, command=lambda: click(2))
    btn_2.place(x=600, y=720)
    btn_3 = Button(f1, text="3",font=('', 40),pady=20,padx=30, command=lambda: click(3))
    btn_3.place(x=750, y=720)
    btn_4 = Button(f1, text="4",font=('', 40), pady=20,padx=30, command=lambda: click(4))
    btn_4.place(x=450, y=570)
    btn_5 = Button(f1, text="5",font=('', 40),pady=20,padx=30, command=lambda: click(5))
    btn_5.place(x=600, y=570)
    btn_6 = Button(f1, text="6", font=('', 40), pady=20,padx=30,command=lambda: click(6))
    btn_6.place(x=750, y=570)
    btn_7 = Button(f1, text="7",font=('', 40),pady=20,padx=30, command=lambda: click(7))
    btn_7.place(x=450, y=420)
    btn_8 = Button(f1, text="8",font=('', 40),pady=20,padx=30, command=lambda: click(8))
    btn_8.place(x=600, y=420)
    btn_9 = Button(f1, text="9",font=('', 40), pady=20,padx=30, command=lambda: click(9))
    btn_9.place(x=750, y=420)
    btn_0 = Button(f1, text="0",font=('', 40), pady=20,padx=30, command=lambda: click(0))
    btn_0.place(x=450, y=870)
    btn_submit = Button(f1, text="Submit",font=('', 37), pady=20,padx=35, command=action)
    btn_submit.place(x=600, y=870)

    back = Button(f1, text=' Back ', fg="red", font=('', 30), pady=20, command=main)
    back.place(x=1450, y=0)

    nextbtn = Button(f1,  text='Next', fg="blue", font=('', 30), pady=20, command=batch)
    nextbtn.place(x=1450, y=900)
    unsetbutton()
    btv1.when_pressed = main
    
    btv3.when_pressed = batch


def cleanAndExit():
        print("Cleaning...")
        #GPIO.cleanup()
        print("Bye!")
        root.destroy()
        root.quit()
        sys.exit()  


def main():
    
    global w
    global f0
    global f1
    global show_weight
    global frame_no
    f1.destroy()
    f2.destroy()
    f3.destroy()
    
    frame_no = 0
    def zero1():
        hx.zero()
      
        
    f0 = Frame(root)
    f0.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)
    weight1 = Label(f0,text="Weight:-",font = ('', 100))
    weight1.place(x=0,y=0)
    weight2 = Label(f0,text="KG",font = ('', 100))
    weight2.place(x=1200,y=0)
    
    sbtn = Button(f0, text=' End  ', font=('', 40), pady=40, command=cleanAndExit)
    sbtn.place(x=1425, y=0)

    reset_bt = Button(f0, text='Reset', font=('', 40), pady=20, command=zero1)
    reset_bt.place(x=1425, y=900)

    new_batch = Button(f0, text="New Batch", font=('', 40), pady=20, command=batchcode)
    new_batch.place(x=1300, y=470)

    record = Button(f0, text='Record', font=('', 50), pady=20, command=lambda: query(frame_no))
    record.place(x=270, y=900)
    #title = Label(f0, text='Weight[Kg]', font=('', 50))
    #title.place(x=120, y=100)
    unsetbutton()
    bth1.when_pressed = lambda:query(frame_no)
    btv1.when_pressed = cleanAndExit
    btv2.when_pressed = batchcode
    btv3.when_pressed = zero1
    

def core():   
        global w
    
        global hx
        hx.setUnit(Mass.Unit.KG)
        hx.zero()
        
        while True:
            
            m = float(hx.weight(1))
            x = abs(m)
            w = float('{:.1f}'.format(x))
            #b.when_pressed = reset1
            #weight = Label(root,text="Weight :- " + '{:.2f}'.format(w) + "Kg",font = ('', 100))
            weight = Label(root,text=w,font = ('', 100))
            weight.place(x=1100,y=0)
            
    
            weight.forget()
            weight.update()



root = Tk()
root.geometry("1800x1500")
root.title(u"Weight scale")
root.attributes('-fullscreen',True)
a = Image.open("Bijak300.jpeg")
photo = ImageTk.PhotoImage(a)
b = Label(root, image=photo)
b.pack(side=LEFT, anchor=NW)
f1 = Frame(root)
f1.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)
f2 = Frame(root)
f2.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)
f3 = Frame(root)
f3.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)

main()
root.after(100,core)
root.mainloop()
