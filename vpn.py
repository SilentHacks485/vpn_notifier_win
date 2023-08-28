import subprocess
from tkinter import *
from tkinter import messagebox
import threading
import time
import os
import datetime
import signal
import sys

vpn_connection_log_file = "vpn_logger.txt"
#directory_name = "\\" + "vpn_log"
directory_name = os.getcwd() + "\\" + "vpn_log"
directory_path = directory_name + "\\" + vpn_connection_log_file
ping_interval = 3

global time_out


#write file macros

def write_log_file(content):

    with open(directory_path , 'a') as f:
        now = datetime.datetime.now()  
        apnow = content + " " + str(now) +"\n\n"
        
        f.write(apnow)


def write_file(content):
    
    with open("ip.txt" , 't+w') as f:

        f.write(content)

def txt_reader():

    with open("ip.txt") as f:
        lines = f.readline()
        return lines


def show_error_message(title, message , color , type):
    root = Tk()
    root.title(title)
    root.geometry("1500x900")
    enable_fullscreen(root ,True)
    root.config(bg=color)
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x_offset = (root.winfo_screenwidth() - width) // 2
    y_offset = (root.winfo_screenheight() - height) // 2
    root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
    root.attributes("-topmost" , True)
   
    w = Label(root , text =type , font=("sans" ,150) , fg="white" , bg = color)    
    w.place(relx=0.5 , rely=0.4 , anchor="center")
 
    msg = Message(root , text=message , font=("sans" , 15) , fg="white" , bg = color , width=900)
    msg.place(relx=0.5 , rely=0.55 , anchor="center")

    b = Button(root , text= "OK" , font=("sans" , 15), command=root.destroy , width=20 , height=5)

    b.place(relx=0.5 , rely=0.7 , anchor="center")

    root.mainloop()


def enable_fullscreen(root , state):
    root.attributes("-fullscreen" , state)


def submit(root):
    
    global rec_text
    rec_text=""
    rec_text = text_entry.get()
    print("Entered text:", rec_text)
    root.destroy()


def close_window(root):

    time_out  = True
    root.destroy()
    show_error_message("Input timeout" , "You did not provide connection name , press ok and enter input on the command prompt" , "blue" , "TIMEOUT")
      




def input_gui():

    root = Tk()
    root.title("Connection Input")
    root.geometry("500x350")
    enable_fullscreen(root ,False)
    root.config(bg='white')
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x_offset = (root.winfo_screenwidth() - width) // 2
    y_offset = (root.winfo_screenheight() - height) // 2
    root.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
    root.attributes("-topmost" , True)
   
    msg = Message(root , text="Enter VPN Connection Name" , font=("sans" , 15) , fg="black" , bg = 'white', width=300)
    msg.place(relx=0.5 , rely=0.25 , anchor="center")

    global text_entry
    text_entry=  Entry(root , None , font = ("sans" , 15) , fg = 'black' , bg="gray")
    text_entry.place(relx=0.5 ,  rely=0.45 , anchor = "center")

    b = Button(root , text= "Submit" , font=("sans" , 15), command=lambda:submit(root) , width=10 , height=2)
    b.place(relx=0.5 , rely=0.65 , anchor="center")

    
    cl = Button(root , text= "Close" , font=("sans" , 15), command=lambda:exit(0) , width=10 , height=2)
    cl.place(relx=0.5 , rely=0.85 , anchor="center")

    root.after(30000 , lambda:close_window(root))
    root.mainloop()



def check_vpn_connection(vpn_server):

    print("Started Notifier , to stop current batch job press Ctrl-C on terminal")


    while True:

        try:
            result = subprocess.run(["ping" , "-n", "1" , vpn_server] , stdout=subprocess.PIPE , text=True , timeout=10)

            if (result.returncode !=0):

                show_error_message("VPN Connection Error", "VPN connection to {} is unstable or unreachable . Reconnect to the VPN and press OK to monitor VPN connection.".format(vpn_server) , "red" , "WARNING")

                write_log_file("VPN CONNECTION FAILED")

            else:
                write_log_file("VPN CONNECTION STABLE")

        except subprocess.TimeoutExpired:

            write_log_file("VPN_CONNECTION TIMEDOUT")

        except KeyboardInterrupt:
             
             break

        time.sleep(ping_interval)


def create_process(vpn):
    vpn_check_thread = threading.Thread(target=check_vpn_connection(vpn_server=vpn))
    vpn_check_thread.daemon = True  # The thread will exit when the main program exits
    vpn_check_thread.start()

rec_text=0

#create file
if(not os.path.isfile("ip.txt")):
    open("ip.txt" , 'a').close()

if(not os.path.exists(directory_name)):          
    print(directory_name)
    open(directory_path , 'a').close()

while(True):

    check_if_domain_valid=0     

    try :
        
        if(txt_reader() == ""):
            
            input_gui()
        
        else:   
            rec_text = txt_reader()
            
        time.sleep(1)

        if (rec_text != 0 and rec_text !='') :
            

            check_if_domain_valid = subprocess.run(["ping", "-n", "1", rec_text], stdout=subprocess.PIPE , text=TRUE, timeout=10)
        
            if(check_if_domain_valid.returncode !=0):

                messagebox.showerror("Error", "Connection Error , name provided is not valid")
                write_file("")
                    
            else :

                write_file(rec_text)

                print("\nProcess Started")
            
                create_process(rec_text)

                #keep looping parent process
                while(True):
                    pass
        
    except KeyboardInterrupt:
            
            sys.stdout.flush()
            sys.stderr.flush()
            break
            
