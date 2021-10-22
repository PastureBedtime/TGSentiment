#Begining of Wideband Systems Inc Reference suite
#Author: Alexander Bosman
#Start Date Oct 15, 2021
#
#Maybe add in a few buttons? 
#Like "what do you want to know: How much it costs, how long it takes,
#weight/size/ etc etc etc
#
#an open orders application with add/remove/complete and all info!!!
#
#
version = '1.0.1'

from tkinter import *
import requests

#from InterfaceDictionary import *
#from info_pool import *

#This gets/retrieves the text entered in box
#def decode():
  #  ticker=textentry.get() #collects text
 #   output.delete(0.0, END)


def major():
    ticker=textentry.get() #collects text
    output.delete(0.0, END)
    
    
    url = 'https://api.thetagang.com/trades'
    payload = {'ticker': ticker}

    resp = requests.get(url, params=payload)
    trades = resp.json()['data']['trades']
    
    short_puts = [x for x in trades if x['short_put'] != None]
    long_puts = [x for x in trades if x['long_put'] != None]
    short_calls = [x for x in trades if x['short_call'] != None]
    long_calls = [x for x in trades if x['long_call'] != None]

    #print(
    #    json.dumps(short_puts, indent=2)
    #)

    csp_strike = [s['short_put'] for s in short_puts]
#print(csp_strike)
    list(csp_strike)

    csp_strike_ints = [float(i) for i in csp_strike]
#print(csp_strike_ints)

    csp_total = sum(csp_strike_ints)
    csp_mean = csp_total/len(csp_strike)
#print(f'Short Put Concensus: {int(csp_mean)}')

#
#
# LONG PUTS
#
#

    lp_strike = [s['long_put'] for s in long_puts]
#print(lp_strike)
    list(lp_strike)

    lp_strike_ints = [float(i) for i in lp_strike]
#print(lp_strike_ints)

    lp_total = sum(lp_strike_ints)
    lp_mean = lp_total/len(lp_strike)
#print(f'Long Put Concenus: {int(lp_mean)}')

#
#
# Short Calls
#
#
    cc_strike = [s['short_call'] for s in short_calls]
#print(cc_strike)
    list(cc_strike)

    cc_strike_ints = [float(i) for i in cc_strike]
#print(cc_strike_ints)

    cc_total = sum(cc_strike_ints)
    cc_mean = cc_total/len(cc_strike)
#print(f'Short call Concenus: {int(cc_mean)}')

#
#
#Long Calls
#
#

    lc_strike = [s['long_call'] for s in long_calls]
#print(lp_strike)
    list(lc_strike)

    lc_strike_ints = [float(i) for i in lc_strike]
#print(lp_strike_ints)

    lc_total = sum(lc_strike_ints)
    lc_mean = lc_total/len(lc_strike)
#print(f'Long call Concenus: {int(lc_mean)}')

#
#
# Thetagang Price Prediction
#
#

    put_side = (csp_mean + lp_mean)/2
    call_side = (cc_mean + lc_mean)/2

   
    #def sentiment():
    name=(f'Info found for: {ticker}')
    spc=(f' \nShort Put Concensus: {int(csp_mean)}')
    lpc=(f' \nLong Put Concensus: {int(lp_mean)}')
    scc=(f' \nShort call Concensus: {int(cc_mean)}')
    lcc=(f' \nLong call Concensus: {int(lc_mean)}')
    ter=(f' \nThetagang Expected Range: {int(put_side)} to {int(call_side)}')
    warn=(f' \n\n\nInformation provided in this tool is not financial advice, and is collected from user input. This input can skew the data unfavorably. Use at own risk.')
    show_me = name + spc + lpc + scc + lcc + ter + warn
    output.insert(END, show_me)
    #sentiment()

#def purchase():
 #   entered_text=textentry.get()
 #   output.delete(0,0, END)
 #   try:
  #      definition = priceis
  #  except:
  #      definition = 'Price unavailable'
  #  output.insert(END, definition)

#Main 
window = Tk()
window.title(f'Thetagang Sentiment v {version}(UNOFFICIAL)')
window.configure(background="black")

#Enter Image below
#label (window, image=xxxxx, bg='black').grid(row=o, column=0, stick=W)

#Create Label 
Label (window, text='Enter Stock Ticker:', bg='black', fg='white', font='none 12 bold').grid(row=1, column=0, stick=W)

#Create Text entry box
textentry = Entry(window, width=20, bg='#32CD32')
textentry.grid(row=2,column=0, stick=W)

#Decode button
Button(window, text='Gather Data', width=11, command=major).grid(row=3, column=0, sticky=W)

#label number2
Label (window, text='\nOutput:', bg='black', fg='white', font='none 12 bold').grid(row=5,column=0,sticky=W)

#output textbox
output = Text(window, width=75, height=10, wrap=WORD, background='#32CD32')
output.grid(row=6, column=0, columnspan=2,sticky=W)

#how to use

Label (window, text='\nHow to use:', bg='black', fg='white', font='none 12 bold').grid(row=20,column=0,sticky=W)
Label (window, text='\nIf current stock price is above range, the stock may be overbought.', bg='black', fg='white', font='none 8 bold').grid(row=21,column=0,sticky=W)
Label (window, text='\nIf current stock price is below range, the stock may be oversold.', bg='black', fg='white', font='none 8 bold').grid(row=22,column=0,sticky=W)
Label (window, text='\nLow trade volume may be a big factor in range skew.', bg='black', fg='white', font='none 8 bold').grid(row=23,column=0,sticky=W)

#the dictionary
nomen = major()
    

#exit function
def close_window():
    window.destroy()
    exit()

#Exit Button
Button(window, text='Click to terminate', width =18, command=close_window).grid(row=7,column=0,sticky=W)

#exit function
def close_window():
    window.destroy()
    exit()




window.mainloop()