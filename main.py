from email.message import EmailMessage
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import random
import smtplib
import sys
import tempfile
import threading
import time
from typing import Optional
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from ttkbootstrap.widgets.scrolled import ScrolledFrame, ScrolledText
from ttkbootstrap.widgets import ToastNotification

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_data_dir():
    base_dir = os.path.join(os.getenv("APPDATA"), "RetailBillingApp")
    bills_dir = os.path.join(base_dir, "bills")
    os.makedirs(bills_dir, exist_ok=True)
    return bills_dir

BILLS_DIR = get_data_dir()

# if not os.path.exists('bills'):
#     os.mkdir('bills') 

mailWindow: Optional[ttk.Toplevel] = None
def send_email():
    def send_mail_job():
        msg = EmailMessage()
        msg['Subject'] = 'Retail Bill'
        msg['From'] = senderGmailEntry.get()
        msg['To'] = recipientEmailEntry.get()
        msg.set_content('Please find your bill attached')
        msg.add_attachment(messageArea.get('1.0',END).encode('utf-8'),maintype='text', 
        subtype='plain', 
        filename='Customer_Bill.txt')
        try:
            with smtplib.SMTP(host='smtp.gmail.com',port=587) as server:
                server.starttls()
                server.login(senderGmailEntry.get(), passwordEntry.get())
                server.send_message(msg)
            root.after(0, lambda: show_success_toast('Mail Sent'))
        except:
            root.after(0, lambda: show_success_toast('Unable to sent Mail. Something Went Wrong!'))
        finally:
            def cleanup():
                sendButton.config(state='normal')
                if mailWindow and mailWindow.winfo_exists():
                    mailWindow.destroy()
            root.after(0, cleanup)
            
    def sendAction():
        sendButton.config(state='disabled')
        thread = threading.Thread(
            target=send_mail_job,
            daemon=True
        ).start()
    global mailWindow
    if billTextArea.get('1.0', END) == '\n':
        show_error_toast('Bill is empty')
    elif mailWindow is None or not mailWindow.winfo_exists():
        mailWindow = ttk.Toplevel(title='New Title', size=(1000, 600))
        mailWindow.grab_set()
        container = ScrolledFrame(mailWindow, padding=10, autohide=True)
        container.pack(fill='both', expand=True)
        senderFrame = ttk.Labelframe(container, text='Sender', padding=(20,0))
        senderFrame.pack(fill='x', anchor='n')
        senderFrame.columnconfigure(1, weight=1)
        senderGmailLabel = ttk.Label(senderFrame, text="Gmail ID")
        senderGmailLabel.grid(row=0, column=0, pady=20, padx=10, sticky='w')
        senderGmailEntry = ttk.Entry(senderFrame)
        senderGmailEntry.grid(row=0, column=1, sticky='ew',pady=20)
        
        passwordLabel = ttk.Label(senderFrame, text="Password")
        passwordLabel.grid(row=1, column=0, pady=20,padx=10,sticky='w')
        passwordEntry = ttk.Entry(senderFrame)
        passwordEntry.grid(row=1, column=1, sticky='ew',pady=20)

        recipientFrame = ttk.Labelframe(container, text='Recipient', padding=(20,0))
        recipientFrame.pack(fill='x', anchor='n', pady=20)
        recipientFrame.columnconfigure(1, weight=1)
        recipientEmailLabel = ttk.Label(recipientFrame, text="Email Address")
        recipientEmailLabel.grid(row=0, column=0, pady=20, padx=10, sticky='w')
        recipientEmailEntry = ttk.Entry(recipientFrame)
        recipientEmailEntry.grid(row=0, column=1, sticky='ew',pady=20)
        messageLabel = ttk.Label(recipientFrame, text="Message")
        messageLabel.grid(row=1, column=0, pady=20, padx=10, sticky='nw')
        messageArea = ScrolledText(recipientFrame,autohide=True, height=10, width=45, font=('Consolas', 11),)
        messageArea.grid(row=1, column=1, pady=20, sticky='ew')
        messageArea.delete('1.0', END)
        messageArea.insert('1.0',billTextArea.get('1.0',END))
        sendButton = ttk.Button(recipientFrame, text='Send', command=sendAction)
        sendButton.grid(row=2, column=0, columnspan=2, sticky='ew', ipadx=20, ipady=10, pady=20)
        mailWindow.mainloop()
    else:
        mailWindow.deiconify()
        mailWindow.lift()


