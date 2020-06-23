#------------------------------------------------------------------IMPORTS-----------------------------------------------------------

from avwx.models import MetarSet
from metar import Metar
import datetime
import csv
import math
import ast
import threading
import os

#------------------------------------------------------------------INITIATION-----------------------------------------------------------

try:
        datafile=open('pilot.txt','r')
except FileNotFoundError:
        datafile=open('pilot.txt','x')
        datafile.close()
        datafile=open('pilot.txt','r')
data = datafile.read().splitlines()

datafile.close()
flightplans=[]
for i in data:
    flightplan=(i.strip('][').split(', ') )
    flightplans.append(flightplan)
fplanlist=[]
for flightplan in flightplans:
    finalfplan=[]
    for i in flightplan:
        try:
            i=i.replace("'","")
        except:
            pass
        try:
            i=float(i)
        except:
            if 'datetime.datetime' in i:
                i=i.replace(",","/")
                strip=''
                brack=False
                for x in i:
                    if x==')':
                        brack=False
                    if brack==True:
                        strip+=(x)
                    if x=='(':
                        brack=True
                strip=str(strip)
                i=datetime.datetime.strptime(strip, '%Y/%m/%d/%H/%M')

        finalfplan.append(i)
    fplanlist.append(finalfplan)
    
datafile=open('pilot.txt','a')
os.system("title FLIGHT SCHEDULE MANAGER")
os.system("color 01")

#------------------------------------------------------------------DEFINITIONS-----------------------------------------------------------

def getmetar(icao):
    try:
        icao = str(icao.upper())
        metar = MetarSet(icao)
        metar.refresh()
        metar = metar.get_latest()
        metar=(str(metar.raw_text))
        return str(metar)
    except Exception as e:
        return str(e)

class TestThreading(object):
    def __init__(self, interval=1):
        self.interval = interval

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while True:
            try:
                    for plan in fplanlist:
                        todate=datetime.datetime.now().date()
                        reqdate=plan[1].date()
                        if reqdate==todate:
                            reqtime=plan[1].strftime("%H:%M:%S")
                            told=0
                            if datetime.datetime.now().strftime("%H:%M:%S")==reqtime:
                                fplan=plan
                                if told==0:
                                    print(f'Your scheduled flight {fplan[0]} departs from {fplan[2]} headed to {fplan[4]} now.')
                                    time=1
                                else:
                                    time.sleep(2)
                                    told=0.
                        else:
                            continue
            except:
                    continue
                


def aptnamelatlon(icao):
    readrows=[]
    with open('airports.csv', newline='', encoding='utf-8') as apts:
        for i in csv.reader(apts):
            if str(i[1]).upper()==str(icao).upper():
                alist=[i[3],i[4],i[5]]
                return alist
            else:
                continue
        return [0,0,0]

def getdist(dpt,arr):
    R = 6373.0
    lat1 = math.radians(float(aptnamelatlon(dpt)[1]))
    lon1 = math.radians(float(aptnamelatlon(dpt)[2]))
    lat2 = math.radians(float(aptnamelatlon(arr)[1]))
    lon2 = math.radians(float(aptnamelatlon(arr)[2]))
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    return distance

