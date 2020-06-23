import json, requests, sys
import socket, urllib3, time
import os, random, threading
from time import time as tom
cnt=(0)
ping=(0)
count=(0)
threads=(0)
working=(0)
loop=(True)
debugg=(False)
not_working=(0)
key=('Test-Key')
types=(['http','https','socks4','socks5'])
headers=({'Content-Type': 'application/json', 'Authorization': '{0}'.format(key)})
def debug(msg):
    global debugg
    if debugg:
        print("     [!]  Debug >> "+str(msg))
try:
    if sys.argv[1]:
        maxThreads=(int(sys.argv[1]))
    else:
        maxThreads=(10)
except Exception as e:
    debug(e)
    maxThreads=(10)
    with open("errors.dat", "a+") as f:
        f.write(str('No_Arg_MaxThreads'))
        f.write("\n")
try:
    if sys.argv[2]:
        perThread=(int(sys.argv[2]))
    else:
        perThread=(1)
except Exception as e:
    debug(e)
    perThread=(1)
    with open("errors.dat", "a+") as f:
        f.write(str('No_Arg_PerThread'))
        f.write("\n")
try:
    if sys.argv[3]:
        if int(sys.argv[3])==1:
            debugg=(True)
        else:
            debugg=(False)
    else:
        debugg=(False)
except Exception as e:
    debug(e)
    debugg=(False)
def getProxy(proxType):
    debug(proxType)
    api_url=('{0}{1}'.format("https://proxy.soteria.cf/", proxType))
    response=(requests.get(api_url, headers=headers))
    if response.status_code == 200:
        proxy=(json.loads(response.content.decode('utf-8')))
        debug(proxy)
        return proxy
    else:
        debug(json.loads(response.content.decode('utf-8')))
        return None
def check(proxy, proxType, url):
    global ping, working, not_working
    try:
        bef=(tom())
        requests.get(url,proxies={''+proxType:proxType+'://'+proxy},timeout=(2,5))
        aft=(tom())
        ping=(str(aft-bef))
        working+=(1)
        if timeSinceLastRun < 300:
            with open(str(proxType)+".dat", "a+") as f:
                f.write(proxy)
                debug(proxy)
                f.write("\n")
        else:
            with open(str(proxType)+".dat", "w") as f:
                f.write(proxy)
                debug(proxy)
                f.write("\n")
        return "Working!"
    except Exception as e:
        debug(e)
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
def cleanDupes(Type):
    try:
        uniqlines=(set(open(str(Type)+".dat").readlines()))
        out=(open(str(Type)+".temp.dat", 'w').writelines(uniqlines))
        with open(str(Type)+".temp.dat", "r") as f:
            out=(open(str(Type)+".dat", 'w').writelines(f.readlines()))
        os.remove(str(Type)+".temp.dat")
    except Exception as e:
        debug(e)
        with open("errors.dat", "a+") as f:
            f.write(str(e))
            f.write("\n")
