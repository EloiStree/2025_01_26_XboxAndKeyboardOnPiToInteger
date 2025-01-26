from evdev import list_devices
from evdev import InputDevice



import os
import sys

# Function to restart the current Python script
def restart_program():
    print("Restarting the program...")
    os.execv(sys.executable, ['python'] + sys.argv)


from evdev import InputDevice, categorize, ecodes
from evdev import InputDevice, categorize, ecodes, list_devices
from select import select

import time
import random
import socket
import struct
import asyncio



class Mapping_Keyword:
    def __init__(self, keyword, range_horizontal=32760, range_vertical=32760):
        self.keyword = keyword
        self.range_horizontal = range_horizontal
        self.range_vertical = range_vertical

class TargetIVP4:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        
class GamepadValue:    
    def __init__(self, path, range_horizontal=32760, range_vertical=32760, invert_horizontal=False, invert_vertical=False):
        self.path= path
        self.random_id=random.randint(-2000000000, 0)
        self.horizontal = 0
        self.vertical = 0
        self.range_horizontal = range_horizontal
        self.range_vertical = range_vertical
        self.pad = InputDevice(device_path)
        self.invert_horizontal = invert_horizontal
        self.invert_vertical = invert_vertical
  
        
    def turn_axis_to_range_1_99(self, axis):
        axis+=1
        axis*=0.5
        axis*=98
        axis+=1
        return int(axis)
    
    def get_int_1899999999_format(self):
        int_value =1800000000
        horizontal_99 = self.turn_axis_to_range_1_99(self.horizontal)
        vertical_99 = self.turn_axis_to_range_1_99(self.vertical)
        int_value+=horizontal_99 * 1000000
        int_value+=vertical_99   * 10000
        int_value+=horizontal_99 * 100
        int_value+=vertical_99   * 1
        
        return int_value
    
            
        
        

allows_gamepad =[]



gamepads =[]

        
        
target_ipv4="""
10.0.211.25:2504
10.0.211.24:2504
10.0.211.23:2504
10.0.211.21:2504
193.150.14.47:3615
"""



target_ipv4_class = []
# turn text in target

line = target_ipv4.split("\n")
for line in line:
    if line:
        ip, port = line.split(":")
        target = TargetIVP4(ip, port)
        print(target.ip, target.port)
        target_ipv4_class.append(target)
        

    


def push_index_integer(int_index, int_integer):
    # Convert integers to bytes (4 bytes each in little-endian order)
    byte_data = struct.pack("<ii", int_index, int_integer)
    print("Sending to targets:", byte_data)
    
    # Send the bytes to each target
    for t in target_ipv4_class:
        # Create a UDP socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Send data to each target IP and port
            s.sendto(byte_data, (t.ip, int(t.port)))
            print(f"Sent to {t.ip}:{t.port}:", byte_data)


def get_gamepad(device_path):
    for gamepad in gamepads:
        if gamepad.path == device_path:
            return gamepad
    return None












ban_keywords = ["keyboard", "mouse"]
allows_gamepad.append(Mapping_Keyword("Xbox Wireless Controller", 65535, 65535))
allows_gamepad.append(Mapping_Keyword("X-Box", 32760, 32760))
allows_gamepad.append(Mapping_Keyword("XBox", 32760, 32760))


devices = list_devices()

device_path_not_ban_or_registered = []
print("Connected Input Devices:")
for device_path in devices:
    device = InputDevice(device_path)
    device_name_low = device.name.lower()
  
    for allow_info in ban_keywords:
        if allow_info in device_name_low:
            continue
    
    bool_found = False
    for allow_info in allows_gamepad:
        if allow_info.keyword.lower() in device_name_low:
            
            print (f"\n\n\nADD IN LIST: {allow_info.keyword}")
            print(f"Device Path: {device.path}")
            print(f"  Device Name: {device.name}")
            print(f"  Device Type: {device.fn}")
            print(f"  Device Event Type(s): {device.capabilities()}")
            print (f"Range Horizontal: {allow_info.range_horizontal} Range Vertical: {allow_info.range_vertical}")
            print("-" * 40)
            print (f"\n\n\n")
            gamepads.append(GamepadValue(device.path, allow_info.range_horizontal, allow_info.range_vertical))
            bool_found = True
            break
    if not bool_found:
        print (f"NOT IN THE LIST")        
        print(f"Device Path: {device.path}")
        print(f"  Device Name: {device.name}")
        print(f"  Device Type: {device.fn}")
        print(f"  Device Event Type(s): {device.capabilities()}")
        print("-" * 40)
        device_path_not_ban_or_registered.append(f"{device.path} - {device.name}")
        
    

for device_path in device_path_not_ban_or_registered:
    print(f"Device Path: {device_path}")



    async def listen_to_gamepad(gamepad):
        pad = gamepad.pad
        print(f"Listening to {pad.path}...")
        print(f"Device name: {pad.name}")
        print(f"Device path: {pad.path}")

        try:
            async for event in pad.async_read_loop():
                if event.type == ecodes.EV_ABS:  # Axis movement (joystick movement)
                    abs_event = categorize(event)
                    print(f"Axis {abs_event.event.code} moved to {abs_event.event.value} ({pad.name})")
                    
                    
                    
                    if abs_event.event.code == 0:  # Horizontal
                        if gamepad.range_horizontal >40000:
                           gamepad.horizontal = max(-1.0, min(1.0, (abs_event.event.value / gamepad.range_horizontal)*2.0-1.0))
                        else :
                           gamepad.horizontal = max(-1.0, min(1.0, abs_event.event.value / gamepad.range_horizontal))
                        if gamepad.invert_horizontal:
                            gamepad.horizontal = -gamepad.horizontal
                           
                    elif abs_event.event.code == 1:  # Vertical axis
                        if gamepad.range_vertical >40000:
                            gamepad.vertical = max(-1.0, min(1.0, -((abs_event.event.value / gamepad.range_vertical)*2.0-1.0)))
                        else :
                            gamepad.vertical = max(-1.0, min(1.0, -abs_event.event.value / gamepad.range_vertical))
                        if gamepad.invert_vertical:
                            gamepad.vertical = -gamepad.vertical
                            
                    print (f"Horizontal: {gamepad.horizontal} Vertical: {gamepad.vertical}")
                    push_index_integer(gamepad.random_id, gamepad.get_int_1899999999_format())

                elif event.type == ecodes.EV_KEY:  # Button press or release
                    key_event = categorize(event)
                    if key_event.event.value == 1:  # Button pressed
                        print(f"Button {key_event.event.code} pressed")
                        # Handle button press
                        push_index_integer(gamepad.random_id, 1300)
                    elif key_event.event.value == 0:  # Button released
                        print(f"Button {key_event.event.code} released")
                        # Handle button release
                        push_index_integer(gamepad.random_id, 2300)
                        
                    if key_event.event.code == 314:
                        restart_program()

                elif event.type == ecodes.EV_SW:  # Switch event (D-pad)
                    switch_event = categorize(event)
                    print(f"Switch {switch_event.event.code} state: {switch_event.event.value}")

        except asyncio.CancelledError:
            print(f"\nExiting... for device {pad.path}")

        finally:
            pad.close()

    async def main():
        tasks = [listen_to_gamepad(gamepad) for gamepad in gamepads]
        await asyncio.gather(*tasks)

    if __name__ == "__main__":
        asyncio.run(main())