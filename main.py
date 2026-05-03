import random
import time
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.scrolled import ScrolledFrame, ScrolledText
from ttkbootstrap.widgets import ToastNotification

def total():
    global soapPrice
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
    toast(title='Success',message='Successfully added!')

randnumber = random.randint(10, 99)
curtime = time.strftime("%y%m%d%H%M%S")
billnumber = f'{randnumber}{curtime}'

def safe_num(val, target_type="int", default=None):
    try:
        if target_type == 'int':
            return int(float(val))
        elif target_type == 'float':
            return float(val)
    except:
        return default
    
def bill_area():
    # if safe_num(nameEntry.get()) or safe_num(phoneEntry.get()):
    #     toast(title='Error',message='Customer details are required!', style=DANGER, alert=True)
    # elif safe_num(cosmeticPriceEntry.get()) and safe_num(groceryPriceEntry.get()) and safe_num(coldDrinkPriceEntry.get()):
    #     toast(title='Error',message='No products selected!', style=DANGER, alert=True)
    # else:
        billTextArea.delete('1.0',END)
        billTextArea.insert(END, '\t\t**Welcome Customer**\n\n')
        billTextArea.insert(END, f'Bill Number: {billnumber}\n')
        billTextArea.insert(END, f'Customer Name: {nameEntry.get()}\n')
        billTextArea.insert(END, f'Customer Phone No.: {phoneEntry.get()}\n')
        billTextArea.insert(END, '='*36 +'\n')
        billTextArea.insert(END, f'Product\t\tQuantity\t\tPrice\n')
        billTextArea.insert(END, '='*36 +'\n')
        if(safe_num(bathsoapEntry.get())):
             billTextArea.insert(END, f'Bath Soap\t\t{soapPrice}')
             
        


def toast(title, message, style=SUCCESS, alert=False):
    toast = ToastNotification(
        title=title,
        message=message,
        position=(10, 60, "ne"),
        duration=3000,
        alert=alert,
        iconfont=("", 12),
        bootstyle=style
    )
    toast.show_toast()

root = ttk.Window(themename='solar')
root.state('zoomed')
root.resizable(False, False)

root.title('Retail Billing Software')

main_scrolled_frame = ScrolledFrame(root, autohide=True)
main_scrolled_frame.pack(fill=BOTH, expand=YES)

root.iconbitmap('assets/icon.ico')
style = ttk.Style()
style.configure('.', font=("Helvetica", 11))
img = ttk.PhotoImage(file='assets/img1.png')
ttk.Label(main_scrolled_frame, text='Retail Billing Software'.upper(), image=img, bootstyle='dark-inverse', \
           anchor='center', padding=20, font=("",14), compound='left').pack(fill='x')

customer_details_frame = ttk.Labelframe(main_scrolled_frame, text='Customer Details', padding=20)
customer_details_frame.pack(fill='x', padx=20, pady=10)

nameLabel = ttk.Label(customer_details_frame, text='Name')
nameEntry = ttk.Entry(customer_details_frame)
nameLabel.grid(row=0, column=0,padx=10)
customer_details_frame.columnconfigure(1, weight=1)
nameEntry.grid(row=0, column=1, padx=10, sticky='ew')

phoneLabel = ttk.Label(customer_details_frame, text='Phone')
phoneEntry = ttk.Entry(customer_details_frame)
phoneLabel.grid(row=0, column=2, padx=10)
customer_details_frame.columnconfigure(3, weight=1)
phoneEntry.grid(row=0, column=3, padx=10, sticky='ew')

billnumberLabel = ttk.Label(customer_details_frame, text='Bill Number')
billnumberEntry = ttk.Entry(customer_details_frame)
billnumberLabel.grid(row=0, column=4, padx=10)
customer_details_frame.columnconfigure(5, weight=1)
billnumberEntry.grid(row=0, column=5, padx=10, sticky='ew')

searchBtn = ttk.Button(customer_details_frame, text='Save', bootstyle=PRIMARY)
searchBtn.grid(row=0, column=6, padx=10)

productsFrame = ttk.Frame(main_scrolled_frame, padding=20)
productsFrame.pack(fill='x')
productsFrame.columnconfigure(0,weight=1, uniform='productframe')
productsFrame.columnconfigure(1,weight=1, uniform='productframe')
productsFrame.columnconfigure(2,weight=1, uniform='productframe')
productsFrame.columnconfigure(3,weight=1, uniform='productframe')

cosmeticsFrame = ttk.Labelframe(productsFrame, text='Cosmetics', padding=20)
cosmeticsFrame.grid(row=0, column=0, sticky='senw')
cosmeticsFrame.columnconfigure(1, weight=1)

bathsoapLabel = ttk.Label(cosmeticsFrame, text='Bath Soap')
bathsoapEntry = ttk.Entry(cosmeticsFrame)
bathsoapLabel.grid(row=0, column=0, padx=20, sticky='w')
bathsoapEntry.grid(row=0, column=1, sticky='ew', pady=10)
bathsoapEntry.insert(0,0)

