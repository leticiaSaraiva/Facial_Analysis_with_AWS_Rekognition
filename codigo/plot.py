

import boto3,pickle
import sys
from decouple import config
import psycopg2
import cv2
import tkinter
from tkinter import messagebox
from  PIL import Image,ImageTk
import json
import socket
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from collections import Counter

class Charts:
    def __init__(self,charts):
        self.charts = charts

        self.cha = tkinter.Frame(self.charts, relief='ridge')
        self.frame5 = tkinter.Frame(self.cha, relief='ridge')

        self.frame6 = tkinter.Frame(self.cha, relief='ridge')
        self.frame7 = tkinter.Frame(self.cha, relief='ridge')
        self.frame8 = tkinter.Frame(self.cha, relief='ridge')
     
        
        self.cha.pack(fill='x')
        
      
                
 
        
        self.label_Sent = tkinter.Label(self.frame5,font=('Courier',22), text="Smiles")
        self.label_Smile = tkinter.Label(self.frame6,font=('Courier',22), text='Sentiments')
        self.label1 = tkinter.Label(self.frame7)#, image=self.img_sent)
    
        self.label2 = tkinter.Label(self.frame8)
        
        self.label2.pack(fill='x')
        self.label1.pack(fill='x')

        self.label_Sent.pack(fill='x')
        self.label_Smile.pack(fill='x')
        
        self.frame5.grid(column=0, row=0, sticky="nsew")
        self.frame6.grid(column=1, row=0, sticky="nsew")
        self.frame7.grid(column=0, row=1, sticky="nsew")  
        self.frame8.grid(column=1, row=1, sticky="nsew")  
        
        
  #      i = Image.open("smile.png") 

        self.frame = cv2.imread("graph/smile.png")
        self.img = Image.fromarray(self.frame)
        self.imgtk = ImageTk.PhotoImage(image=self.img)
        self.label1.imgtk = self.imgtk
        self.label1.configure(image=self.imgtk)
        
        self.frame = cv2.imread("graph/sentiment.png")
        self.img = Image.fromarray(self.frame)
        self.imgtk = ImageTk.PhotoImage(image=self.img)
        self.label2.imgtk = self.imgtk
        self.label2.configure(image=self.imgtk)
     


charts = tkinter.Tk()
charts.title("Photo analysis charts")
rep = Charts(charts)
charts.mainloop()
