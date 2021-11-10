#Author - PastureBedtime
#Help from - Major
#

version = '1.1.2'

from tkinter import *
import requests
import datetime as dt
from datetime import timedelta
from matplotlib import style
import pandas_datareader.data as web

def major():
    ticker=textentry.get() #collects text
    output.delete(0.0, END)
    
    #ticker price stuff
    style.use('ggplot')
    start = dt.datetime.now() - timedelta(days=1)
    end = dt.datetime.now()
    df = web.DataReader(ticker, 'yahoo', start, end)
    dfl = df['Adj Close']
    dfls = dfl.to_string()
    dflsl = list(dfl)
    #dflsl[1] is the current price
    #trades api stuff
    
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

    cspl5 = csp_strike_ints[0:5]
    csp_total = sum(csp_strike_ints)
    csp_len = len(csp_strike)
    csp_mean = csp_total/csp_len
    
    sppf = [s['price_filled'] for s in short_puts]
    list(sppf)
    sppf_total = sum(sppf)
    sppf_len = len(sppf)
    sppf_mean = sppf_total/sppf_len
    
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

    lpl5 = lp_strike_ints[0:5]
    lp_total = sum(lp_strike_ints)
    lp_len = len(lp_strike)
    lp_mean = lp_total/lp_len
    
    lppf = [s['price_filled'] for s in long_puts]
    list(lppf)
    lppf_total = sum(lppf)
    lppf_len = len(lppf)
    lppf_mean = lppf_total/lppf_len
    
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
    
    ccl5 = cc_strike_ints[0:5]
    cc_total = sum(cc_strike_ints)
    cc_len = len(cc_strike)
    cc_mean = cc_total/cc_len
    
    scpf = [s['price_filled'] for s in short_calls]
    list(scpf)
    scpf_total = sum(scpf)
    scpf_len = len(scpf)
    scpf_mean = scpf_total/scpf_len
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

    lcl5 = lc_strike_ints[0:5]
    lc_total = sum(lc_strike_ints)
    lc_len = len(lc_strike)
    lc_mean = lc_total/lc_len
    
    lcpf = [s['price_filled'] for s in long_calls]
    list(lcpf)
    lcpf_total = sum(lcpf)
    lcpf_len = len(lcpf)
    lcpf_mean = lcpf_total/lcpf_len
    
    #print(f'Long call Concenus: {int(lc_mean)}')

    #
    #
    # Thetagang Price Prediction
    #
    #

    put_side = (csp_mean + lp_mean)/2
    call_side = (cc_mean + lc_mean)/2
    totaltrades = csp_len + cc_len + lp_len + lc_len
    def bias():
        if csp_len + lc_len > cc_len + lp_len:
            return 'Bullish'
        else:
            return 'Bearish'
    def inrange():
        if int(dflsl[1]) < call_side and int(dflsl[1]) > put_side:
            return "In range, safe to trade"
        else: 
            return "Out of range, use caution"
    #def sentiment():
    name=(f'Info found for: {ticker}')
    lastp=(f'\nLast Closing and Current Price: \n{dfls}')
    bullbear=(f'\nSentiment: {bias()}')
    rcheck=(f'\nPrice vs Expected Range: {inrange()}')
    ttr=(f'\n\nTotal Trades Gathered: {totaltrades}')
    spc=(f' \n\nShort Put Concensus:  {int(csp_mean)} | Number of Trades: {int(csp_len)} | AVG Premium: {round(sppf_mean, 2)} | Last 5: {ccl5} ')
    lpc=(f' \nLong Put Concensus:   {int(lp_mean)} | Number of Trades: {int(lp_len)} | AVG Premium: {round(lppf_mean, 2)} | Last 5: {lpl5}')
    scc=(f' \nShort call Concensus: {int(cc_mean)} | Number of Trades: {int(cc_len)} | AVG Premium: {round(scpf_mean, 2)}  | Last 5: {ccl5} ')
    lcc=(f' \nLong call Concensus:  {int(lc_mean)} | Number of Trades: {int(lc_len)} | AVG Premium: {round(lcpf_mean, 2)} | Last 5: {lcl5} ')
    ter=(f' \n\nThetagang Expected Range: {int(put_side)} to {int(call_side)}')
    warn=(f' \n\n\nInformation provided in this tool is not financial advice, and is collected from user input. This input can skew the data unfavorably. Use at own risk.')
    show_me = name + lastp + ttr + bullbear + rcheck + spc + lpc + scc + lcc + ter + warn
    output.insert(END, show_me)
    #sentiment()

#Main 
window = Tk()
window.title(f'Thetagang Sentiment v{version}    (unofficial)')
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
output = Text(window, width=120, height=20, wrap=WORD, background='#32CD32')
output.grid(row=6, column=0, columnspan=2,sticky=W)

#how to use

#Label (window, text='\nHow to use:', bg='black', fg='white', font='none 10 bold').grid(row=20,column=0,sticky=W)
Label (window, text='\nIf current stock price is within range:\nCash Secured Puts, Covered Calls, Put Credit Spreads, and Call Credit Spreads are all ideal', bg='black', fg='white', font='none 8 bold').grid(row=21,column=0,)
Label (window, text='\nIf current stock price is above range(possibly overbought): \nIf Bullish: Care should be taken, Put Credit Spreads or Cash Secured puts are possible.\nIf bearish: Covered Calls or Call Credit Spreads are ideal.', bg='black', fg='white', font='none 8 bold').grid(row=22,column=0,)
Label (window, text='\nIf current stock price is below range(possibly oversold): \nIf Bullish: Cash secured puts and Put Credit Spreads are ideal. \nIf Bearish: Care should be taken, Call Credit Spreads and Covered Calls are ideal.', bg='black', fg='white', font='none 8 bold').grid(row=23,column=0,)
Label (window, text='\nLow trade volume may be a big factor in range skew.', bg='black', fg='white', font='none 8 bold').grid(row=24,column=0)


#nomen = major()
    

#exit function
def close_window():
    window.destroy()
    exit()

#Exit Button
Button(window, text='Click to terminate', width =18, command=close_window).grid(row=27,column=0)




window.mainloop()