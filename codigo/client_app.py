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
import os

HOST = 'ec2-18-228-5-73.sa-east-1.compute.amazonaws.com'   # Endereco IP do Servidor
PORT = 5002           # Porta do Servidor
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)




response = ""
s3_client = boto3.client('s3')
#response = s3_client.upload_file(img_name,s3_bucket,img_name)
s3_bucket = 'ufcquixada'


class Report:
    def __init__(self,rep,username,info):
        self.rep = rep
        self.report = tkinter.Frame(self.rep, relief='ridge')
        self.frame5 = tkinter.Frame(self.report, relief='ridge')

        self.frame6 = tkinter.Frame(self.report, relief='ridge')
        self.frame7 = tkinter.Frame(self.report, relief='ridge')
        self.frame8 = tkinter.Frame(self.report, relief='ridge')
        self.frame9 = tkinter.Frame(self.report, relief='ridge')
        self.frame10 = tkinter.Frame(self.report, relief='ridge')
        self.frame11 = tkinter.Frame(self.report, relief='ridge')
        self.frame12 = tkinter.Frame(self.report, relief='ridge')
        self.frame13 = tkinter.Frame(self.report, relief='ridge')
        self.report.grid(pady=(20,40),padx=(20,20))
        self.report.pack(fill='x')
        self.frame5.grid(column=0, row=2, sticky="nsew",pady=(8,15))
        self.frame6.grid(column=0, row=1, sticky="nsew",pady=(15,9))
        self.frame7.grid(column=0, row=3, sticky="nsew",pady=1)  
        self.frame8.grid(column=0, row=4, sticky="nsew",pady=1)  
        self.frame9.grid(column=0, row=5, sticky="nsew",pady=1)
        self.frame10.grid(column=0, row=6, sticky="nsew",pady=1)
        self.frame11.grid(column=0, row=7, sticky="nsew",pady=1)  
        self.frame12.grid(column=0, row=8, sticky="nsew",pady=1)
        self.frame13.grid(column=0, row=9, sticky="nsew", pady = (0,50))
        
        self.username = tkinter.Label(self.frame5,font=('Courier',15), text ='Username: {}'.format(username ))

        self.resum_ = tkinter.Label(self.frame6,font=('Courier',22), text="Report")
        self.label_sexo = tkinter.Label(self.frame7,font=('Courier',15), text='Sex: {}, Confidence: {}'.format(info['Sex'],info['ConfS']))
        self.faixa_i = tkinter.Label(self.frame8,font=('Courier',15), text='Age range: Between {} and {}'.format(info['AgeL'],info['AgeH']))
        self.sentimento = tkinter.Label(self.frame9,font=('Courier',15), text='Predominant sentiment: {}, Confidence: {}'.format(info['Sent'], info['ConfS']))
        self.sorrindo = tkinter.Label(self.frame10,font=('Courier',15), text='Smiling: {}, Confidence: {}'.format(info['Smile'],info['ConfSmile']))
        self.glasses = tkinter.Label(self.frame11,font=('Courier',15), text='Eye Glasses: {}, Confidence: {}'.format(info['Eyeglasses'],info['EyeglassesConf']))
        self.mustache = tkinter.Label(self.frame12,font=('Courier',15), text='Mustache: {}, Confidence: {}'.format(info['Mustache'], info['MustacheConf']))
        self.eyeopen = tkinter.Label(self.frame13,font=('Courier',15), text='EyeOpen: {}, Confidence: {}'.format(info['EyeOpen'],info['EyeOpenConf']))
        
        self.resum_.pack(fill='x')
        self.username.pack(side='left')
        self.label_sexo.pack(side='left')
        self.faixa_i.pack(side='left')
        self.sentimento.pack(side='left')
        self.sorrindo.pack(side='left')
        self.glasses.pack(side='left')
        self.mustache.pack(side='left')
        self.eyeopen.pack(side='left')

