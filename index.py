import json, requests, sys
import socket, urllib3, time
import os, random, threading
from time import time as tom
cnt=(0)
ping=(0)
key=('Test-Key')
count=(0)
threads=(0)
working=(0)
loop=(True)
not_working=(0)
headers=({'Content-Type': 'application/json', 'Authorization': '{0}'.format(key)})
try:
    if sys.argv[1]:
        maxThreads=(int(sys.argv[1]))
    else:
        maxThreads=(10)
except Exception:
    maxThreads=(10)
try:
    if sys.argv[2]:
        perThread=(int(sys.argv[2]))
    else:
        perThread=(1)
except Exception:
    perThread=(1)
def getProxy(proxType):
    api_url=('{0}{1}'.format("https://proxy.soteria.cf/", proxType))
    response=(requests.get(api_url, headers=headers))
    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        return None
def cleanFile(a):
    lines=([])
    file=(open(str(a)+".dat", "r"))
    for line in file:
        if (line in lines):
            pass
        else:
            lines.append(line)
    for proxy in lines:
        filed=(open(str(a)+".dat", "w"))
        filed.write(str(proxy))
        filed.close()
    file.close()
def check(proxy, proxType, url):
    global ping, working, not_working
    try:
        bef=(tom())
        requests.get(url,proxies={''+proxType:proxType+'://'+proxy},timeout=(5,10))
        aft=(tom())
        ping=(str(aft-bef))
        working+=(1)
        with open(str(proxType)+".dat", "a+") as f:
            f.write(proxy)
            f.write("\n")
        return "Working!"
    except Exception as e:
        not_working+=(1)
        aft=(tom())
        ping=(str(aft-bef))
        if ('ConnectionPool' in str(e) or 'BadStatusLine' in str(e)):
            pass
        else:
            with open("errors.dat", "a+") as f:
                f.write(str(e))
                f.write("\n")
            pass
        return "Not Working!"
def run(n):
    global cnt, count, perThread, ping
    try:
        p=(0)
        while (p < perThread):
            magic=(random.randint(1,4))
            if (magic==1):
                try:
                    count+=(1)
                    http = getProxy('http')
                    print(" [Thread-"+str(n)+"]    HTTP   = "+http[0]+":"+http[1]+" | "+str(check(http[0]+":"+http[1],'http',"http://www.google.com/"))+" | "+str(ping)+" ")
                except Exception:
                    print(" [Thread-"+str(n)+"]    HTTP   = Malformed Proxy Error   ")
            if (magic==2):
                try:
                    count+=(1)
                    https=(getProxy('https'))
                    print(" [Thread-"+str(n)+"]    HTTPS  = "+https[0]+":"+https[1]+" | "+str(check(https[0]+":"+https[1],'https',"https://www.google.com/"))+" | "+str(ping)+" ")
                except Exception:
                    print(" [Thread-"+str(n)+"]    HTTPS  = Malformed Proxy Error   ")
            if (magic==3):
                try:
                    count+=(1)
                    socks4=(getProxy('socks4'))
                    print(" [Thread-"+str(n)+"]    Socks4 = "+socks4[0]+":"+socks4[1]+" | "+str(check(socks4[0]+":"+socks4[1],'socks4',"https://www.google.com/"))+" | "+str(ping)+" ")
                except Exception:
                    print(" [Thread-"+str(n)+"]    Socks4 = Malformed Proxy Error   ")
            if (magic==4):
                try:
                    count+=(1)
                    socks5=(getProxy('socks5'))
                    print(" [Thread-"+str(n)+"]    Socks5 = "+socks5[0]+":"+socks5[1]+" | "+str(check(socks5[0]+":"+socks5[1],'socks5',"https://www.google.com/"))+" | "+str(ping)+" ")
                except Exception:
                    print(" [Thread-"+str(n)+"]    Socks5 = Malformed Proxy Error   ")
            p+=(1)
        else:
            cnt+=(1)
            return
    except KeyboardInterrupt:
        return
def finish():
    global cnt, working, loop, not_working, befTime, count
    try:
        while (loop):
            while (cnt == maxThreads):
                type=(['http','https','socks4','socks5'])
                if (count==not_working+working):
                    aftTime=(tom())
                    print(" \r\n")
                    print("     [#] Finished Proxy API Analysis in "+str(aftTime-befTime)+" ")
                    print("     [#] "+str(working)+" working and "+str(not_working)+" not working ")
                    print("     [#] out of "+str(not_working+working)+" tested! ")
                    print("\r\n ")
                    cnt+=(1)
                    loop=(False)
                else:
                    aftTime=(tom())
                    print(" \r\n")
                    print("     [!] Minimal Error Found in Memory! {"+str(count)+":"+str(cnt)+"} ")
                    print("     [#] Finished Proxy API Analysis in "+str(aftTime-befTime)+" ")
                    print("     [#] "+str(working)+" working and "+str(not_working)+" not working ")
                    print("     [#] out of "+str(not_working+working)+" tested! ")
                    print("\r\n ")
                    cnt+=(1)
                    loop=(False)
                for t in type:
                    #cleanFile(str(t))
                    pass
                return
            else:
                pass
    except KeyboardInterrupt:
        return
try:
    os.system('cls' if os.name=='nt' else 'clear')
    print("""\r\n
        /---------------------------------------------\\
        |               Soteria Proxy Grabber          |
        \\---------------------------------------------/\
    """)
    print("\r\n ")
    print("     [#]  Starting Proxy API Analysis... (ctrl+c to stop)    ")
    print(" \r\n")
    while (threads < maxThreads):
        befTime=(tom())
        threading.Thread(target=run, args=(threads,)).start()
        threads+=(1)
    else:
        threading.Thread(target=finish).start()
    exit
except KeyboardInterrupt:
    loop=(False)
    print(" \r\n")
    print("     [#]  Force Stopped Proxy API Analysis!  ")
    print("     [#] "+str(working)+" working and "+str(not_working)+" not working   ")
    print("     [#] out of "+str(not_working+working)+" tested! ")
    print("\r\n ")
    exit