def saveBill(billnumber):
  result = Messagebox.yesno(message='Do you want to save this bill?',title='Confirm')
  if result:
    bill_content = billTextArea.get('1.0',END)
    with open(os.path.join(BILLS_DIR, f"{billnumber}.txt"), 'w') as f:
        f.write(bill_content)
    billnumberEntry['values'] = [i.split('.')[0] for i in os.listdir(BILLS_DIR)]
    show_success_toast('Bill saved!')
    

def total():
    global soapPrice, facecreamPrice,hairsprayPrice,hairgelPrice,bodylotionPrice, facewashPrice
    global riceprice, daalPrice, oilPrice, sugerPrice, teaPrice, wheatPrice
    global maazaPrice, frootiPrice, dewPrice, pepsiPrice, spritePrice, cocacolaPrice,totalBill
    soapPrice = int(bathsoapEntry.get()) * 20
    facecreamPrice = int(facecreamEntry.get()) * 50
    facewashPrice = int(facewashEntry.get()) * 100
    hairsprayPrice = int(hairsprayEntry.get()) * 150
    hairgelPrice = int(hairgelEntry.get()) * 80
    bodylotionPrice = int(bodylotionEntry.get()) * 60
    totalcosmeticPrice = soapPrice+facecreamPrice+facewashPrice+hairsprayPrice+hairgelPrice+bodylotionPrice
    cosmeticPriceEntry.delete(0,END)
    cosmeticPriceEntry.insert(0,totalcosmeticPrice)
    cosmeticTax = totalcosmeticPrice*0.12
    cosmeticTaxEntry.delete(0, END)
    cosmeticTaxEntry.insert(0, f'{cosmeticTax:.2f}')
    
    riceprice = int(riceEntry.get()) * 30
    daalPrice = int(daalEntry.get()) * 100
    oilPrice = int(oilEntry.get()) * 120
    sugerPrice = int(sugerEntry.get()) * 50
    teaPrice = int(teaEntry.get()) * 140
    wheatPrice = int(wheatEntry.get()) * 80
    totalGroceryPrice = riceprice+daalPrice+oilPrice+sugerPrice+teaPrice+wheatPrice
    groceryPriceEntry.delete(0,END)
    groceryPriceEntry.insert(0, totalGroceryPrice)
    groceryTax = totalGroceryPrice * 0.12
    groceryTaxEntry.delete(0, END)
    groceryTaxEntry.insert(0, f'{groceryTax:.2f}')
    
    maazaPrice = int(maazaEntry.get()) * 30
    frootiPrice = int(frootiEntry.get()) * 30
    dewPrice = int(dewEntry.get()) * 30
    pepsiPrice = int(pepsiEntry.get()) * 30
    spritePrice = int(spriteEntry.get()) * 30
    cocacolaPrice = int(cocacolaEntry.get()) * 30
    totalColdDrinkPrice = maazaPrice + frootiPrice + dewPrice + pepsiPrice + spritePrice + cocacolaPrice
    coldDrinkPriceEntry.delete(0, END)
    coldDrinkPriceEntry.insert(0, totalColdDrinkPrice)
    colddrinkTax = totalColdDrinkPrice * 0.08
    coldDrinkTaxEntry.delete(0, END)
    coldDrinkTaxEntry.insert(0, f'{colddrinkTax:.2f}')
    totalBill = totalcosmeticPrice+totalGroceryPrice+totalColdDrinkPrice+groceryTax+cosmeticTax+colddrinkTax
    show_success_toast('Successfully added!')

def get_bill_number():
    randnumber = random.randint(10, 99)
    curtime = time.strftime("%y%m%d%H%M%S")
    billnumber = f'{randnumber}{curtime}'
    return billnumber

def safe_num(val, target_type="int", default=None):
    try:
        if target_type == 'int':
            return int(float(val))
        elif target_type == 'float':
            return float(val)
    except:
        return default


def only_numbers(P):
    if P == "":
        return True
    try:
        if P == ".":
            return True
        float(P)
        return True
    except ValueError:
        return False