class Charts:
    def __init__(self,charts):
        self.charts = charts
        self.cha = tkinter.Frame(self.charts, relief='ridge')
        self.frame5 = tkinter.Frame(self.cha, relief='ridge')

        self.frame6 = tkinter.Frame(self.cha, relief='ridge')
        self.frame7 = tkinter.Frame(self.cha, relief='ridge')
        self.frame8 = tkinter.Frame(self.cha, relief='ridge')
     
        
        self.cha.pack(fill='x')
        
      
                
        
       
        
        self.label_Sent = tkinter.Label(self.frame5,font=('Courier',22), text="Sentiments")
        self.label_Smile = tkinter.Label(self.frame6,font=('Courier',22), text='Smiles')
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
        
        
class App:
    def __init__(self,root,username):
        self.username = username
        self.root = root
        #self.frame1 = tkinter.Frame(root)
        self.frame1 = tkinter.Frame(root, borderwidth=1, relief='ridge')  
        self.frame2 = tkinter.Frame(root, borderwidth=1, relief='ridge')
        self.frame14 = tkinter.Frame(self.frame2, borderwidth=1, relief='ridge')  
        self.frame15 = tkinter.Frame(self.frame2, borderwidth=1, relief='ridge')  

        self.frame3 = tkinter.Frame(root, borderwidth=1, relief='ridge')
        self.frame11 = tkinter.Frame(root, borderwidth=1, relief='ridge')
        
        self.frame4 = tkinter.Frame(self.frame3, relief='ridge')  
        self.frame5 = tkinter.Frame(self.frame3, relief='ridge')  
        self.frame6 = tkinter.Frame(self.frame3, relief='ridge')
        self.frame7 = tkinter.Frame(self.frame3, relief='ridge')
        self.frame8 = tkinter.Frame(self.frame3, relief='ridge')
        self.frame9 = tkinter.Frame(self.frame3, relief='ridge')
        self.frame10 = tkinter.Frame(self.frame3, relief='ridge')
        
        self.frame12 = tkinter.Frame(self.frame3, relief='ridge')
        self.frame13 = tkinter.Frame(self.frame3, relief='ridge')

        self.frame1.grid(column=0, row=0, sticky="nsew")  
        self.frame2.grid(column=0, row=1, sticky="nsew") 
        self.frame14.grid(column=0, row=0, sticky="nsew") 
        self.frame15.grid(column=1, row=0, sticky="nsew")  


        self.frame3.grid(column=1, row=0, sticky="nsew")
        self.frame11.grid(column=1, row=1, sticky="nsew")
        
        
        self.frame4.grid(column=0, row=0, sticky="nsew",padx=140)  
        self.frame5.grid(column=0, row=1, sticky="nsew")  
        self.frame6.grid(column=0, row=2, sticky="nsew",pady=15)
        self.frame7.grid(column=0, row=3, sticky="nsew")  
        self.frame8.grid(column=0, row=4, sticky="nsew")  
        self.frame9.grid(column=0, row=5, sticky="nsew")
        self.frame10.grid(column=0, row=6, sticky="nsew", pady = (0,15))
        self.frame12.grid(column=0, row=8, sticky="nsew")
        self.frame13.grid(column=0, row=9, sticky="nsew")
 
        #label1 = tkinter.Label(frame1, text="Simple label")  
        #button1 = tkinter.Button(frame2, text="Simple button")  
        #button2 = tkinter.Button(frame3, text="Apply and close", command=root.destroy)
 
        
    
        self.width, self.height = 800, 600
        self.label1 = tkinter.Label(self.frame1,width=self.width,height=self.height)
        self.llaa = tkinter.Label(self.frame4,text=self.username,font=('Courier',15))
        self.button1 = tkinter.Button(self.frame14,text='Capture',command=self.press_button1,width=int(self.width/25),font=('Courier',18))
        self.button2 = tkinter.Button(self.frame15,text='Try again',command=self.press_button2,width=int(self.width/25),font=('Courier',18))
        self.button3 = tkinter.Button(self.frame5,text='Analyze',command=self.press_button_analise,font=('Courier',18))
        self.button4 = tkinter.Button(self.frame11,text='Logout',command=self.logout,font=('Courier',18))
        self.button5 = tkinter.Button(self.root)
        self.button6 = tkinter.Button(self.root)
        

    
        self.resum_ = tkinter.Label(self.frame6,font=('Courier',22), text='')
        self.label_sexo = tkinter.Label(self.frame7,font=('Courier',15), text='')
        self.faixa_i = tkinter.Label(self.frame8,font=('Courier',15), text='')
        self.sentimento = tkinter.Label(self.frame9,font=('Courier',15), text='')
        self.sorrindo = tkinter.Label(self.frame10,font=('Courier',15), text='')
        
        #self.lmain.pack()
        #self.button1.pack(side='left')
        #self.button2.pack(side='right')
        self.capture = cv2.VideoCapture(0)

        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cam_ = 1
       # self.lmain.grid(row=0,columns=1,columnspan=10,rowspan=8)
        self.label1.pack(fill='x')
        self.button1.pack(fill='x')  
        self.button2.pack(fill='x')
        self.button3.pack(fill='x')
        self.button4.pack(fill='x')
       

        self.resum_.pack(side='left')
        
        self.label_sexo.pack(side='left')
        self.faixa_i.pack(side='left')
        self.sentimento.pack(side='left')
        self.sorrindo.pack(side='left')
        
        #self.button3.pack(fill='x')#side='right')
        self.llaa.pack(fill='x',pady=10)#grid(column=1,row=0,sticky='N')#.pack(side='left')
        
    def show_frame(self):
        if(self.cam_ == 1):
            
            ret,frame = self.capture.read()
            self.frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        
            self.print_image()
        self.label1.after(10, self.show_frame)
        
    def press_button1(self):
        self.cam_ = 0
        #self.capture.release()
    def print_image(self):
        self.img = Image.fromarray(self.frame)
        self.imgtk = ImageTk.PhotoImage(image=self.img)
        self.label1.imgtk = self.imgtk
        self.label1.configure(image=self.imgtk)
    
    def press_button2(self):
        
        #self.capture = cv2.VideoCapture(0)
        #self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        #self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self.cam_ = 1
        self.resum_.config(text='')
        self.label_sexo.config(text='')
        self.faixa_i.config(text='')
        self.sentimento.config(text='')
        self.sorrindo.config(text='')
    
 #       self.nome.delete(0, 'end')
        self.button3.config(state='normal')
        self.button5.destroy()
        self.button6.destroy()

    def press_button_analise(self):
        if(self.cam_ == 1):
            messagebox.showinfo("Uncaptured photo","Capture a photo of your face before proceeding.")
  #      if(self.nome.get() == ''):
   #         messagebox.showinfo("Name's field incomplete", "Enter your name to continue the analysis.")
        else:
            buckeet = s3_client.list_objects(Bucket=s3_bucket)
           # name = self.nome.get()
            num = len(buckeet['Contents'])
            file_name = 'img{}.png'.format(num)
            self.img.save('img/'+ file_name)
            response = s3_client.upload_file('img/' + file_name,s3_bucket,file_name)
            msg_send = '1-{}-{}'.format(file_name,self.username)
            tcp.send(msg_send.encode())
            data= tcp.recv(4096)
            self.response = pickle.loads(data)
            if(self.response != ''):
                self.resum_.config(text="Analyze summary")
                self.label_sexo.config(text="Sex: {}".format(self.response['Sex']))
                #print(self.response)
                self.button3.config(state='disable')
                
                self.faixa_i.config(text='Age range: Between {} and {}'.format(self.response['AgeL'],self.response['AgeH']))
                
                
        

                self.sentimento.config(text = 'Predominant sentiment: {}'.format(self.response['Sent']))
                self.sorrindo.config(text='Smiling: {}'.format(self.response['Smile']))
                
                width = int(self.frame.shape[1] * self.response['Width'])
                height = int(self.frame.shape[0] * self.response['Height'])
                top = int(self.frame.shape[0] * self.response['Top'])
                left = int(self.frame.shape[1] * self.response['Left'])

                cv2.rectangle(self.frame,(left,top),(left+width,top+height),(0,255,0),2)
                print(self.response)
                
                self.print_image()
                self.button5 = tkinter.Button(self.frame12,text='Generate report',command=self.press_button_report,font=('Courier',18))
                self.button6 = tkinter.Button(self.frame13,text='Generate charts',command=self.press_button_charts,font=('Courier',18))
                self.button5.pack(fill='x')
                self.button6.pack(fill='x')

                
               
            else:
                messagebox.showinfo("Multiple or no faces in the image", "Capture only one face in the photo.")
    def press_button_report(self):
        
        report = tkinter.Tk()
        report.title("Photo analysis report")
        rep = Report(report,self.username,self.response)
        report.mainloop()
        
    def press_button_charts(self):
        msg_send = '4-{}-{}'.format(self.username,'')
        tcp.send(msg_send.encode())
        data= tcp.recv(10096)
        self.result = pickle.loads(data)
        if(self.result != []):
            result = pd.DataFrame(self.result,columns=['username','count','sent','smile'])
            plt.figure(figsize=(7,7))
            sentime, count = np.unique(result['sent'].values, return_counts=True)
            colors=['red','green','yellow','blue','black','pink','gray']
            plt.bar(sentime,count , color=colors[:len(sentime)] );
            #print(result['sent'].values)
            #formatter = FuncFormatter(to_percent)
            plt.ylabel('Quantity')
            plt.savefig("graph/sentiment.png");
            plt.clf() 
            
            plt.figure(figsize=(7,7))
            smi, count = np.unique(result['smile'].values, return_counts=True)
            colors=['red','green']
            if(len(count) == 2 ):
            	plt.pie(count,colors=colors , labels=['No','Yes'],autopct='%1.1f%%');
            
            elif(len(count) ==1 and smi[0] == False):
                plt.pie(count,colors=colors , labels=['No'],autopct='%1.1f%%');
            
            elif(len(count) ==1 and smi[0] == True):
                plt.pie(count,colors=colors , labels=['Yes'],autopct='%1.1f%%');
            

            print(count)
            
            plt.savefig("graph/smile.png");
            
            os.system("python plot.py")
            #charts = tkinter.Tk()
            #charts.title("Photo analysis charts")
            #rep = Charts(charts)
            #charts.mainloop()
        
        
            
    def logout(self):
        self.capture.release()

        self.root.destroy()

        login = tkinter.Tk()
        login.title("Photo analysis")
        log = Login(login)
        login.mainloop()
        
                
