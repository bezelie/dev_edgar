#!/usr/bin/python3
# _*_ coding: utf8 _*_
import Tkinter as Tk, ttk
from PIL import Image
import time

root = Tk.Tk()
root.title(u" レッド ")
root.geometry("600x80+20+60")

frame1 = ttk.Frame(root, width = 10, height = 10)
frame1.place(height = 80, width = 640, x = 0, y = 0)

label1 = ttk.Label(frame1, text=u"BLUE", background="#000000", foreground="#FFFFFF", font=("",20))
label1.place(x = 0, y = 0)

label12 = ttk.Label(frame1, text=u" 残念なお知らせです。プラモ用の塗料を乾燥させてしまったひとがいます。", background="#FFFFFF", foreground="#000000",font=("",20),width=200,padding=(5,10))
label12.place(x = 10, y = 20)

root2 = Tk.Tk()
root2.title(u" GREEN ")
root2.geometry("600x80+20+200")

mes2=u" 残念なお知らせです。プラモ用の塗料を乾燥させてしまったひとがいます。"
label2 = ttk.Label(root2, text=mes2, background="#FFFFFF", foreground="#000000",font=("",20),width=200,padding=(5,10))
label2.place(x = 10, y = 10)

# sub_win = Toplevel()

root.mainloop()
