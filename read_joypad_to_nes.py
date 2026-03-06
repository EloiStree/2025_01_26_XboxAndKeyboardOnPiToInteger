import os
import sys
from evdev import list_devices
from evdev import InputDevice
from evdev import InputDevice, categorize, ecodes
from evdev import InputDevice, categorize, ecodes, list_devices
from select import select
import time
import random
import socket
import struct
import asyncio


use_prind_for_iid=True
use_print=False
use_print_button_changed = False
use_print_axis_moved = False

start_gamepad_index = 1
bool_use_random_player_index = False


def get_ipv4_from_mdns(mdns_name):
    try:
        # Resolve the mDNS name to an IP address
        ip_address = socket.gethostbyname(mdns_name)
        return ip_address
    except socket.gaierror:
        print(f"Could not resolve mDNS name: {mdns_name}")
        return None

raspberry_pi_mdns_name = "raspberrypi.local"
raspberry_pi_ipv4 = get_ipv4_from_mdns(raspberry_pi_mdns_name)



target_ipv4="""
192.168.178.35:3615
127.0.0.1:3615
"""

if raspberry_pi_ipv4:
    target_ipv4 += f"{raspberry_pi_ipv4}:3615\n"


print(f"""
Use print for debugging is disabled.
Print consume a lot of performance, so it is recommended to disable it for better performance.
You can enable it by setting use_print to True in the code.

The message are send to:
{target_ipv4}          

If you add controller your need to restart the code.
OS and USB Hub are not the best at handling lot's of joypad.
Take that in consideration.

Starting index is at {start_gamepad_index}.
{"Random player index is enabled." if bool_use_random_player_index else "Random player index is disabled."}

This tool use the S2W NES convention:
https://github.com/EloiStree/s2w

And the IID convetion for transmitting the data:
https://github.com/EloiStree/iid

You can look at Godot Multi NES if you want to make a game yourself:
https://github.com/EloiStree/2026_01_18_gdp_nes_udp_multiplayer

          """)


def restart_program():
    if use_print:
        print("Restarting the program...")
    os.execv(sys.executable, ['python'] + sys.argv)



def display_all_devices_name_ignore_print():
    print("Available input devices:")
    for path in list_devices():
        dev = InputDevice(path)
        print(f"Name: {dev.name} \t\t\t Path: {dev.path}")
display_all_devices_name_ignore_print()


def display_device_information():
    if use_print:
        print("Available input devices:")
    for path in list_devices():
        dev = InputDevice(path)
        if use_print:
            print(f"Path: {dev.path}")
            print(f"Name: {dev.name}")
            print(f"Phys: {dev.phys}")
            print(f"Uniq: {dev.uniq}")
            print(f"Capabilities: {dev.capabilities()}")
            print("-" * 40)

def display_device_path_name():
    if use_print:
        print("Available input devices:")
    for path in list_devices():
        dev = InputDevice(path)
        if use_print:
            print(f"Path: |{dev.path}|{dev.name}")
            # dispaly button id
        
        if use_print:
            print("-" * 40)


def is_number_in_array(number, array):
    for element in array:
        if element == number:
            return True
    return False

def display_all_devices_full_information():
    if use_print:
        print("Available input devices:")
    for path in list_devices():
        dev = InputDevice(path)
        if use_print:
            print(f"Path: {dev.path}")
            print(f"Name: {dev.name}")
            print(f"Phys: {dev.phys}")
            print(f"Uniq: {dev.uniq}")
            print(f"Capabilities: {dev.capabilities()}")
            print("-" * 40)




