import logging
import asyncio
import platform
import ast
import time
import csv

from bleak import BleakClient
from bleak import BleakScanner
from bleak import discover
import datetime as dt
import os


RED_LED_UUID = '19B10001-E8F2-537E-4F6C-D104768A1214'

RED = False


async def run():
    found = False
    devices = await discover()
    y=list()
    name = input("Enter subj name: ")
    hours = input("how many hours: ")
    print(int(hours) * 3600)
    try:
        os.mkdir(name)
    except OSError as error: 
        print(error)  
    for d in devices:       
        if 'Device1'in d.name:
            print('Found Device1')
            found = True
            async with BleakClient(d.address) as client:
                print(f'Connected to {d.address}')
                timeout = time.time() + (int(hours) * 3600)   #  3 hours from now
                t = dt.datetime.now()
                count = 0
                
                while time.time() < timeout:
                    delta = dt.datetime.now()-t
                    if delta.seconds >= 60:
                        count = count + 1
                        print("1 Min")
                        # Update 't' variable to new time
                        t = dt.datetime.now()
                        fileName = name + "\\" + name + "_" + str(count) + ".csv"
                        csv = open(fileName, 'w')
                        for line in y:
                             csv.write(str(line) + "\n")
                        csv.close()
                        y.clear()
                        
                    val = await client.read_gatt_char(RED_LED_UUID)
                    print(val.decode('utf-8'))
                    y.append(val.decode('utf-8'))

                

    if not found:
        print('Could not find Device1')

                    
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run())
except KeyboardInterrupt:
    print('\nReceived Keyboard Interrupt')
finally:
    print('Program finished')
