from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import time
import sys
import math
from HX711 import *
import RPi.GPIO as GPIO
#from gpiozero import Button
from signal import pause
import sqlite3
from gpiozero import Button as gpiobutton
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


global commodity_name
global batch_no
global f0
global f1
global f2
global f3
global show_weight
global total_weight
global w
total_weight = 0.0

def none():
    print("")
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

def query():
    def destroy():
        bth1.when_pressed = query
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
    btn = Button(top, text="Close",font=('', 50), command = top.destroy)
    btn.pack()
    bth1.when_pressed = none
    bth2.when_pressed = destroy
    
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
    f2.destroy()
    commodity_name = cat
    f3 = Frame(root)
    f3.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)

    my_label = Label(f3, text=f"Batch No.      :- {batch_no}", font=('', 50))
    my_label.place(x=250, y=175)
    my_label1 = Label(f3, text=f"Commodity. :-  {cat}", font=('', 50))
    my_label1.place(x=250, y=250)
    title = Label(f3, text='Total weight[Kg]', font=('', 70))
    title.place(x=250, y=500)
    back = Button(f3, text=' Back ', fg="red", font=('', 30), pady=20, command=batch)
    back.place(x=1350, y=0)
    add_weight = Button(f3, text='Add Weight ', fg="blue", font=('', 30), pady=20, command=lambda:total(w,total_weight))
    add_weight.place(x=1250, y=470)
    save = Button(f3, text='Save', font=('', 50), pady=20, command=save_record)
    save.place(x=0, y=900)
    record = Button(f3, text='Record', font=('', 50), pady=20, command=save_record)
    record.place(x=270, y=900)
    new = Button(f3, text='New Batch', font=('', 50), pady=20, command=batchcode)
    new.place(x=630, y=900)
    exit_bt = Button(f3, text='Exit', font=('', 50), pady=20, command=main)
    exit_bt.place(x=1100, y=900)

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

        my_label = Label(f2, text=f"Batch No.  {batch_no}", font=('', 70))
        my_label.place(x=350, y=175)
        my_label = Label(f2, text="Select Commodity", font=('', 70))
        my_label.place(x=250, y=350)

        back = Button(f2, text=' Back ', fg="red", font=('', 50), pady=20, command=batchcode)
        back.place(x=1350, y=0)

        potato = Button(f2, text='Potato', font=('', 50), pady=20, command=lambda: commo_dity("Potato"))
        potato.place(x=0, y=700)

        onion = Button(f2, text='Onion', font=('', 50), pady=20, command=lambda: commo_dity("onion"))
        onion.place(x=250, y=700)

        eggplant = Button(f2, text='Eggplant', font=('', 50), pady=20, command=lambda: commo_dity("eggplant"))
        eggplant.place(x=480, y=700)

        pumpkin = Button(f2, text='Pumpkin', font=('', 50), pady=20, command=lambda: commo_dity("pumpkin"))
        pumpkin.place(x=810, y=700)

        ladyfinger = Button(f2, text='Ladyfinger', font=('', 50), pady=20, command=lambda: commo_dity("ladyfinger"))
        ladyfinger.place(x=1130, y=700)


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

    my_label = Label(f1, text="Enter Batch No", font=('', 70))
    my_label.place(x=330, y=200)

    e = Entry(f1, width=15,font=('', 30), borderwidth=5)
    e.place(x=450, y=350)

    btn_del = Button(f1, text="Del",font=('', 30), pady=10, command=delete)
    btn_del.place(x=1000, y=350)
    btn_1 = Button(f1, text="1",font=('', 30), pady=10, command=lambda: click(1))
    btn_1.place(x=520, y=620)
    btn_2 = Button(f1, text="2",font=('', 30), pady=10, command=lambda: click(2))
    btn_2.place(x=620, y=620)
    btn_3 = Button(f1, text="3",font=('', 30), pady=10, command=lambda: click(3))
    btn_3.place(x=720, y=620)
    btn_4 = Button(f1, text="4",font=('', 30), pady=10, command=lambda: click(4))
    btn_4.place(x=520, y=520)
    btn_5 = Button(f1, text="5",font=('', 30), pady=10, command=lambda: click(5))
    btn_5.place(x=620, y=520)
    btn_6 = Button(f1, text="6", font=('', 30), pady=10,command=lambda: click(6))
    btn_6.place(x=720, y=520)
    btn_7 = Button(f1, text="7",font=('', 30),pady=10, command=lambda: click(7))
    btn_7.place(x=520, y=420)
    btn_8 = Button(f1, text="8",font=('', 30),pady=10, command=lambda: click(8))
    btn_8.place(x=620, y=420)
    btn_9 = Button(f1, text="9",font=('', 30), pady=10, command=lambda: click(9))
    btn_9.place(x=720, y=420)
    btn_0 = Button(f1, text="0",font=('', 30), pady=10, command=lambda: click(0))
    btn_0.place(x=520, y=720)
    btn_submit = Button(f1, text="Submit",font=('', 27), pady=10, command=action)
    btn_submit.place(x=620, y=720)

    back = Button(f1, text=' Back ', fg="red", font=('', 30), pady=20, command=main)
    back.place(x=1350, y=0)

    nextbtn = Button(f1,  text='Next', fg="blue", font=('', 30), pady=20, command=batch)
    nextbtn.place(x=1350, y=900)


def main():
    global w
    global f0
    global f1
    global show_weight
    f1.destroy()
    f2.destroy()
    f3.destroy()
    
    def zero1():
        hx.zero()
    
    def cleanAndExit():
        print("Cleaning...")
        #GPIO.cleanup()
        print("Bye!")
        root.destroy()
        root.quit()
        sys.exit()   
        
    f0 = Frame(root)
    f0.pack(fill='both', expand=True, padx=0, pady=0, side=TOP)
    
    
    sbtn = Button(f0, text=' End  ', font=('', 40), pady=40, command=cleanAndExit)
    sbtn.place(x=1350, y=0)

    reset_bt = Button(f0, text='Reset', font=('', 40), pady=20, command=zero1)
    reset_bt.place(x=1350, y=900)

    new_batch = Button(f0, text="New Batch", font=('', 40), pady=20, command=batchcode)
    new_batch.place(x=1250, y=470)

    record = Button(f0, text='Record', font=('', 50), pady=20, command=query)
    record.place(x=270, y=900)
    #title = Label(f0, text='Weight[Kg]', font=('', 50))
    #title.place(x=120, y=100)
    
    bth1.when_pressed = query
    btv1.when_pressed = cleanAndExit
    btv2.when_pressed = batchcode
    btv3.when_pressed = zero1
    

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
root.mainloop()
