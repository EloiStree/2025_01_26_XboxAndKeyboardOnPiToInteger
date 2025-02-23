from evdev import InputDevice, categorize, ecodes, list_devices
from select import select

import time
import random
import socket
import struct


gamepads =[]

class TargetIVP4:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        
class GamepadValue:    
    def __init__(self, path):
        self.path= path
        self.random_id=random.randint(-2000000000, 0)
        self.horizontal = 0
        self.vertical = 0
        self.is_left_down = False
        self.is_right_down = False
        self.is_up_down = False
        self.is_down_down = False
        self.is_attack_down = False
        
    def refresh_axis(self):
        if self.is_left_down and not self.is_right_down:
            self.horizontal = -1
        elif self.is_right_down and not self.is_left_down:
            self.horizontal = 1
        else:
            self.horizontal = 0
            
        if self.is_up_down and not self.is_down_down:
            self.vertical = 1
        elif self.is_down_down and not self.is_up_down:
            self.vertical = -1
        else:
            self.vertical = 0
        
    
        
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

KEY_LEFT = "KEY_A"
KEY_RIGHT = "KEY_D"
KEY_UP = "KEY_W"
KEY_DOWN = "KEY_S"
KEY_ATTACK= "KEY_SPACE"



if __name__ == "__main__":
    
    while True:
        gamepads.clear()
        # List all input devices
        devices = [InputDevice(path) for path in list_devices()]
        print("Devices:")
        for d in devices:
            print(d)

        # Filter only keyboard devices
        keyboards = [device for device in devices if 'keyboard' in device.name.lower()]
        print("Keyboard:")
        for k in keyboards:
            print(k)
        
        print("Listening to the following keyboards:")
        for keyboard in keyboards:
            print(f">> {keyboard.path}: {keyboard.name}")

        # Open devices for reading
        devices = [InputDevice(keyboard.path) for keyboard in keyboards]

        # Monitor multiple keyboards
        bool_quit = True
        while bool_quit:
            r, _, _ = select(devices, [], [])
            for device in r:
                for event in device.read():
                    if event.type == ecodes.EV_KEY:
                        key_event = categorize(event)
                        
                        ## If hold continue
                        if key_event.keystate == key_event.key_hold:
                            continue
                        str_key =  str(key_event.keycode)
                        gamepad_ref = get_gamepad(device.path)
                        if gamepad_ref is None:
                            gamepad_ref = GamepadValue(device.path)
                            gamepads.append(gamepad_ref)
                        
                        
                        
                        
                        
                        print(f"KEY: {str_key}")
                        print(f"Device {device.path}({gamepad_ref.random_id}): {key_event}")
                        print(f"Key Event: {key_event.keycode}, {key_event.keystate}")
                        
                        if str_key== KEY_LEFT:
                            if  key_event.keystate == key_event.key_down:
                                gamepad_ref.is_left_down = True
                            elif key_event.keystate == key_event.key_up:
                                gamepad_ref.is_left_down = False
                                
                        elif str_key == KEY_RIGHT:
                            if key_event.keystate == key_event.key_down:
                                gamepad_ref.is_right_down = True
                            elif key_event.keystate == key_event.key_up:
                                gamepad_ref.is_right_down = False
                                
                        elif str_key== KEY_UP:
                            if key_event.keystate == key_event.key_down:
                                gamepad_ref.is_up_down = True
                            elif key_event.keystate == key_event.key_up:
                                gamepad_ref.is_up_down = False
                        elif str_key == KEY_DOWN:
                            if key_event.keystate == key_event.key_down:
                                gamepad_ref.is_down_down = True
                            elif key_event.keystate == key_event.key_up:
                                gamepad_ref.is_down_down = False
                        elif str_key == KEY_ATTACK:
                            if key_event.keystate == key_event.key_down:
                                push_index_integer(gamepad_ref.random_id, 1300)
                            else :
                                push_index_integer(gamepad_ref.random_id, 2300)
                        gamepad_ref.refresh_axis()
                        #print gamepad axis
                        print(f"X:{gamepad_ref.horizontal} Y:{ gamepad_ref.vertical}")        
                
                        int_value = gamepad_ref.get_int_1899999999_format()
                        print(f"Int value: {int_value}")
                        push_index_integer(gamepad_ref.random_id, int_value)
                        
                        if key_event.keystate == key_event.key_down:
                            if key_event.keycode == 'KEY_ESC':
                                bool_quit = False
            