def print_bill():
    if not billTextArea.get('1.0', END).strip():
        show_error_toast('Bill is empty')
        return
    with tempfile.NamedTemporaryFile(mode='w',suffix='.txt',delete=False) as tf:
        tf.write(billTextArea.get('1.0', END))
        tmp_file = tf.name
        try:
            os.startfile(tmp_file, 'print')
            def cleanup():
                time.sleep(30)
                if os.path.exists(tmp_file):
                    os.remove(tmp_file)

        except Exception as e:
            show_error_toast(f'Printing failed! {e}')

def search_bill():
    if not billnumberEntry.get() == '':
        try:
            with open(os.path.join(BILLS_DIR, f"{billnumberEntry.get()}.txt"), 'r') as f:
                    billTextArea.delete('1.0', END)
                    billTextArea.insert('1.0',f.read())
        except:
            show_error_toast('Bill not found')

def bill_area():
    if nameEntry.get() == '' or phoneEntry.get() == '':
        show_error_toast('Customer details are required!')
    elif not (safe_num(cosmeticPriceEntry.get()) or safe_num(groceryPriceEntry.get()) or safe_num(coldDrinkPriceEntry.get())):
        show_error_toast('No products selected!')
    else:
        billTextArea.delete('1.0', END)
        billTextArea.insert(END, f'{"**Welcome Customer**":^45}\n\n') # Centered header
        billnumber = get_bill_number()
        billTextArea.insert(END, f'Bill Number: {billnumber}\n')
        billTextArea.insert(END, f'Customer Name: {nameEntry.get()}\n')
        billTextArea.insert(END, f'Customer Phone No.: {phoneEntry.get()}\n')
        billTextArea.insert(END, '='*45 + '\n')
        billTextArea.insert(END, f'{"Product":<16}{"Quantity":<10}{"Price":>10}\n')
        billTextArea.insert(END, '='*45 + '\n')
        if safe_num(bathsoapEntry.get()):
            billTextArea.insert(END, f'{"Bath Soap":<16}{bathsoapEntry.get():<10}{soapPrice:>10}\n')
        if safe_num(hairsprayEntry.get()):
            billTextArea.insert(END, f'{"Hair Spray":<16}{hairsprayEntry.get():<10}{hairsprayPrice:>10}\n')
        if safe_num(hairgelEntry.get()):
            billTextArea.insert(END, f'{"Hair Gel":<16}{hairgelEntry.get():<10}{hairgelPrice:>10}\n')
        if safe_num(facecreamEntry.get()):
            billTextArea.insert(END, f'{"Face Cream":<16}{facecreamEntry.get():<10}{facecreamPrice:>10}\n')
        if safe_num(facewashEntry.get()):
            billTextArea.insert(END, f'{"Face Wash":<16}{facewashEntry.get():<10}{facewashPrice:>10}\n')
        if safe_num(bodylotionEntry.get()):
            billTextArea.insert(END, f'{"Body Lotion":<16}{bodylotionEntry.get():<10}{bodylotionPrice:>10}\n')
        if safe_num(riceEntry.get()):
            billTextArea.insert(END, f'{"Rice":<16}{riceEntry.get():<10}{riceprice:>10}\n')
        if safe_num(oilEntry.get()):
            billTextArea.insert(END, f'{"Oil":<16}{oilEntry.get():<10}{oilPrice:>10}\n')
        if safe_num(daalEntry.get()):
            billTextArea.insert(END, f'{"Daal":<16}{daalEntry.get():<10}{daalPrice:>10}\n')
        if safe_num(wheatEntry.get()):
            billTextArea.insert(END, f'{"Wheat":<16}{wheatEntry.get():<10}{wheatPrice:>10}\n')
        if safe_num(sugerEntry.get()):
            billTextArea.insert(END, f'{"Sugar":<16}{sugerEntry.get():<10}{sugerPrice:>10}\n')
        if safe_num(teaEntry.get()):
            billTextArea.insert(END, f'{"Tea":<16}{teaEntry.get():<10}{teaPrice:>10}\n')
        if safe_num(maazaEntry.get()):
            billTextArea.insert(END, f'{"Maaza":<16}{maazaEntry.get():<10}{maazaPrice:>10}\n')
        if safe_num(pepsiEntry.get()):
            billTextArea.insert(END, f'{"Pepsi":<16}{pepsiEntry.get():<10}{pepsiPrice:>10}\n')
        if safe_num(spriteEntry.get()):
            billTextArea.insert(END, f'{"Sprite":<16}{spriteEntry.get():<10}{spritePrice:>10}\n')
        if safe_num(dewEntry.get()):
            billTextArea.insert(END, f'{"Dew":<16}{dewEntry.get():<10}{dewPrice:>10}\n')
        if safe_num(frootiEntry.get()):
            billTextArea.insert(END, f'{"Frooti":<16}{frootiEntry.get():<10}{frootiPrice:>10}\n')
        if safe_num(cocacolaEntry.get()):
            billTextArea.insert(END, f'{"Coca Cola":<16}{cocacolaEntry.get():<10}{cocacolaPrice:>10}\n')
        if safe_num(cosmeticTaxEntry.get()) or safe_num(groceryTaxEntry.get()) or safe_num(coldDrinkTaxEntry.get()):
            billTextArea.insert(END, '-'*45 + '\n')
        if safe_num(cosmeticTaxEntry.get()):
            billTextArea.insert(END, f'{"Cosmetic Tax":<28}{cosmeticTaxEntry.get():>10}\n')
        if safe_num(groceryTaxEntry.get()):
            billTextArea.insert(END, f'{"Grocery Tax":<28}{groceryTaxEntry.get():>10}\n')
        if safe_num(coldDrinkTaxEntry.get()):
            billTextArea.insert(END, f'{"Cold Drink Tax":<28}{coldDrinkTaxEntry.get():>10}\n')
        if totalBill:
            billTextArea.insert(END, '-'*45 + '\n')
            billTextArea.insert(END, f'{"Total Bill":<28}{totalBill:>10.2f}\n')
            billTextArea.insert(END, '-'*45 + '\n')
        saveBill(billnumber)
             