def fliplan(t):
    callsign=input("CALLSIGN : ")
    while 1:
                        depticao=input("DEPT ICAO : ")
                        getmetar(depticao)
                        deptmetar=(getmetar(depticao)[0])
                        showdeptmetar=(getmetar(depticao)[1])
                        deptapt=aptnamelatlon(depticao)[0]
                        print("DEPARTURE AT :",deptapt)
                        print((showdeptmetar).upper())
                        print()
                        choice=input("PROCEED? (Y/N/E):")
                        if choice in 'Yy':
                                        break
                        elif choice in 'Nn':
                                        pass
                        elif choice in 'Ee':
                                        return None
    while 1:
                        arricao=input("ARR ICAO : ")
                        getmetar(arricao)
                        arrmetar=(getmetar(arricao)[0])
                        showarrmetar=(getmetar(arricao)[1])
                        arrapt=aptnamelatlon(arricao)[0]
                        print("ARRIVE AT :",arrapt)
                        print((showarrmetar).upper())
                        print()
                        choice=input("PROCEED? (Y/N/E):")
                        if choice in 'Yy':
                                        break
                        elif choice in 'Nn':
                                        pass
                        elif choice in 'Ee':
                                        return None
    distance=((getdist(depticao,arricao)))
    distancenm=distance/1.852
    kts=float(input("SPEED (in knots) : "))
    time=distancenm/kts
    alt=float(input("ALTITUDE (in FL) : "))
    rte=input("ROUTE : ")
    while 1:
            totfuel=float(input("FUEL (in lbs) : "))
            lfuel=rfuel=totfuel*0.8
            bfuel=totfuel*0.2
            load=float(input("LOAD (in lbs) : "))
            TOW=load+totfuel
            print("FUEL DISTRIBUTION : ",lfuel,"LEFT  |  ",bfuel,"CENTER  |  ",rfuel,"RIGHT")
            print("TOW (TAKE OFF WEIGHT) :",TOW)
            choice=input("PROCEED? (Y/N/E):")
            if choice in 'Yy':
                    break
            elif choice in 'Nn':
                    pass
            elif choice in 'Ee':
                    return None
    rem=input("REMARKS : ")
    #t=t.strftime('datetime.datetime(%Y,%m,%d,%H,%M)')
    #t=t.replace(", ",",")
    finalplan=[callsign,t,deptapt,deptmetar,arrapt,arrmetar,distancenm,time,kts,alt,rte,lfuel,bfuel,rfuel,load,rem]
    datafile.writelines([str(finalplan),'\n'])
    datafile.close()
    return finalplan

def fly(t=datetime.datetime.now().strftime('datetime.datetime(%Y,%m,%d,%H,%M)')):
    fplan=fliplan((t))
    os.system('cls')
    print('FLIGHT PLAN')
    print()
    print(f'''CALLSIGN : {fplan[0]}

SCHEDULED TIME OF DEPARTURE : {fplan[1]}

DEPARTURE AIRPORT : {fplan[2]}
METAR AT DEPARTURE AIRPORT : {fplan[3]}

ARRIVAL AIRPORT : {fplan[4]}
METAR AT ARRIVAL AIRPORT : {fplan[5]}

DISTANCE : {fplan[6]} NAUTICAL MILES
FLIGHT : {fplan[7]} HOURS
SPEED : {fplan[8]} KNOTS
CRUISE ALTITUDE : FL {fplan[9]}
ROUTE : {fplan[10]}

FUEL ON LEFT TANK : {fplan[11]} LBS
FUEL ON CENTER TANK : {fplan[12]} LBS
FUEL ON RIGHT TANK : {fplan[13]} LBS
LOAD IN CARGO/PASSENGER COMPARTMENTS : {fplan[14]} LBS

TOTAL TAKE OFF WEIGHT (TOW) : {fplan[11]+fplan[12]+fplan[13]+fplan[14]} LBS

REMARKS : {fplan[15]}''')

def schedulefly():
    while 1:
        year=int(input("YEAR : "))
        month=int(input("MONTH (IN NUMBERS) : "))
        date=int(input("DATE : "))
        hour=int(input("HOUR : "))
        minutes=int(input("MINUTES : "))
        t=datetime.datetime(year,month,date,hour,minutes,00,000000)
        print(f'SCHEDULE FLIGHT FOR {month}/{date}/{year} at {hour}:{minutes}')
        choice=input("PROCEED? (Y/N/E):")
        if choice in 'Yy':
                break
        elif choice in 'Nn':
                pass
        elif choice in 'Ee':
                return None
    fly(t)