facecreamLabel = ttk.Label(cosmeticsFrame, text='Face Cream')
facecreamEntry = ttk.Entry(cosmeticsFrame)
facecreamLabel.grid(row=1, column=0, padx=20, sticky='w')
facecreamEntry.grid(row=1, column=1, sticky='ew',pady=10)
facecreamEntry.insert(0,0)

facewashLabel = ttk.Label(cosmeticsFrame, text='Face Wash')
facewashEntry = ttk.Entry(cosmeticsFrame)
facewashLabel.grid(row=2, column=0, padx=20, sticky='w')
facewashEntry.grid(row=2, column=1, sticky='ew',pady=10)
facewashEntry.insert(0,0)

hairsprayLabel = ttk.Label(cosmeticsFrame, text='Hair Spray')
hairsprayEntry = ttk.Entry(cosmeticsFrame)
hairsprayLabel.grid(row=3, column=0, padx=20, sticky='w')
hairsprayEntry.grid(row=3, column=1, sticky='ew',pady=10)
hairsprayEntry.insert(0,0)

hairgelLabel = ttk.Label(cosmeticsFrame, text='Hair Gel')
hairgelEntry = ttk.Entry(cosmeticsFrame)
hairgelLabel.grid(row=4, column=0, padx=20, sticky='w')
hairgelEntry.grid(row=4, column=1, sticky='ew',pady=10)
hairgelEntry.insert(0,0)

bodylotionLabel = ttk.Label(cosmeticsFrame, text='Body Lotion')
bodylotionEntry = ttk.Entry(cosmeticsFrame)
bodylotionLabel.grid(row=5, column=0, padx=20, sticky='w')
bodylotionEntry.grid(row=5, column=1, sticky='ew',pady=10)
bodylotionEntry.insert(0,0)


groceryFrame = ttk.Labelframe(productsFrame, text='grocery', padding=20)
groceryFrame.grid(row=0, column=1, sticky='esnw', padx=10)
groceryFrame.columnconfigure(1, weight=1)

riceLabel = ttk.Label(groceryFrame, text='Rice')
riceEntry = ttk.Entry(groceryFrame)
riceLabel.grid(row=0, column=0, padx=20, sticky='w')
riceEntry.grid(row=0, column=1, sticky='ew',pady=10)
riceEntry.insert(0,0)

oilLabel = ttk.Label(groceryFrame, text='Oil')
oilEntry = ttk.Entry(groceryFrame)
oilLabel.grid(row=1, column=0, padx=20, sticky='w')
oilEntry.grid(row=1, column=1, sticky='ew',pady=10)
oilEntry.insert(0,0)

daalLabel = ttk.Label(groceryFrame, text='Daal')
daalEntry = ttk.Entry(groceryFrame)
daalLabel.grid(row=2, column=0, padx=20, sticky='w')
daalEntry.grid(row=2, column=1, sticky='ew',pady=10)
daalEntry.insert(0,0)

wheatLabel = ttk.Label(groceryFrame, text='Wheat')
wheatEntry = ttk.Entry(groceryFrame)
wheatLabel.grid(row=3, column=0, padx=20, sticky='w')
wheatEntry.grid(row=3, column=1, sticky='ew',pady=10)
wheatEntry.insert(0,0)

sugerLabel = ttk.Label(groceryFrame, text='Suger')
sugerEntry = ttk.Entry(groceryFrame)
sugerLabel.grid(row=4, column=0, padx=20, sticky='w')
sugerEntry.grid(row=4, column=1, sticky='ew',pady=10)
sugerEntry.insert(0,0)

teaLabel = ttk.Label(groceryFrame, text='Tea')
teaEntry = ttk.Entry(groceryFrame)
teaLabel.grid(row=5, column=0, padx=20, sticky='w')
teaEntry.grid(row=5, column=1, sticky='ew',pady=10)
teaEntry.insert(0,0)

drinksFrame = ttk.Labelframe(productsFrame, text='Cold Drinks', padding=20)
drinksFrame.grid(row=0, column=2, sticky='esnw', padx=10)
drinksFrame.columnconfigure(1, weight=1)

maazaLabel = ttk.Label(drinksFrame, text='Maaza')
maazaEntry = ttk.Entry(drinksFrame)
maazaLabel.grid(row=0, column=0, padx=20, sticky='w')
maazaEntry.grid(row=0, column=1, sticky='ew',pady=10)
maazaEntry.insert(0,0)

pepsiLabel = ttk.Label(drinksFrame, text='Pepsi')
pepsiEntry = ttk.Entry(drinksFrame)
pepsiLabel.grid(row=1, column=0, padx=20, sticky='w')
pepsiEntry.grid(row=1, column=1, sticky='ew',pady=10)
pepsiEntry.insert(0,0)

spriteLabel = ttk.Label(drinksFrame, text='Sprite')
spriteEntry = ttk.Entry(drinksFrame)
spriteLabel.grid(row=2, column=0, padx=20, sticky='w')
spriteEntry.grid(row=2, column=1, sticky='ew',pady=10)
spriteEntry.insert(0,0)