root = ttk.Window(themename='solar')
root.state('zoomed')
root.resizable(False, False)

def show_success_toast(message, parent=root):
    toast = ToastNotification(
        title='Success',
        message=message,
        position=(10, 60, "ne"),
        duration=3000,
        alert=False,
        iconfont=("", 12),
        bootstyle=SUCCESS,
        master = parent        
    )
    toast.show_toast()

def show_error_toast(message, parent=root):
    toast = ToastNotification(
        title='Error',
        message=message,
        position=(10, 60, "ne"),
        duration=3000,
        alert=True,
        iconfont=("", 12),
        bootstyle=DANGER,
        master = parent  
    )
    toast.show_toast()

root.title('Retail Billing Software')
validate_cmd = root.register(only_numbers)

main_scrolled_frame = ScrolledFrame(root, autohide=True)
main_scrolled_frame.pack(fill=BOTH, expand=YES)

root.iconbitmap(resource_path('assets/icon.ico'))
style = ttk.Style()
style.configure('.', font=("Helvetica", 11))
img = ttk.PhotoImage(file=resource_path('assets/img1.png'))
ttk.Label(main_scrolled_frame, text='Retail Billing Software'.upper(), image=img, bootstyle='dark-inverse', \
           anchor='center', padding=4, font=("",14), compound='left').pack(fill='x')

customer_details_frame = ttk.Labelframe(main_scrolled_frame, text='Customer Details', padding=20)
customer_details_frame.pack(fill='x', padx=20, pady=10)

nameLabel = ttk.Label(customer_details_frame, text='Name')
nameEntry = ttk.Entry(customer_details_frame)
nameLabel.grid(row=0, column=0,padx=10)
customer_details_frame.columnconfigure(1, weight=1)
nameEntry.grid(row=0, column=1, padx=10, sticky='ew')

phoneLabel = ttk.Label(customer_details_frame, text='Phone')
phoneEntry = ttk.Entry(customer_details_frame, validate='key')
phoneLabel.grid(row=0, column=2, padx=10)
customer_details_frame.columnconfigure(3, weight=1)
phoneEntry.grid(row=0, column=3, padx=10, sticky='ew')

billnumberLabel = ttk.Label(customer_details_frame, text='Bill Number')
all_bill_numbers = [i.split('.')[0] for i in os.listdir(BILLS_DIR)]
billnumberEntry = ttk.Combobox(
    customer_details_frame, 
    values=all_bill_numbers, 
    state="readonly",
    width=20
)
# billnumberEntry = ttk.Entry(customer_details_frame, width=20, validate='key', validatecommand=(validate_cmd,'%P'))
customer_details_frame.columnconfigure(4, weight=1)
billnumberLabel.grid(row=0, column=4, padx=10, sticky='e')
billnumberEntry.grid(row=0, column=5, padx=10, sticky='e')
searchBtn = ttk.Button(customer_details_frame, text='Search', bootstyle=PRIMARY, command=search_bill)
searchBtn.grid(row=0, column=6, padx=10)

