import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def ema(n, day, values):
    licznik = 0
    mianownik = 0
    if n == 12:
        alfa = (2 / (12 + 1))
        for i in range(13):
            if (day - i) < 0:
                licznik += (((1 - alfa) ** i) * values[0])
                mianownik += ((1 - alfa) ** i)
            else:
                licznik += (((1 - alfa) ** i) * values[day - i])
                mianownik += ((1 - alfa) ** i)
        return licznik / mianownik
    elif n == 26:
        alfa = (2 / (26 + 1))
        for i in range(27):
            if (day - i) < 0:
                licznik += (((1 - alfa) ** i) * values[0])
                mianownik += ((1 - alfa) ** i)
            else:
                licznik += (((1 - alfa) ** i) * values[day - i])
                mianownik += ((1 - alfa) ** i)
        return licznik / mianownik


def macd(day, values):
    return (ema(12, day, values) - ema(26, day, values))


def signal(day, macd_list):
    alfa = (2 / (9 + 1))
    licznik = 0
    mianownik = 0
    for i in range(10):
        if (day - i) < 0:
            licznik += (((1 - alfa) ** i) * macd_list[0])
            mianownik += ((1 - alfa) ** i)
        else:
            licznik += (((1 - alfa) ** i) * macd_list[day - i])
            mianownik += ((1 - alfa) ** i)
    return licznik / mianownik


def licz_macd(macd_list, values):
    for i in range(len(values)):
        macd_list.append(macd(i, values))


def licz_signal(signal_list, values, macd_list):
    for i in range(len(values)):
        signal_list.append(signal(i, macd_list))


def wykres(dates, values, macd_list, signal_list):

    plt.figure(figsize=(12,5))
    ax1 = plt.subplot(212)
    plt.plot(dates, macd_list, label='MACD', color='blue')
    plt.plot(dates, signal_list, label='SIGNAL', color='orange')
    plt.legend()
    plt.xlabel('DATES', fontsize=12)
    plt.ylabel('VALUES', fontsize=12)
    ax2 = plt.subplot(211, sharex=ax1)
    plt.plot(dates, values, label='SHARES', color='purple')
    '''plt.xlabel('DATES', fontsize=12)'''
    plt.ylabel('VALUES', fontsize=12)
    plt.xticks(np.arange(0, 1000, step=99))
    plt.title('MACD', fontsize=15)
    plt.legend()
    plt.savefig('wykres.png')
    plt.show()


def dzialanie(konto, values, macd_list, signal_list):
    for i in range(len(values)):
        if i > 1:
            if macd_list[i] > signal_list[i]:
                if macd_list[i-1] < signal_list[i-1]:
                    kup = int(konto["gotowka"]/values[i])
                    konto["ilosc_akcji"] += kup
                    konto["gotowka"] -= kup*values[i]
                elif macd_list[i-1] == signal_list[i-1]:
                    if macd_list[i-2] < signal_list[i-2]:
                        kup = int(konto["gotowka"] / values[i])
                        konto["ilosc_akcji"] += kup
                        konto["gotowka"] -= kup * values[i]
            elif macd_list[i] < signal_list[i]:
                if macd_list[i-1] > signal_list[i-1]:
                    konto["gotowka"] += konto["ilosc_akcji"]*values[i]
                    konto["ilosc_akcji"] = 0
                elif macd_list[i-1] == signal_list[i-1]:
                    if macd_list[i-2] > signal_list[i-2]:
                        konto["gotowka"] += konto["ilosc_akcji"] * values[i]
                        konto["ilosc_akcji"] = 0


def zysk(konto, values):
    z = (konto["ilosc_akcji"]*values[len(values)-1]+konto["gotowka"])/(1000*values[0])
    print("Zysk: "+str(z)+".")


def wypisz(konto, day, values):
    print("Dzien: "+str(day+1)+", wartosc akcji: "+str(values[day])+", ilosc posiadanych akcji: "+str(konto["ilosc_akcji"])+", gotowka: "+str(konto["gotowka"])+".")


def main():
    file = pd.read_csv("wig20_f.csv")
    values = file["Otwarcie"]
    dates = file["Data"]
    macd_list = []
    signal_list = []

    licz_macd(macd_list, values)
    licz_signal(signal_list, values, macd_list)
    wykres(dates, values, macd_list, signal_list)

    konto = {
        "ilosc_akcji": 1000,
        "gotowka": 0
    }

    wypisz(konto, 0, values)
    dzialanie(konto, values, macd_list, signal_list)
    wypisz(konto, len(values)-1, values)
    zysk(konto, values)




main()