def viewfplans():
    try:
            datafile=open('pilot.txt','r')
    except FileNotFoundError:
            datafile=open('pilot.txt','x')
            datafile.close()
            datafile=open('pilot.txt','r')
    data = datafile.read().splitlines()

    datafile.close()
    flightplans=[]
    for i in data:
        flightplan=(i.strip('][').split(', ') )
        flightplans.append(flightplan)
    fplanlist=[]
    for flightplan in flightplans:
        finalfplan=[]
        for i in flightplan:
            try:
                i.replace("'","")
            except:
                pass
            try:
                i=float(i)
            except:
                if 'datetime.datetime' in i:
                    i=i.replace(",","/")
                    strip=''
                    brack=False
                    for x in i:
                        if x==')':
                            brack=False
                        if brack==True:
                            strip+=(x)
                        if x=='(':
                            brack=True
                    strip=str(strip)
                    i=datetime.datetime.strptime(strip, '%Y/%m/%d/%H/%M')

            finalfplan.append(i)
        fplanlist.append(finalfplan)
        
    datafile=open('pilot.txt','a')
    htmllines=[]
    htmllines.append('''<html>
<title>FLIGHT SCHEDULE</title>
    <!-- Material Design Lite -->
    <script src="https://code.getmdl.io/1.3.0/material.min.js"></script>
    <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.red-deep_orange.min.css" />
    <!-- Material Design icon font -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
<script>
(function() {
  'use strict';
  window['counter'] = 0;
  var snackbarContainer = document.querySelector('#demo-toast-example');
  var showToastButton = document.querySelector('#demo-show-toast');
  showToastButton.addEventListener('click', function() {
    'use strict';
    var data = {message: 'Example Message # ' + ++counter};
    snackbarContainer.MaterialSnackbar.showSnackbar(data);
  });
}());
</script>
    <link rel="icon" type="image/png" href="https://webstockreview.net/images/airplane-clipart-logo-3.png"/>
<style>
html { overflow-y: scroll; overflow-x:hidden; scroll-behavior: smooth;}
body {position: absolute; }
#view-source {
position: fixed;
display: block;
right: 0;
bottom: 0;
margin-right: 40px;
margin-bottom: 40px;
z-index: 900;
}
.demo-card-wide.mdl-card {
  width: 70%;
}
.demo-card-wide-1.mdl-card {
  width: 100%;
}

.demo-card-wide-1 > .mdl-card__menu {
  color: #fff;
}

.mdl-layout {
  align-items: center;
  justify-content: center;
}
@media print
{
#view-source {display:none;}
#liawetmat {display:none;}
#liprnopo {display:none;}
#lliawetmat {display:none;}
#nlieawetmat {display:none;}
#m80 {display:none;}
#readys {display:none;}
#uniqwo {display:none;}
#unreadys {display:none;}
#noprrrrr {display:none;}
.demo-card-wide-1 {display:none;}
.noprint {display:none;}
.mdl-button-1 {display:none;}
}

@media screen
{
...
}
//.iframe-container {
//    overflow-x:scroll;
//    overflow-y: scroll;
//    padding-top: 56.25%;
//    position: relative;
//}
//.iframe-container iframe {
//   border: 0;
//   height: 100%;
//   left: 0;
//   position: absolute;
//   top: 0;
//   width: 100%;
//}
</style>
</head>
<body style="background-image:url('https://wallpaperaccess.com/full/445636.jpg'); background-size: cover; background-repeat: no-repeat; background-attachment: fixed;">
<br>
<div class="mdl-layout">
<div class="demo-card-wide mdl-card mdl-shadow--2dp through mdl-shadow--16dp" align="center">
<table class="mdl-data-table mdl-js-data-table" align="center">
<thead>
<tr>
<td class="mdl-data-table__cell--non-numeric">S.NO.</td>
<td class="mdl-data-table__cell--non-numeric">TIME AND DATE</td>
<td class="mdl-data-table__cell--non-numeric">CALLSIGN</td>
<td class="mdl-data-table__cell--non-numeric">DEPARTURE APT</td>
<td class="mdl-data-table__cell--non-numeric">ARRIVAL APT</td>
</tr>
</thead>
<tbody>''')
    count=0
    for plan in fplanlist:
        count+=1
        filename=str(count)+str(plan[0])+'.html'
        htmllines.append('''<tr>
<td class="mdl-data-table__cell--non-numeric">'''+str(count)+'''</td>
<td class="mdl-data-table__cell--non-numeric">'''+str(plan[1])+'''</td>
<td class="mdl-data-table__cell--non-numeric"><a href="'''+str(filename)+'''" target="_blank"><button class="mdl-button mdl-js-button mdl-js-ripple-effect">'''+plan[0]+'''</button></a></td>
<td class="mdl-data-table__cell--non-numeric">'''+plan[2]+'''</td>
<td class="mdl-data-table__cell--non-numeric">'''+plan[4]+'''</td>
</tr>''')
        personallines=[]
        personallines.append('''<html>
<title>'''+str(plan[0])+'''</title>
    <!-- Material Design Lite -->
    <script src="https://code.getmdl.io/1.3.0/material.min.js"></script>
    <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.red-deep_orange.min.css" />
    <!-- Material Design icon font -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
<script>
(function() {
  'use strict';
  window['counter'] = 0;
  var snackbarContainer = document.querySelector('#demo-toast-example');
  var showToastButton = document.querySelector('#demo-show-toast');
  showToastButton.addEventListener('click', function() {
    'use strict';
    var data = {message: 'Example Message # ' + ++counter};
    snackbarContainer.MaterialSnackbar.showSnackbar(data);
  });
}());
</script>
    <link rel="icon" type="image/png" href="https://webstockreview.net/images/airplane-clipart-logo-3.png"/>
<style>
html { overflow-y: scroll; overflow-x:hidden; scroll-behavior: smooth;}
body {position: absolute; }
#view-source {
position: fixed;
display: block;
right: 0;
bottom: 0;
margin-right: 40px;
margin-bottom: 40px;
z-index: 900;
}
.demo-card-wide.mdl-card {
  width: 85%;
}
.demo-card-wide-1.mdl-card {
  width: 100%;
}

.demo-card-wide-1 > .mdl-card__menu {
  color: #fff;
}

.mdl-layout {
  align-items: center;
  justify-content: center;
}
@media print
{
#view-source {display:none;}
#liawetmat {display:none;}
#liprnopo {display:none;}
#lliawetmat {display:none;}
#nlieawetmat {display:none;}
#m80 {display:none;}
#readys {display:none;}
#uniqwo {display:none;}
#unreadys {display:none;}
#noprrrrr {display:none;}
.demo-card-wide-1 {display:none;}
.noprint {display:none;}
.mdl-button-1 {display:none;}
}

@media screen
{
...
}
//.iframe-container {
//    overflow-x:scroll;
//    overflow-y: scroll;
//    padding-top: 56.25%;
//    position: relative;
//}
//.iframe-container iframe {
//   border: 0;
//   height: 100%;
//   left: 0;
//   position: absolute;
//   top: 0;
//   width: 100%;
//}
</style>
</head>
<body style="background-image:url('https://wallpaperaccess.com/full/445636.jpg'); background-size: cover; background-repeat: no-repeat; background-attachment: fixed;">
<br>
<div class="mdl-layout">
<div class="demo-card-wide mdl-card mdl-shadow--2dp through mdl-shadow--16dp" align="center">
<table class="mdl-data-table mdl-js-data-table" align="center">
<tbody>''')
        personallines.append('''<tr>
<td class="mdl-data-table__cell--non-numeric">CALLSIGN</td>
<td class="mdl-data-table__cell--non-numeric">'''+str(plan[0])+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">SCHEDULED TIME OF DEPARTURE</td>
<td class="mdl-data-table__cell--non-numeric">'''+str(plan[1])+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">DEPARTURE AIRPORT</td>
<td class="mdl-data-table__cell--non-numeric">'''+str(plan[2])+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">METAR AT DEPARTURE AIRPORT</td>
<td class="mdl-data-table__cell--non-numeric">'''+str(plan[3])+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">ARRIVAL AIRPORT</td>
<td class="mdl-data-table__cell--non-numeric">'''+str(plan[4])+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">METAR AT ARRIVAL AIRPORT</td>
<td class="mdl-data-table__cell--non-numeric">'''+str(plan[5])+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">DISTANCE</td>
<td class="mdl-data-table__cell--non-numeric">'''+f'{plan[6]} NAUTICAL MILES'+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">FLIGHT DURATION</td>
<td class="mdl-data-table__cell--non-numeric">'''+f'{plan[7]} HOURS'+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">CRUISE SPEED</td>
<td class="mdl-data-table__cell--non-numeric">'''+f'{plan[8]} KNOTS'+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">CRUISE ALTITUDE</td>
<td class="mdl-data-table__cell--non-numeric">'''+f'FL {plan[9]}'+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">ROUTE</td>
<td class="mdl-data-table__cell--non-numeric">'''+str(plan[10])+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">FUEL ON LEFT TANK</td>
<td class="mdl-data-table__cell--non-numeric">'''+f'{plan[11]} LBS'+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">FUEL ON CENTER TANK</td>
<td class="mdl-data-table__cell--non-numeric">'''+f'{plan[12]} LBS'+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">FUEL ON RIGHT TANK</td>
<td class="mdl-data-table__cell--non-numeric">'''+f'{plan[13]} LBS'+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">LOAD IN CARGO/PASSENGER COMPARTMENTS</td>
<td class="mdl-data-table__cell--non-numeric">'''+f'{plan[14]} LBS'+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">TOTAL TAKE OFF WEIGHT (TOW)</td>
<td class="mdl-data-table__cell--non-numeric">'''+f'{plan[11]+plan[12]+plan[13]+plan[14]} LBS'+'''</td>
</tr>
<tr>
<td class="mdl-data-table__cell--non-numeric">REMARKS</td>
<td class="mdl-data-table__cell--non-numeric">'''+str(plan[15])+'''</td>
</tr>''')
        filename=str(count)+str(plan[0])+'.html'
        with open(filename,'w') as html:
                html.writelines(personallines)
    with open('flights.html','w') as html:
        html.writelines(htmllines)
    os.system('flights.html')
def delfrmlog():
        try:
                count=1
                for plan in fplanlist:
                        print(f'{count}  |  {plan[0]}  |  {plan[1]}  |  {plan[2]} - {plan[3]}')
                        count+=1
                choice=int(input("DELETE S.#"))
                todelete=fplanlist.pop(choice-1)
                wplanlist=[]
                for i in fplanlist:
                        wplanlist.append((i))
                for i in wplanlist:
                        t=i[1]
                        t=t.strftime("'datetime.datetime(%Y,%m,%d,%H,%M)'")
                        t=t.replace(", ",",")
                        i[1]=t
                try:
                        filename=str(choice)+"'"+str(todelete[0])+"'.html"
                        os.remove(filename)
                        files = os.listdir(os.getcwd())
                        cnt=0
                
                        for src in files:
                                if src.endswith(".html"):
                                    cnt+=1
                                    for x in range(1,len(fplanlist)+1):
                                            if str(x) in src:
                                                    dst = src.replace(str(cnt), str(cnt+1))
                                            else:
                                                    dst=src
                                    os.rename(src, dst)
                except:
                        print('ERROR IN FILE HANDLING.')
                        return 0
                with open('pilot.txt','w') as file:
                        for i in wplanlist:
                                file.write(str(i))
                                file.write('\n')
                print(todelete[0],'DELETED.')
                
        except Exception as e:
                print('ERROR. FLIGHT PLAN COULD NOT BE DELETED.',e)