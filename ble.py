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
    for d in devices:       
        if 'Device1'in d.name:
            print('Found Device1')
            found = True
            async with BleakClient(d.address) as client:
                    while True:
                        val = await client.read_gatt_char(RED_LED_UUID)
                        print(val.decode('utf-8'))
                
                

    if not found:
        print('Could not find Device1')

                    
loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(run())
except KeyboardInterrupt:
    print('\nReceived Keyboard Interrupt')
finally:
    print('Program finished')
