# Xbox and Keyboard on Raspberry Pi for iMMO

This code enables you to use controllers and keyboards as input devices to play games with 4 to 50+ players. I call this an **Integer Massive Multiplayer Online** game: **iMMO**.

This solution was successfully tested during the **Global Game Jam 2025** 😊.

On a Raspberry Pi, Xbox controllers are recognized as generic HID (Human Interface Device) controllers. These scripts convert input from controllers and keyboards into **Index Integer values (`<ii`)**, which can then be used in your game logic.

I hope this helps!



# Steam Deck OS
```
https://www.reddit.com/r/SteamDeck/comments/x4ct1r/how_do_i_do_a_pip3_install/

I've also been trying to find a way to install pip on Deck and found this which worked for me. Installs pip3 in the home folder without the need for sudo or pacman.

Here is what to do:

Launch Konsole and run:

wget https://bootstrap.pypa.io/get-pip.py  
python3 get-pip.py --user
pip3 will be installed locally under ~/.local/bin/. You now need to add ~/.local/bin to $PATH. To do this, edit ~/.bashrc in something like nano, vim, or KWrite and add this to the end of the file:

if [ -d "$HOME/.local/bin" ]; then
  PATH="$HOME/.local/bin:$PATH"
fi
This checks if ~/.local/bin exists, and adds it to $PATH if it does.

Now run source ~/.bashrc to reload .bashrc, or just close Konsole and open it again.

Test it's working, run:

~/.local/bin/pip3 -V
Should output something like:

pip 22.2.2 from /home/deck/.local/lib/python3.10/site-packages/pip (python 3.10)
Now to install anything with pip, run:

pip3 install <package_name> --user
This will install the package in ~/.local/lib/python3.10/site-packages/

```