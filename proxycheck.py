import requests
import keyboard
import json
from rich import print, pretty
from rich.console import Console
from time import sleep

pretty.install()
console = Console()

def check_proxy(proxy):
    try:
        r = requests.get('https://httpbin.org/ip', proxies=proxy, timeout=1)
        if r.status_code == 200:
            return True
        else:
            return False
    except:
        return False

def check_anonymity(proxy):
    try:
        r = requests.get('https://httpbin.org/ip', proxies=proxy, timeout=1)
        if r.status_code == 200:
            ip = json.loads(r.text)['origin']
            if ip == proxy['http'].split(':')[0]:
                return True
            else:
                return False
        else:
            return False
    except:
        return False

def validatedProxy(proxy):
    if check_proxy(proxy) and check_anonymity(proxy):
        return True
    else:
        return False

def checkProxies():
    with open('proxies.txt', 'r') as f:
        proxies = f.readlines()
    for proxy in proxies:
        proxy = {'http': proxy, 'https': proxy}
        if validatedProxy(proxy):
            console.print("[bold green]Validated Proxy: " + proxy['http'])
            with open('validatedProxies.txt', 'a') as f:
                f.write(proxy['http'])
        else:
            console.print("[bold red]Invalid Proxy: " + proxy['http'])
        if keyboard.is_pressed('esc'):
            print('Exiting...')
            break