class Mapping_Keyword:
    ## No logic, just information to create the gamepad reference and mapping depending of the hardware

    def __init__(self, device_name, range_horizontal=255, range_vertical=255, invert_horizontal=False, invert_vertical=False):
        self.device_name = device_name
        self.range_horizontal = range_horizontal
        self.range_vertical = range_vertical
        self.invert_horizontal = invert_horizontal
        self.invert_vertical = invert_vertical

        # https://github.com/EloiStree/s2w
        # Up Arrow	1281	2281	1291	2291
        # Right Arrow	1282	2282	1292	2292
        # Down Arrow	1283	2283	1293	2293
        # Left Arrow	1284	2284	1294	2294
        # A Button	1285	2285	1295	2295
        # B Button	1286	2286	1296	2296
        # Menu Left	1287	2287	1297	2297
        # Menu Right	1288	2288	1298	2298
        self.gamepad_name ="USB gamepad"
        self.gamepad_key_code_for_button_a = [304]
        self.gamepad_key_code_for_button_b = [305]
        self.gamepad_key_code_for_button_menu_left = [310]
        self.gamepad_key_code_for_button_menu_right = [311]

        # If not using the joystick as d-pad, you can set these to the button codes of the buttons you want to use as d-pad
        self.gamepad_key_code_for_button_arrow_up = [0]
        self.gamepad_key_code_for_button_arrow_right = [0]
        self.gamepad_key_code_for_button_arrow_down = [0]
        self.gamepad_key_code_for_button_arrow_left = [0]


        self.key_press_value_for_up_arrow_pressed = 1281
        self.key_press_value_for_right_arrow_pressed = 1282
        self.key_press_value_for_down_arrow_pressed = 1283
        self.key_press_value_for_left_arrow_pressed = 1284
        self.key_press_value_for_button_a_released = 1285
        self.key_press_value_for_button_b_released = 1286
        self.key_press_value_for_button_menu_left_released = 1287
        self.key_press_value_for_button_menu_right_released = 1288

    
    def set_native_gamepad_name(self, str_gamepad_name):
        self.gamepad_name = str_gamepad_name

    def set_native_button_a(self, int_key_code):
        self.gamepad_key_code_for_button_a = int_key_code

    def set_native_button_b(self, int_key_code):
        self.gamepad_key_code_for_button_b = int_key_code

    def set_native_button_menu_left(self, int_key_code):
        self.gamepad_key_code_for_button_menu_left = int_key_code

    def set_native_button_menu_right(self, int_key_code):
        self.gamepad_key_code_for_button_menu_right = int_key_code

    def set_native_button_to_listen(self, up,right,left,down, a, b, menu_left, menu_right):
        self.gamepad_key_code_for_button_arrow_up = up
        self.gamepad_key_code_for_button_arrow_right = right
        self.gamepad_key_code_for_button_arrow_down = down
        self.gamepad_key_code_for_button_arrow_left = left
        self.gamepad_key_code_for_button_a = a
        self.gamepad_key_code_for_button_b = b
        self.gamepad_key_code_for_button_menu_left = menu_left
        self.gamepad_key_code_for_button_menu_right = menu_right

    def set_integer_to_push_when_button_pressed(self, up,right,down,left, a, b, menu_left, menu_right):
        self.key_press_value_for_up_arrow_pressed = up
        self.key_press_value_for_right_arrow_pressed = right
        self.key_press_value_for_down_arrow_pressed = down
        self.key_press_value_for_left_arrow_pressed = left
        self.key_press_value_for_button_a = a
        self.key_press_value_for_button_b = b
        self.key_press_value_for_button_menu_left = menu_left
        self.key_press_value_for_button_menu_right = menu_right

class TargetIVP4:
    ## Who are we targeting
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
    


class GamepadValue:    
    ## Store the gamepad current state information with the device and mapping info.

    def __init__(self, path, mapping:Mapping_Keyword):
        self.path= path
        self.input_device = InputDevice(device_path)
        self.mapping = mapping
        self.player_index =random.randint(-2000000000, 0)
        self.up_arrow_pressed_previous = False
        self.up_arrow_pressed = False
        self.down_arrow_pressed_previous = False
        self.down_arrow_pressed = False
        self.right_arrow_pressed_previous = False
        self.right_arrow_pressed = False
        self.left_arrow_pressed_previous = False
        self.left_arrow_pressed = False
        self.horizontal = 0.0
        self.vertical = 0.0

    def set_found_index(self, index):
        self.player_index = index

        


# PRIVATE VARIABLES 
# SOME STORAGE BUT NOT CONFIGURABLE
allows_gamepad =[]
gamepads =[]
target_ipv4_class = []
device_path_not_ban_or_registered = []