def run(n):
    global cnt, count, perThread, ping
    try:
        p=(0)
        while (p < perThread):
            magic=(random.randint(1,4))
            if (magic==1):
                try:
                    count+=(1)
                    http=(getProxy('http'))
                    print(" [Thread-"+str(n)+"]    HTTP   = "+http[0]+":"+http[1]+" | "+str(check(http[0]+":"+http[1],'http',"http://www.google.com/"))+" | "+str(ping)+" ")
                except Exception as e:
                    debug(e)
                    print(" [Thread-"+str(n)+"]    HTTP   = Malformed Proxy Error   ")
            if (magic==2):
                try:
                    count+=(1)
                    https=(getProxy('https'))
                    print(" [Thread-"+str(n)+"]    HTTPS  = "+https[0]+":"+https[1]+" | "+str(check(https[0]+":"+https[1],'https',"https://www.google.com/"))+" | "+str(ping)+" ")
                except Exception as e:
                    debug(e)
                    print(" [Thread-"+str(n)+"]    HTTPS  = Malformed Proxy Error   ")
            if (magic==3):
                try:
                    count+=(1)
                    socks4=(getProxy('socks4'))
                    print(" [Thread-"+str(n)+"]    Socks4 = "+socks4[0]+":"+socks4[1]+" | "+str(check(socks4[0]+":"+socks4[1],'socks4',"https://www.google.com/"))+" | "+str(ping)+" ")
                except Exception as e:
                    debug(e)
                    print(" [Thread-"+str(n)+"]    Socks4 = Malformed Proxy Error   ")
            if (magic==4):
                try:
                    count+=(1)
                    socks5=(getProxy('socks5'))
                    print(" [Thread-"+str(n)+"]    Socks5 = "+socks5[0]+":"+socks5[1]+" | "+str(check(socks5[0]+":"+socks5[1],'socks5',"https://www.google.com/"))+" | "+str(ping)+" ")
                except Exception as e:
                    debug(e)
                    print(" [Thread-"+str(n)+"]    Socks5 = Malformed Proxy Error   ")
            p+=(1)
        else:
            debug('Thread '+str(n)+' Done!')
            cnt+=(1)
            return
    except KeyboardInterrupt:
        return
    except Exception as e:
        debug(e)
        with open("errors.dat", "a+") as f:
            f.write(str(e))
            f.write("\n")
def finish():
    global cnt, working, loop, not_working, befTime, count, types
    try:
        while (loop):
            while (cnt == maxThreads):
                for typ in types:
                    cleanDupes(typ)
                with open("time.dat", "w") as f:
                    f.write(str(tom()))
                if (count==not_working+working):
                    aftTime=(tom())
                    print(" \r\n")
                    print("     [#] Finished Proxy API Scraping in "+str(aftTime-befTime)+" ")
                    print("     [#] "+str(working)+" working and "+str(not_working)+" not working ")
                    print("     [#] out of "+str(not_working+working)+" tested! ")
                    print("\r\n ")
                    cnt+=(1)
                    loop=(False)
                else:
                    aftTime=(tom())
                    print(" \r\n")
                    print("     [!] Minimal Error Found in Memory! {"+str(count)+":"+str(cnt)+"} ")
                    print("     [#] Finished Proxy API Scraping in "+str(aftTime-befTime)+" ")
                    print("     [#] "+str(working)+" working and "+str(not_working)+" not working ")
                    print("     [#] out of "+str(not_working+working)+" tested! ")
                    print("\r\n ")
                    cnt+=(1)
                    loop=(False)
                return
            else:
                pass
    except KeyboardInterrupt:
        return
    except Exception as e:
        debug(e)
        with open("errors.dat", "a+") as f:
            f.write(str(e))
            f.write("\n")
if __name__ == "__main__":
    try:
        os.system('cls' if os.name=='nt' else 'clear')
        print("""\r\n\
  ____        _            _       
 / ___|  ___ | |_ ___ _ __(_) __ _ 
 \___ \ / _ \| __/ _ \ '__| |/ _` |
  ___) | (_) | ||  __/ |  | | (_| |
 |____/ \___/ \__\___|_|  |_|\__,_|""")
        print("\r\n ")
        with open("time.dat", "r") as f:
            timeSinceLastRun=(int(tom())-int(float(f.read())))
            debug(timeSinceLastRun)
        print("     [#]  Starting Proxy API Scraping... (ctrl+c to stop)    ")
        print(" \r\n")
        while (threads < maxThreads):
            befTime=(tom())
            threading.Thread(target=run, args=(threads,)).start()
            debug(threads)
            threads+=(1)
        else:
            threading.Thread(target=finish).start()
        exit
    except KeyboardInterrupt:
        loop=(False)
        print(" \r\n")
        print("     [#]  Force Stopped Proxy API Scraping!  ")
        print("     [#] "+str(working)+" working and "+str(not_working)+" not working   ")
        print("     [#] out of "+str(not_working+working)+" tested! ")
        print("\r\n ")
        exit
    except Exception as e:
        debug(e)
        with open("errors.dat", "a+") as f:
            f.write(str(e))
            f.write("\n")
