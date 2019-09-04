# no-more-baklava
This is a project to prevent people in [Scotty](https://www.scotty.app) to order desert when your computer is idle. Applies to pretty much every company I've worked at so far :)

## How it works:
This python program checks ioreg entries to measure the idle time of your computer. If it is greater than a certain threshold it activates your camera and tries to detect a human face.
If a face is detected it captures the image and saves it under images/ + locks your computer. I tailed the OS logs for 'SACLockScreenImmediate' and 'LUIAuthenticationServiceProvider' events to see if the mac is currently locked (let me know if there is a better way). If your computer is locked, it will not do anything.

### Requirements:
- Python 3.6
- Open CV