productsFrame = ttk.Frame(main_scrolled_frame, padding=6)
productsFrame.pack(fill='x')
productsFrame.columnconfigure(0,weight=1, uniform='productframe')
productsFrame.columnconfigure(1,weight=1, uniform='productframe')
productsFrame.columnconfigure(2,weight=1, uniform='productframe')
# productsFrame.columnconfigure(3,weight=1, uniform='productframe')

cosmeticsFrame = ttk.Labelframe(productsFrame, text='Cosmetics', padding=20)
cosmeticsFrame.grid(row=0, column=0, sticky='senw')
cosmeticsFrame.columnconfigure(1, weight=1)

bathsoapLabel = ttk.Label(cosmeticsFrame, text='Bath Soap')
bathsoapEntry = ttk.Entry(cosmeticsFrame, validate='key', validatecommand=(validate_cmd,'%P'))
bathsoapLabel.grid(row=0, column=0, padx=20, sticky='w')
bathsoapEntry.grid(row=0, column=1, sticky='ew', pady=10)
bathsoapEntry.insert(0,0)

facecreamLabel = ttk.Label(cosmeticsFrame, text='Face Cream')
facecreamEntry = ttk.Entry(cosmeticsFrame, validate='key', validatecommand=(validate_cmd,'%P'))
facecreamLabel.grid(row=1, column=0, padx=20, sticky='w')
facecreamEntry.grid(row=1, column=1, sticky='ew',pady=10)
facecreamEntry.insert(0,0)

facewashLabel = ttk.Label(cosmeticsFrame, text='Face Wash')
facewashEntry = ttk.Entry(cosmeticsFrame, validate='key', validatecommand=(validate_cmd,'%P'))
facewashLabel.grid(row=2, column=0, padx=20, sticky='w')
facewashEntry.grid(row=2, column=1, sticky='ew',pady=10)
facewashEntry.insert(0,0)

hairsprayLabel = ttk.Label(cosmeticsFrame, text='Hair Spray')
hairsprayEntry = ttk.Entry(cosmeticsFrame, validate='key', validatecommand=(validate_cmd,'%P'))
hairsprayLabel.grid(row=3, column=0, padx=20, sticky='w')
hairsprayEntry.grid(row=3, column=1, sticky='ew',pady=10)
hairsprayEntry.insert(0,0)

hairgelLabel = ttk.Label(cosmeticsFrame, text='Hair Gel')
hairgelEntry = ttk.Entry(cosmeticsFrame, validate='key', validatecommand=(validate_cmd,'%P'))
hairgelLabel.grid(row=4, column=0, padx=20, sticky='w')
hairgelEntry.grid(row=4, column=1, sticky='ew',pady=10)
hairgelEntry.insert(0,0)

bodylotionLabel = ttk.Label(cosmeticsFrame, text='Body Lotion')
bodylotionEntry = ttk.Entry(cosmeticsFrame, validate='key', validatecommand=(validate_cmd,'%P'))
bodylotionLabel.grid(row=5, column=0, padx=20, sticky='w')
bodylotionEntry.grid(row=5, column=1, sticky='ew',pady=10)
bodylotionEntry.insert(0,0)


groceryFrame = ttk.Labelframe(productsFrame, text='grocery', padding=20)
groceryFrame.grid(row=0, column=1, sticky='esnw', padx=10)
groceryFrame.columnconfigure(1, weight=1)

riceLabel = ttk.Label(groceryFrame, text='Rice')
riceEntry = ttk.Entry(groceryFrame, validate='key', validatecommand=(validate_cmd,'%P'))
riceLabel.grid(row=0, column=0, padx=20, sticky='w')
riceEntry.grid(row=0, column=1, sticky='ew',pady=10)
riceEntry.insert(0,0)

oilLabel = ttk.Label(groceryFrame, text='Oil')
oilEntry = ttk.Entry(groceryFrame, validate='key', validatecommand=(validate_cmd,'%P'))
oilLabel.grid(row=1, column=0, padx=20, sticky='w')
oilEntry.grid(row=1, column=1, sticky='ew',pady=10)
oilEntry.insert(0,0)

