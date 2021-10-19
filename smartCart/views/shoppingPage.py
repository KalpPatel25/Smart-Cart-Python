import tkinter as tk
from tkinter import ANCHOR
from tkinter.messagebox import showinfo

import firebase as firebase
import firebase_admin
from firebase_admin import credentials
from numpy.core import double
from pyasn1.compat.octets import null
from pyrebase import pyrebase
from firebase_admin import db
import geocoder

from views.paymentPage import PaymentPage


class ShoppingPage(tk.Tk):


    def connectWithDatabase(self):
        cred = firebase_admin.credentials.Certificate("smart-shopping-cart-1fbac-firebase-adminsdk-wfobd-09a600f28a.json")
        default_app = firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://smart-shopping-cart-1fbac-default-rtdb.firebaseio.com/'
        })
        self.ref = db.reference('items')




    def checkItemInTheInventory(self,itemCode):
        doc = self.ref.child(itemCode).get()
        print(doc)
        if(doc != None):
            return db.reference('items').child(itemCode).get()
        else:
            return None

    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry('500x500')
        self.newItem = ''
        self.connectWithDatabase()
        self.totalPrice : float = 0.0
        print(type(self.totalPrice))
        self.itemsArray=[]
        self.priceArray=[]
        self.itemCodeArray=[]
        self.lblItemsInTheCart = tk.Label(text="Items in the cart").grid(row="0",column="0",columnspan=4)
        self.listItem = tk.Listbox(self)
        self.listItem.grid(row="1",column="0",columnspan="5")
        self.priceList = tk.Listbox(self)
        self.priceList.grid(row="1",column="6",columnspan="3")

        self.lblTotalPrice = tk.Label(self, text='$ '+str(self.totalPrice))
        self.lblTotalPrice.grid(row="2", column="6")
        self.btnClearAll = tk.Button(self, text="Clear All Items",command = lambda : self.clearAllItem()).grid(row="2", column="0", columnspan="3")
        self.btnRemoveItem = tk.Button(self, text="Remove Item", command = lambda : self.removeItem()).grid(row="2", column="4", columnspan="2")

        self.btnHelp = tk.Button(self,text = "Help",command = lambda : self.helpCall()).grid(row="3",column="0",columnspan="2")
        self.btnProductMap = tk.Button(self, text="Product Map", ).grid(row="3", column="3", columnspan="2")
        self.btnFinish = tk.Button(self, text="Finish", command = lambda : self.paymentPage()).grid(row="3", column="6", columnspan="2")

        self.bind('<Key>', self.addNewItemInTheList)


    def addNewItemInTheList(self, event):
        if event.char in '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz':
            self.newItem += event.char

        elif event.keysym == 'Return':
            print(self.newItem)
            if(self.checkItemInTheInventory(self.newItem) != None):
                jsonObj = self.checkItemInTheInventory(self.newItem)
                self.addItem(jsonObj['name'], jsonObj['price'])
            else:
                self.newItem=''
                showinfo('Not Found !', 'This item is not available here')

    def addItem(self, itemName, itemPrice):
        self.listItem.insert(tk.END,itemName)
        self.priceList.insert(tk.END, itemPrice)
        self.totalPrice = self.totalPrice + float(itemPrice)
        self.itemsArray.append(itemName)
        self.priceArray.append(itemPrice)
        self.itemCodeArray.append(self.newItem)
        self.updatePriceLbl()
        #self.lblTotalPrice.config(text=str(self.totalPrice))
        self.newItem = ''

    def paymentPage(self):
        self.destroy()
        print(self.itemsArray)
        print(self.priceArray)
        PaymentPage(self.itemsArray, self.priceArray, self.totalPrice, self.itemCodeArray)

    def updatePriceLbl(self):
        self.lblTotalPrice.config(text="$ " + str(self.totalPrice))



    def removeItem(self):
        selection = self.listItem.curselection()
        selection =str(selection)
        idx = int (selection[1])
        print("Currently removing : "+str(idx))
        self.listItem.delete(idx)
        self.itemsArray.pop(idx)
        self.priceArray.pop(idx)
        self.itemCodeArray.pop(idx)
        itemPrice = self.priceList.get(idx)
        self.totalPrice = self.totalPrice - float(itemPrice)
        self.priceList.delete(idx)
        self.updatePriceLbl()

    def clearAllItem(self):
        self.listItem.delete(0,self.listItem.size()-1)
        self.priceList.delete(0,self.priceList.size()-1)
        self.totalPrice = 0.0