def add_target_ipv4():
    global target_ipv4_class
    line = target_ipv4.split("\n")
    for line in line:
        if line:
            ip, port = line.split(":")
            target = TargetIVP4(ip, port)
            print(f"Adding target: {ip}:{port}")
            target_ipv4_class.append(target)
        
add_target_ipv4()


def push_index_integer(int_index, int_integer):
    # Convert integers to bytes (4 bytes each in little-endian order)
    byte_data = struct.pack("<ii", int_index, int_integer)
    if use_print:
        print(f"{int_index}| Sending to targets: {byte_data}")
    
    # Send the bytes to each target
    for t in target_ipv4_class:
        # Create a UDP socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Send data to each target IP and port
            s.sendto(byte_data, (t.ip, int(t.port)))
            #if use_print:
            print(f"Sent to {t.ip}:{t.port}")
    if use_prind_for_iid:
        print(f"{int_index}|{int_integer} ")


def get_gamepad(device_path):
    for gamepad in gamepads:
        if gamepad.path == device_path:
            return gamepad
    return None

pad_usb_gamepad = Mapping_Keyword("USB gamepad", 255, 255, False, False)
pad_usb_gamepad.set_native_button_to_listen([0], [0], [0], [0], [288,291,292], [289,290,293], [296], [297])
pad_usb_gamepad.set_integer_to_push_when_button_pressed(1281, 1282, 1283, 1284, 1285, 1286, 1287, 1288)


ban_keywords = ["keyboard", "mouse","Xbox","xbox","x-box","XBox","ps4","ps5","dualshock","dualsense"]
# allows_gamepad.append(Mapping_Keyword("Xbox Wireless Controller", 65535, 65535))
# allows_gamepad.append(Mapping_Keyword("X-Box", 32760, 32760))
# allows_gamepad.append(Mapping_Keyword("XBox", 32760, 32760))
allows_gamepad.append(pad_usb_gamepad)


## display_all_devices_full_information()

devices = list_devices()
if use_print:
    print("Connected Input Devices:")
for device_path in devices:
    device = InputDevice(device_path)
    device_name_low = device.name.lower()
  
    for ban_keyword in ban_keywords:
        if ban_keyword.lower() in device_name_low:
            continue
    
    bool_found = False
    for allow_info in allows_gamepad:
        if allow_info.device_name.lower() in device_name_low:

            if use_print:        
                print (f"\n\n\n> ADD IN LIST: {allow_info.device_name}")
                print(f"  Device Path: {device.path}")
                print(f"  Device Name: {device.name}")
                print(f"  Device Type: {device.fd}")
                print(f"  Device Event Type(s): {device.capabilities()}")
                print (f" Range Horizontal: {allow_info.range_horizontal} Range Vertical: {allow_info.range_vertical}")
                print("-" * 40)
                print (f"\n\n\n")
            pad = GamepadValue(device.path, allow_info)
            number_gamepad = len(gamepads)
            if bool_use_random_player_index:
                pad.set_found_index(random.randint(-2000000000, 0))
            else:
                pad.set_found_index(start_gamepad_index + number_gamepad)

            gamepads.append(pad)
            bool_found = True
            if use_print:
                print (f"COUNT GAMEPAD: {len(gamepads)}")
            break
    if not bool_found:
        if use_print:
            print(f"\n\n\n> NOT IN THE LIST")        
            print(f"  Device Path: {device.path}")
            print(f"  Device Name: {device.name}")
            print(f"  Device Type: {device.fd}")
            print(f"  Device Event Type(s): {device.capabilities()}")
            print("-" * 40)
            print (f"\n\n\n")
        device_path_not_ban_or_registered.append(f"{device.path} - {device.name}")
        