daalLabel = ttk.Label(groceryFrame, text='Daal')
daalEntry = ttk.Entry(groceryFrame, validate='key', validatecommand=(validate_cmd,'%P'))
daalLabel.grid(row=2, column=0, padx=20, sticky='w')
daalEntry.grid(row=2, column=1, sticky='ew',pady=10)
daalEntry.insert(0,0)

wheatLabel = ttk.Label(groceryFrame, text='Wheat')
wheatEntry = ttk.Entry(groceryFrame, validate='key', validatecommand=(validate_cmd,'%P'))
wheatLabel.grid(row=3, column=0, padx=20, sticky='w')
wheatEntry.grid(row=3, column=1, sticky='ew',pady=10)
wheatEntry.insert(0,0)

sugerLabel = ttk.Label(groceryFrame, text='Suger')
sugerEntry = ttk.Entry(groceryFrame, validate='key', validatecommand=(validate_cmd,'%P'))
sugerLabel.grid(row=4, column=0, padx=20, sticky='w')
sugerEntry.grid(row=4, column=1, sticky='ew',pady=10)
sugerEntry.insert(0,0)

teaLabel = ttk.Label(groceryFrame, text='Tea')
teaEntry = ttk.Entry(groceryFrame, validate='key', validatecommand=(validate_cmd,'%P'))
teaLabel.grid(row=5, column=0, padx=20, sticky='w')
teaEntry.grid(row=5, column=1, sticky='ew',pady=10)
teaEntry.insert(0,0)

drinksFrame = ttk.Labelframe(productsFrame, text='Cold Drinks', padding=20)
drinksFrame.grid(row=0, column=2, sticky='esnw', padx=10)
drinksFrame.columnconfigure(1, weight=1)

maazaLabel = ttk.Label(drinksFrame, text='Maaza')
maazaEntry = ttk.Entry(drinksFrame, validate='key', validatecommand=(validate_cmd,'%P'))
maazaLabel.grid(row=0, column=0, padx=20, sticky='w')
maazaEntry.grid(row=0, column=1, sticky='ew',pady=10)
maazaEntry.insert(0,0)

pepsiLabel = ttk.Label(drinksFrame, text='Pepsi')
pepsiEntry = ttk.Entry(drinksFrame, validate='key', validatecommand=(validate_cmd,'%P'))
pepsiLabel.grid(row=1, column=0, padx=20, sticky='w')
pepsiEntry.grid(row=1, column=1, sticky='ew',pady=10)
pepsiEntry.insert(0,0)

spriteLabel = ttk.Label(drinksFrame, text='Sprite')
spriteEntry = ttk.Entry(drinksFrame, validate='key', validatecommand=(validate_cmd,'%P'))
spriteLabel.grid(row=2, column=0, padx=20, sticky='w')
spriteEntry.grid(row=2, column=1, sticky='ew',pady=10)
spriteEntry.insert(0,0)

dewLabel = ttk.Label(drinksFrame, text='Dew')
dewEntry = ttk.Entry(drinksFrame, validate='key', validatecommand=(validate_cmd,'%P'))
dewLabel.grid(row=3, column=0, padx=20, sticky='w')
dewEntry.grid(row=3, column=1, sticky='ew',pady=10)
dewEntry.insert(0,0)

frootiLabel = ttk.Label(drinksFrame, text='Frooti')
frootiEntry = ttk.Entry(drinksFrame, validate='key', validatecommand=(validate_cmd,'%P'))
frootiLabel.grid(row=4, column=0, padx=20, sticky='w')
frootiEntry.grid(row=4, column=1, sticky='ew',pady=10)
frootiEntry.insert(0,0)

cocacolaLabel = ttk.Label(drinksFrame, text='Coca Cola')
cocacolaEntry = ttk.Entry(drinksFrame, validate='key', validatecommand=(validate_cmd,'%P'))
cocacolaLabel.grid(row=5, column=0, padx=20, sticky='w')
cocacolaEntry.grid(row=5, column=1, sticky='ew',pady=10)
cocacolaEntry.insert(0,0)

billFrame = ttk.Frame(productsFrame)
billFrame.grid(row=0, column=3, sticky='nsew')
# billFrame.columnconfigure(0, weight=1)