dewLabel = ttk.Label(drinksFrame, text='Dew')
dewEntry = ttk.Entry(drinksFrame)
dewLabel.grid(row=3, column=0, padx=20, sticky='w')
dewEntry.grid(row=3, column=1, sticky='ew',pady=10)
dewEntry.insert(0,0)

frootiLabel = ttk.Label(drinksFrame, text='Frooti')
frootiEntry = ttk.Entry(drinksFrame)
frootiLabel.grid(row=4, column=0, padx=20, sticky='w')
frootiEntry.grid(row=4, column=1, sticky='ew',pady=10)
frootiEntry.insert(0,0)

cocacolaLabel = ttk.Label(drinksFrame, text='Coca Cola')
cocacolaEntry = ttk.Entry(drinksFrame)
cocacolaLabel.grid(row=5, column=0, padx=20, sticky='w')
cocacolaEntry.grid(row=5, column=1, sticky='ew',pady=10)
cocacolaEntry.insert(0,0)

billFrame = ttk.Frame(productsFrame)
billFrame.grid(row=0, column=3, sticky='nsew')
billFrame.columnconfigure(0, weight=1)

billLabel =  ttk.Label(billFrame, text='Bill Area', bootstyle='light-inverse', anchor='center', padding=10)
billLabel.pack(fill='x')

billTextArea = ScrolledText(billFrame, height=15, autohide=True)
billTextArea.pack()

# scrollbar = ttk.Scrollbar(billFrame, bootstyle="round", orient=VERTICAL)
# scrollbar.grid(row=1,column=1, sticky='ns')
# scrollbar.config(command=textarea.yview)
# textarea.config(yscrollcommand=scrollbar.set)

billmenuFrame = ttk.Labelframe(main_scrolled_frame, text='Bill Menu', padding=20)
billmenuFrame.pack(fill='x', padx=20, pady=10)

cosmeticPriceLabel = ttk.Label(billmenuFrame, text='Cosmetic Price')
cosmeticPriceEntry = ttk.Entry(billmenuFrame)
cosmeticPriceLabel.grid(row=0, column=0,padx=10)
cosmeticPriceEntry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

cosmeticTaxLabel = ttk.Label(billmenuFrame, text='Cosmetic Tax')
cosmeticTaxEntry = ttk.Entry(billmenuFrame)
cosmeticTaxLabel.grid(row=0, column=2,padx=10, sticky='w')
cosmeticTaxEntry.grid(row=0, column=3, padx=10, pady=10, sticky='ew')

groceryPriceLabel = ttk.Label(billmenuFrame, text='Grocery Price')
groceryPriceEntry = ttk.Entry(billmenuFrame)
groceryPriceLabel.grid(row=1, column=0,padx=10, sticky='w')
groceryPriceEntry.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

groceryTaxLabel = ttk.Label(billmenuFrame, text='Grocery Tax')
groceryTaxEntry = ttk.Entry(billmenuFrame)
groceryTaxLabel.grid(row=1, column=2,padx=10, sticky='w')
groceryTaxEntry.grid(row=1, column=3, padx=10, pady=10, sticky='ew')

coldDrinkPriceLabel = ttk.Label(billmenuFrame, text='Cold Drink Price')
coldDrinkPriceEntry = ttk.Entry(billmenuFrame)
coldDrinkPriceLabel.grid(row=2, column=0,padx=10, sticky='w')
coldDrinkPriceEntry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

coldDrinkTaxLabel = ttk.Label(billmenuFrame, text='Cold Drink Tax')
coldDrinkTaxEntry = ttk.Entry(billmenuFrame)
coldDrinkTaxLabel.grid(row=2, column=2,padx=10, sticky='w')
coldDrinkTaxEntry.grid(row=2, column=3, padx=10, pady=10, sticky='ew')
billButtonFrame = ttk.Frame(billmenuFrame, bootstyle='dark')
billmenuFrame.columnconfigure(4, weight=1)
billButtonFrame.grid(row=0, column=4, rowspan=3, sticky='nesw')

billButtonFrame.columnconfigure((0, 1, 2, 3, 4), weight=1)
billButtonFrame.rowconfigure(0, weight=1)

totalButton = ttk.Button(billButtonFrame, text='Total', bootstyle=DANGER, padding=(40, 20), command=total)
totalButton.grid(row=0, column=0, padx=20, sticky='ew')

billButton = ttk.Button(billButtonFrame, text='Bill', bootstyle=DANGER, padding=(40, 20), command=bill_area)
billButton.grid(row=0, column=1, padx=20, sticky='ew')

emailButton = ttk.Button(billButtonFrame, text='Email', bootstyle=DANGER, padding=(40, 20))
emailButton.grid(row=0, column=2, padx=20, sticky='ew')

printButton = ttk.Button(billButtonFrame, text='Print', bootstyle=DANGER, padding=(40, 20))
printButton.grid(row=0, column=3, padx=20, sticky='ew')

clearButton = ttk.Button(billButtonFrame, text='Clear', bootstyle=DANGER, padding=(40, 20))
clearButton.grid(row=0, column=4, padx=20, sticky='ew')

root.mainloop()