for device_path in device_path_not_ban_or_registered:
    if use_print:
        print(f"Device Path: {device_path}")

    async def listen_to_gamepad(gamepad):
        input_device_found = gamepad.input_device
        if use_print:
            print(f"Listening to {input_device_found.path}...")
            print(f"Device name: {input_device_found.name}")
            print(f"Player Index: {gamepad.player_index}")
    

        try:
            async for event in input_device_found.async_read_loop():
                if event.type == ecodes.EV_ABS:  # Axis movement (joystick movement)
                    abs_event = categorize(event)
                    if use_print and use_print_axis_moved:
                        print(f"Axis {abs_event.event.code} moved to {abs_event.event.value} ({input_device_found.name})")
                    
                    new_horizontal = 0
                    new_vertical = 0
                    
                    if abs_event.event.code == 0:  # Horizontal
                        
                        new_horizontal = max(-1.0, min(1.0, (abs_event.event.value / gamepad.mapping.range_horizontal)*2.0-1.0))
                       
                        if gamepad.mapping.invert_horizontal:
                            new_horizontal = -new_horizontal
                           
                    elif abs_event.event.code == 1:  # Vertical axis
                        new_vertical = max(-1.0, min(1.0, -((abs_event.event.value / gamepad.mapping.range_vertical)*2.0-1.0)))
                        if gamepad.mapping.invert_vertical:
                            new_vertical = -new_vertical
                    
                    death_zone =0.35

                    gamepad.up_arrow_pressed_previous = gamepad.up_arrow_pressed
                    gamepad.down_arrow_pressed_previous = gamepad.down_arrow_pressed
                    gamepad.right_arrow_pressed_previous = gamepad.right_arrow_pressed
                    gamepad.left_arrow_pressed_previous = gamepad.left_arrow_pressed

                    gamepad.up_arrow_pressed = new_vertical >= death_zone 
                    gamepad.down_arrow_pressed = new_vertical <= -death_zone 
                    gamepad.right_arrow_pressed = new_horizontal >= death_zone
                    gamepad.left_arrow_pressed = new_horizontal <= -death_zone

                    bool_changed =False

                    if gamepad.up_arrow_pressed != gamepad.up_arrow_pressed_previous:
                        bool_changed=True
                        if gamepad.up_arrow_pressed:
                            if use_print and use_print_button_changed:
                                print(f"Up arrow pressed ({gamepad.mapping.key_press_value_for_up_arrow_pressed})")
                            push_index_integer(gamepad.player_index, gamepad.mapping.key_press_value_for_up_arrow_pressed)
                        else:
                            if use_print and use_print_button_changed:
                                print(f"Up arrow released ({gamepad.mapping.key_press_value_for_up_arrow_pressed+1000})")
                            push_index_integer(gamepad.player_index, gamepad.mapping.key_press_value_for_up_arrow_pressed+1000)
                    if gamepad.down_arrow_pressed != gamepad.down_arrow_pressed_previous:
                        bool_changed=True
                        if gamepad.down_arrow_pressed:
                            if use_print and use_print_button_changed:
                                print(f"Down arrow pressed ({gamepad.mapping.key_press_value_for_down_arrow_pressed})")
                            push_index_integer(gamepad.player_index, gamepad.mapping.key_press_value_for_down_arrow_pressed)
                        else:
                            if use_print and use_print_button_changed:
                                print(f"Down arrow released ({gamepad.mapping.key_press_value_for_down_arrow_pressed+1000})")
                            push_index_integer(gamepad.player_index, gamepad.mapping.key_press_value_for_down_arrow_pressed+1000)
                    if gamepad.right_arrow_pressed != gamepad.right_arrow_pressed_previous:
                        bool_changed=True
                        if gamepad.right_arrow_pressed:
                            if use_print and use_print_button_changed:
                                print(f"Right arrow pressed ({gamepad.mapping.key_press_value_for_right_arrow_pressed})")
                            push_index_integer(gamepad.player_index, gamepad.mapping.key_press_value_for_right_arrow_pressed)
                        else:
                            if use_print and use_print_button_changed:
                                print(f"Right arrow released ({gamepad.mapping.key_press_value_for_right_arrow_pressed+1000})")
                            push_index_integer(gamepad.player_index, gamepad.mapping.key_press_value_for_right_arrow_pressed+1000)
                    if gamepad.left_arrow_pressed != gamepad.left_arrow_pressed_previous:
                        bool_changed=True
                        if gamepad.left_arrow_pressed:
                            if use_print and use_print_button_changed:
                                print(f"Left arrow pressed ({gamepad.mapping.key_press_value_for_left_arrow_pressed})")
                            push_index_integer(gamepad.player_index, gamepad.mapping.key_press_value_for_left_arrow_pressed)
                        else:
                            if use_print and use_print_button_changed:
                                print(f"Left arrow released ({gamepad.mapping.key_press_value_for_left_arrow_pressed+1000})")
                            push_index_integer(gamepad.player_index, gamepad.mapping.key_press_value_for_left_arrow_pressed+1000)
                    
                    gamepad.horizontal = new_horizontal
                    gamepad.vertical = new_vertical
                            
                    if bool_changed:
                        if use_print and use_print_axis_moved:
                            print (f"Horizontal: {gamepad.horizontal} Vertical: {gamepad.vertical}")

                elif event.type == ecodes.EV_KEY:  # Button press or release
                    key_event = categorize(event)
                    int_key_code = key_event.event.code
                    button_name = ""
                    button_key_to_push = 0
                    if is_number_in_array(int_key_code, gamepad.mapping.gamepad_key_code_for_button_a):
                        button_name = "Button A"
                        button_key_to_push = gamepad.mapping.key_press_value_for_button_a
                    elif is_number_in_array(int_key_code, gamepad.mapping.gamepad_key_code_for_button_b):
                        button_name = "Button B"
                        button_key_to_push = gamepad.mapping.key_press_value_for_button_b
                    elif is_number_in_array(int_key_code, gamepad.mapping.gamepad_key_code_for_button_menu_left):
                        button_name = "Menu Left"
                        button_key_to_push = gamepad.mapping.key_press_value_for_button_menu_left
                    elif is_number_in_array(int_key_code, gamepad.mapping.gamepad_key_code_for_button_menu_right):
                        button_name = "Menu Right"
                        button_key_to_push = gamepad.mapping.key_press_value_for_button_menu_right
                    elif is_number_in_array(int_key_code, gamepad.mapping.gamepad_key_code_for_button_arrow_up):
                        button_name = "Arrow Up"
                        button_key_to_push = gamepad.mapping.key_press_value_for_up_arrow_pressed
                    elif is_number_in_array(int_key_code, gamepad.mapping.gamepad_key_code_for_button_arrow_right):
                        button_name = "Arrow Right"
                        button_key_to_push = gamepad.mapping.key_press_value_for_right_arrow_pressed
                    elif is_number_in_array(int_key_code, gamepad.mapping.gamepad_key_code_for_button_arrow_down):
                        button_name = "Arrow Down"
                        button_key_to_push = gamepad.mapping.key_press_value_for_down_arrow_pressed
                    elif is_number_in_array(int_key_code, gamepad.mapping.gamepad_key_code_for_button_arrow_left):
                        button_name = "Arrow Left"
                        button_key_to_push = gamepad.mapping.key_press_value_for_left_arrow_pressed
                    else:
                        button_name = f"Unknown Button (code {int_key_code})"
                    

                    if key_event.event.value == 1:  # Button pressed

                        if use_print and use_print_button_changed:
                            print(f"Button {key_event.event.code} pressed ({button_name} - {button_key_to_push})")
                        # Handle button press
                        push_index_integer(gamepad.player_index, button_key_to_push)
                    elif key_event.event.value == 0:  # Button released
                        if use_print and use_print_button_changed:
                            print(f"Button {key_event.event.code} released ({button_name} - {button_key_to_push+1000})")
                        # Handle button release
                        push_index_integer(gamepad.player_index, button_key_to_push + 1000)
                        
                    # if key_event.event.code == 314:
                    #     restart_program()

                elif event.type == ecodes.EV_SW:  # Switch event (D-pad)
                    switch_event = categorize(event)
                    if use_print:
                        print(f"Switch {switch_event.event.code} changed to {switch_event.event.value} ({input_device_found.name})")

        except asyncio.CancelledError:
            print(f"\nExiting... for device {input_device_found.path}")

        finally:
            input_device_found.close()

    async def main():
        tasks = [listen_to_gamepad(gamepad) for gamepad in gamepads]
        await asyncio.gather(*tasks)

    if __name__ == "__main__":
        asyncio.run(main())