billLabel =  ttk.Label(billFrame, text='Bill Area', bootstyle='light-inverse', anchor='center', padding=10)
billLabel.pack(fill='x')

billTextArea = ScrolledText(billFrame, height=15, width=45, font=('Consolas', 11), autohide=True)
billTextArea.pack()

# scrollbar = ttk.Scrollbar(billFrame, bootstyle="round", orient=VERTICAL)
# scrollbar.grid(row=1,column=1, sticky='ns')
# scrollbar.config(command=textarea.yview)
# textarea.config(yscrollcommand=scrollbar.set)

billmenuFrame = ttk.Labelframe(main_scrolled_frame, text='Bill Menu', padding=10)
billmenuFrame.pack(fill='x', padx=20, pady=6)

cosmeticPriceLabel = ttk.Label(billmenuFrame, text='Cosmetic Price')
cosmeticPriceEntry = ttk.Entry(billmenuFrame, validate='key', validatecommand=(validate_cmd,'%P'))
cosmeticPriceLabel.grid(row=0, column=0,padx=10)
cosmeticPriceEntry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

cosmeticTaxLabel = ttk.Label(billmenuFrame, text='Cosmetic Tax')
cosmeticTaxEntry = ttk.Entry(billmenuFrame, validate='key', validatecommand=(validate_cmd,'%P'))
cosmeticTaxLabel.grid(row=0, column=2,padx=10, sticky='w')
cosmeticTaxEntry.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

groceryPriceLabel = ttk.Label(billmenuFrame, text='Grocery Price')
groceryPriceEntry = ttk.Entry(billmenuFrame, validate='key', validatecommand=(validate_cmd,'%P'))
groceryPriceLabel.grid(row=1, column=0,padx=10, sticky='w')
groceryPriceEntry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

groceryTaxLabel = ttk.Label(billmenuFrame, text='Grocery Tax')
groceryTaxEntry = ttk.Entry(billmenuFrame, validate='key', validatecommand=(validate_cmd,'%P'))
groceryTaxLabel.grid(row=1, column=2,padx=10, sticky='w')
groceryTaxEntry.grid(row=1, column=3, padx=10, pady=10, sticky='ew')

coldDrinkPriceLabel = ttk.Label(billmenuFrame, text='Cold Drink Price')
coldDrinkPriceEntry = ttk.Entry(billmenuFrame, validate='key', validatecommand=(validate_cmd,'%P'))
coldDrinkPriceLabel.grid(row=2, column=0,padx=10, sticky='w')
coldDrinkPriceEntry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

coldDrinkTaxLabel = ttk.Label(billmenuFrame, text='Cold Drink Tax')
coldDrinkTaxEntry = ttk.Entry(billmenuFrame, validate='key', validatecommand=(validate_cmd,'%P'))
coldDrinkTaxLabel.grid(row=2, column=2,padx=10, sticky='w')
coldDrinkTaxEntry.grid(row=2, column=3, padx=10, pady=10, sticky='ew')
billButtonFrame = ttk.Frame(billmenuFrame, bootstyle='dark')
billmenuFrame.columnconfigure(4, weight=1)
billButtonFrame.grid(row=0, column=4, rowspan=3, sticky='nesw')

billButtonFrame.columnconfigure((0, 1, 2, 3, 4), weight=1)
billButtonFrame.rowconfigure(0, weight=1)

totalButton = ttk.Button(billButtonFrame, text='Total', bootstyle=DANGER, width=10, command=total)
totalButton.grid(row=0, column=0, padx=20, sticky='ew', ipady=8)

billButton = ttk.Button(billButtonFrame, text='Bill', bootstyle=DANGER, width=10, command=bill_area)
billButton.grid(row=0, column=1, padx=20, sticky='ew', ipady=8)

emailButton = ttk.Button(billButtonFrame, text='Email', bootstyle=DANGER, width=10, command=send_email)
emailButton.grid(row=0, column=2, padx=20, sticky='ew', ipady=8)

printButton = ttk.Button(billButtonFrame, text='Print', bootstyle=DANGER, width=10, command=print_bill)
printButton.grid(row=0, column=3, padx=20, sticky='ew', ipady=8)

clearButton = ttk.Button(billButtonFrame, text='Clear', bootstyle=DANGER, width=10)
clearButton.grid(row=0, column=4, padx=20, sticky='ew', ipady=8)

root.mainloop()