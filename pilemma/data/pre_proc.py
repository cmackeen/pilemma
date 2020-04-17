import numpy as np
import pandas as pd

df=pd.read_csv("ETHUSDT.csv")
df['Open time']=pd.to_datetime(df['Open time'], unit='ms')
df['Time'] = df['Open time'].dt.time
df['Date'] = df['Open time'].dt.floor('D')
#df=df[['Open time', 'Close time', 'Open','High','Low','Close','Volume']]
colsnew=['Date', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']

df=df[colsnew]

df.to_csv('ETHUSDT_simp.csv')


