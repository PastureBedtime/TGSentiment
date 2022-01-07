#Author - PastureBedtime
#Huge thanks to Major for getting me started with the json file
#Another huge thanks to Joonie for letting me scrape his website!


version = '1.1.4'

from tkinter import *
import math
import requests
import datetime as dt
from datetime import timedelta
from matplotlib import style
import pandas_datareader.data as web

def major():
    ticker=textentry.get() #collects text
    ivpre=textentry2.get()
    iv=int(ivpre)/100
    
    #
    #
    dte=30 #This is going to be editable later
    #
    #
    
    
    output.delete(0.0, END)
    
    #live data ticker price stuff via Yahoo
    style.use('ggplot')
    start = dt.datetime.now() - timedelta(days=1)
    end = dt.datetime.now()
    df = web.DataReader(ticker, 'yahoo', start, end)
    dfl = df['Adj Close']
    dfls = dfl.to_string()
    dflsl = list(dfl)
    #dflsl[1] is the current live price, but I've had issues with that throwing errors.
    
    #TG trades api stuff
    
    url = 'https://api.thetagang.com/trades'
    payload = {'ticker': ticker}

    resp = requests.get(url, params=payload)
    trades = resp.json()['data']['trades']
    
    short_puts = [x for x in trades if x['short_put'] != None]
    long_puts = [x for x in trades if x['long_put'] != None]
    short_calls = [x for x in trades if x['short_call'] != None]
    long_calls = [x for x in trades if x['long_call'] != None]
    
    #Below prings the trades json for the ticker selected. 
    #Use for debugging
    #print(
    #    json.dumps(short_puts, indent=2)
    #)

    #
    #
    # SHORT PUTS
    #
    #
    
    csp_strike = [s['short_put'] for s in short_puts]
    list(csp_strike)
    csp_strike_ints = [float(i) for i in csp_strike]
    cspl5 = csp_strike_ints[0:5]
    csp_total = sum(csp_strike_ints)
    csp_len = len(csp_strike)
    csp_mean = csp_total/csp_len
    
    sppf = [s['price_filled'] for s in short_puts]
    list(sppf)
    sppf_total = sum(sppf)
    sppf_len = len(sppf)
    sppf_mean = sppf_total/sppf_len
    

    #
    #
    # LONG PUTS
    #
    #

    lp_strike = [s['long_put'] for s in long_puts]
    list(lp_strike)
    lp_strike_ints = [float(i) for i in lp_strike]
    lpl5 = lp_strike_ints[0:5]
    lp_total = sum(lp_strike_ints)
    lp_len = len(lp_strike)
    lp_mean = lp_total/lp_len
    
    lppf = [s['price_filled'] for s in long_puts]
    list(lppf)
    lppf_total = sum(lppf)
    lppf_len = len(lppf)
    lppf_mean = lppf_total/lppf_len
    

    #
    #
    # Short Calls
    #
    #
    
    cc_strike = [s['short_call'] for s in short_calls]
    list(cc_strike)
    cc_strike_ints = [float(i) for i in cc_strike]
    
    ccl5 = cc_strike_ints[0:5]
    cc_total = sum(cc_strike_ints)
    cc_len = len(cc_strike)
    cc_mean = cc_total/cc_len
    
    scpf = [s['price_filled'] for s in short_calls]
    list(scpf)
    scpf_total = sum(scpf)
    scpf_len = len(scpf)
    scpf_mean = scpf_total/scpf_len
   
    
    #
    #
    #Long Calls
    #
    #

    lc_strike = [s['long_call'] for s in long_calls]
    list(lc_strike)
    lc_strike_ints = [float(i) for i in lc_strike]
    lcl5 = lc_strike_ints[0:5]
    lc_total = sum(lc_strike_ints)
    lc_len = len(lc_strike)
    lc_mean = lc_total/lc_len
    
    lcpf = [s['price_filled'] for s in long_calls]
    list(lcpf)
    lcpf_total = sum(lcpf)
    lcpf_len = len(lcpf)
    lcpf_mean = lcpf_total/lcpf_len
    

    #
    #
    # Thetagang Price Prediction
    # This section is under construction
    #
    #

    put_side = (csp_mean + lp_mean)/2
    call_side = (cc_mean + lc_mean)/2
    
    #
    # Overall Bias Feature 
    # inrange function.... redundent??
    #
    
    totaltrades = csp_len + cc_len + lp_len + lc_len
    def bias():
        if csp_len + lc_len > cc_len + lp_len:
            return 'Bullish'
        else:
            return 'Bearish'
    def inrange():
        if int(dflsl[0]) < call_side and int(dflsl[0]) > put_side:
            return "In range, safe to trade"
        else: 
            return "Out of range, use caution"
    #
    #Reccomended Trades Feature
    #
   
    #def traderec():
        #unsure of what to do here yet
    
    #
    #
    #Standard Diviation Calculations
    #
    #
    
    def StandardDeviations():
        #Strikes below Standard Deviation 
        OneStdDevUp = int(dflsl[0]) + (int(dflsl[0])*iv*math.sqrt(dte/365))
        TwoStdDevUp = int(dflsl[0]) + (int(dflsl[0])*(iv*2)*math.sqrt(dte/365))
        OneStdDevDown = int(dflsl[0]) - (int(dflsl[0])*iv*math.sqrt(dte/365))
        TwoStdDevDown = int(dflsl[0]) - (int(dflsl[0])*(iv*2)*math.sqrt(dte/365))
        devrange1 = (f'1 Standard Deviation {round(OneStdDevDown,2)} to {round(OneStdDevUp,2)}')
        devrange2 = (f'\n2 Standard Deviations {round(TwoStdDevDown,2)} to {round(TwoStdDevUp,2)}')
        return devrange1 + devrange2
    
    #
    # Output code
    #
    
    name=(f'Info found for: {ticker}')
    lastp=(f'\nLast Price: \n{dfls}')
    bullbear=(f'\nOverall Sentiment: {bias()}')
    rcheck=(f'\nPrice vs Expected Range: {inrange()}')
    ttr=(f'\n\nTotal Trades Gathered: {totaltrades}')
    spc=(f' \n\nShort Put Consensus:  {int(csp_mean)} | Number of Trades: {int(csp_len)} | AVG Prem: {round(sppf_mean, 2)}')
    lpc=(f' \nLong Put Consensus:   {int(lp_mean)} | Number of Trades: {int(lp_len)} | AVG Cost: {round(lppf_mean, 2)} ')
    scc=(f' \nShort call Consensus: {int(cc_mean)} | Number of Trades: {int(cc_len)} | AVG Prem: {round(scpf_mean, 2)} ')
    lcc=(f' \nLong call Consensus:  {int(lc_mean)} | Number of Trades: {int(lc_len)} | AVG Cost: {round(lcpf_mean, 2)} ')
    calcr=(f'\n{StandardDeviations()}')
    ter=(f' \n\nThetagang Expected Range: {int(put_side)} to {int(call_side)}')
    warn=(f' \n\n\nInformation provided in this tool is not financial advice, and is partially collected from user input. This input can skew the data unfavorably. Use at own risk.')
    show_me = name + lastp + ttr + bullbear + ter + calcr + spc + lpc + scc + lcc + warn
    output.insert(END, show_me)
    

