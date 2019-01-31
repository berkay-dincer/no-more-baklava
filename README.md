# No-More-Baklava
This is a project to prevent people in Scotty to order desert when the victims computer is idle. Applies to pretty much every company I've worked at so far :)

## How it works:
This python program checks ioreg entries to measure the idle time of your computer. If it is greater than a certain threshold it activates your camera and tries to detect a human face.
If a face is detected it captures the image and saves it under images/ + locks your computer. I tailed to OS logs for 'SACLockScreenImmediate' and 'LUIAuthenticationServiceProvider' events to see if the mac is currently locked (let me know if there is a better way) if it is locked program will do nothing.