#window = App(root)
                
                

class Login:
    def __init__(self, root = None):
        
        self.frame1 = tkinter.Frame(root, borderwidth=0, relief='ridge')  
        self.frame2 = tkinter.Frame(root, borderwidth=0, relief='ridge')  
        self.frame3 = tkinter.Frame(root, borderwidth=0, relief='ridge')
        
        self.frame4 = tkinter.Frame(self.frame1, relief='ridge')  
        self.frame5 = tkinter.Frame(self.frame1, relief='ridge')  
        self.frame6 = tkinter.Frame(self.frame2, relief='ridge')
        self.frame7 = tkinter.Frame(self.frame2, relief='ridge')   
        self.frame8 = tkinter.Frame(self.frame3, relief='ridge')
        self.frame9 = tkinter.Frame(self.frame3, relief='ridge')
        
        self.frame1.grid(column=0, row=0, sticky="nsew",padx=45,pady=(50,0))  
        self.frame2.grid(column=0, row=1, sticky="nsew",pady=(15,50),padx=45)  
        self.frame3.grid(column=0, row=2, sticky="nsew")
        
        self.frame4.grid(column=0, row=0, sticky="nsew")  
        self.frame5.grid(column=1, row=0, sticky="nsew")  
        self.frame6.grid(column=0, row=0, sticky="nsew")
        self.frame7.grid(column=1, row=0, sticky="nsew") 
        self.frame8.grid(column=0, row=0, sticky="nsew")
        self.frame9.grid(column=1, row=0, sticky="nsew") 
        
        
        
        self.username = tkinter.Label(self.frame4,text="Username:",font=('Courier',19))
        self.password = tkinter.Label(self.frame6,text="Password:",font=('Courier',19))
        
        self.usernameEntry = tkinter.Entry(self.frame5,font=('Courier',19))
        self.passwordEntry = tkinter.Entry(self.frame7,font=('Courier',19),show="*")

        self.login = tkinter.Button(self.frame8,text='Login',command=self.press_login,font=('Courier',15),width=20)
        self.cadastrar = tkinter.Button(self.frame9,text='Register',command=self.press_register,font=('Courier',15),width=20)

        self.usernameEntry.pack(fill='x')
        self.password.pack(fill='x')
        self.passwordEntry.pack(fill='x')
        self.username.pack(fill='x')
        self.login.pack(fill='x')
        self.cadastrar.pack(fill='x')

        self.root = root
        
    def press_login(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        
        if(password != '' and username !=''):
            tcp.send('2-{}-{}'.format(username,'').encode())
            msg = tcp.recv(4096)
            
            if(msg.decode() == '1'):
                messagebox.showinfo("Error", "Username not exist")
            
            elif(msg.decode() == '2'):
                
                tcp.send(password.encode())
        
                msg = tcp.recv(4096)
                    
                if(msg.decode() == '4'):
                    messagebox.showinfo("Error", "Invalid username or password")
                elif(msg.decode() == '3'):
                    self.root.destroy()
                    root = tkinter.Tk()
                    root.title("Photo analysis")
                    app = App(root,username)
                    app.show_frame()
                    root.mainloop()
                    app.capture.release()
            
        else:
            messagebox.showinfo("Error", "Blank username or password")

                
            
        
    def press_register(self):
        username = self.usernameEntry.get()
        password = self.passwordEntry.get()
        
        if(password != '' and username !=''):
            tcp.send('3-{}-{}'.format(username,'').encode())
            msg = tcp.recv(4096)
            
            if(msg.decode() == '1'):
                messagebox.showinfo("Error", "Username exist")
            
            elif(msg.decode() == '2'):
                
                tcp.send(password.encode())
        
                msg = tcp.recv(4096)
                    
              
                if(msg.decode() == '3'):
                    self.root.destroy()
                    root = tkinter.Tk()
                    root.title("Photo analysis")
                    app = App(root,username)
                    app.show_frame()
                    root.mainloop()
                    app.capture.release()
            
        else:
            messagebox.showinfo("Error", "Blank username or password")
        




login = tkinter.Tk()
login.title("Photo analysis")
log = Login(login)
login.mainloop()
                  