#Main 
window = Tk()
window.title(f'Thetagang Sentiment v{version}    (unofficial)')
window.configure(background="black")

#Enter Image below
#label (window, image=xxxxx, bg='black').grid(row=o, column=0, stick=W)

#Create Label 
Label (window, text='Enter Stock Ticker:', bg='black', fg='white', font='none 12 bold').grid(row=1, column=0, sticky=W)
Label (window, text='Enter IV(No % sign):', bg='black', fg='white', font='none 12 bold').grid(row=3, column=0, sticky=W)
#Create Text entry box for ticker
textentry = Entry(window, width=20, bg='#32CD32')
textentry.grid(row=2,column=0, sticky=W)

#Label for IV

#Create 2nd Text box for IV
textentry2 = Entry(window, width=20, bg='#32CD32')
textentry2.grid(row=4,column=0, sticky=W)

#Decode button
Button(window, text='Gather Data', width=11, command=major).grid(row=5, column=0, sticky=W)

#label number2
Label (window, text='\nOutput:', bg='black', fg='white', font='none 12 bold').grid(row=6,column=0,sticky=W)

#output textbox
output = Text(window, width=120, height=25, wrap=WORD, background='#32CD32')
output.grid(row=6, column=0, columnspan=2,sticky=W)

#how to use

#Label (window, text='\nHow to use:', bg='black', fg='white', font='none 10 bold').grid(row=20,column=0,sticky=W)


#nomen = major()
    

#exit function
def close_window():
    window.destroy()
    exit()

#Exit Button
Button(window, text='Click to terminate', width =18, command=close_window).grid(row=27,column=0)




window.mainloop()