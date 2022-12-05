import urllib.request , socket
from rich import print, pretty
from rich.table import Table
from rich.console import Console
from time import sleep
import requests
import json

pretty.install()
console = Console()

socket.setdefaulttimeout(180)

def is_bad_proxy(pip):
    try:        
        proxy_handler = urllib.request.ProxyHandler({'http': pip})        
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)        
        sock=urllib.request.urlopen('http://www.google.com')  # change the url address here
    except urllib.error.HTTPError as e:        
        print('Error code: ', e.code)
        return e.code
    except Exception as detail:

        print( "ERROR:", detail)
        return 1
    return 0

def get_ipandport(URL):
    response = requests.get(URL)
    proxies = json.loads(response.text)
    ip = []
    port = []
    country = []
    proxyList = []
    for proxy in proxies['data']:
        ip.append(proxy['ip'])
        port.append(proxy['port'])
        country.append(proxy['country'])
        proxyList.append(proxy['ip'] + ':' + str(proxy['port']))
    for i in range(len(ip)):
        print('Getting proxy: ' + ip[i] + ':' + str(port[i]))
        with open('proxies.txt', 'a') as f:
            f.write(ip[i] + ':' + port[i] + " # " + country[i] + '\n')
        with console.status("\n[bold green]Getting Proxies...") as status:
            sleep(0.05)
    console.print("\n[bold green]Done! Check the file 'proxies.txt'")
    print(' ')
    for i in range(len(proxyList)):
        if is_bad_proxy(proxyList[i]):
            print("Bad Proxy", proxyList[i])
        else:
            print("Good Proxy", proxyList[i])
            # save good proxy to file
            with open('good_proxies.txt', 'a') as f:
                f.write(proxyList[i] + " # " + country[i] + '\n')
    return ip, port
    
def PROTOCOL_HTTP():
    PROXY_HTTP = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=http'
    get_ipandport(PROXY_HTTP)

def PROTOCOL_HTTPS():
    PROXY_HTTPS = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=https'
    get_ipandport(PROXY_HTTPS)

def PROTOCOL_SOCKS4():
    PROXY_SOCKS4 = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks4'
    get_ipandport(PROXY_SOCKS4)

def PROTOCOL_SOCKS5():
    PROXY_SOCKS5 = 'https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc&protocols=socks5'
    get_ipandport(PROXY_SOCKS5)

def main():
    print('PROXY GENERATOR BY @LESTER.')
    print(' ')
    print('CHOOSE A PROTOCOL')
    print('1 - HTTP')
    print('2 - HTTPS')
    print('3 - SOCKS4')
    print('4 - SOCKS5')
    print('5 - ALL')
    print(' ')

    choice = input('Enter your choice: ')

    if choice == '1':
        PROTOCOL_HTTP()
    elif choice == '2':
        PROTOCOL_HTTPS()
    elif choice == '3':
        PROTOCOL_SOCKS4()
    elif choice == '4':
        PROTOCOL_SOCKS5()
    elif choice == '5':
        PROTOCOL_HTTP()
        PROTOCOL_HTTPS()
        PROTOCOL_SOCKS4()
        PROTOCOL_SOCKS5()
    else:
        print('Invalid Choice')


if __name__ == '__main__':
    main()