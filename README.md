# DIY_raspi_phone
This is a project I've been working on for a while, inspired by other projects online, like OURS phone and the tutorial on Core Electronics
Made using some parts I had (Raspberry Pi and screen), and the most compatible parts I could find online (4G hat and mini keyboard). 
This is my first time properly uploading a project to a github repo so I hope I'm doing this right. 
The main code file is flask_sms.py, which I access on my raspberry pi from a command, so it's basically an app. On my raspberry pi all the files are found in the Desktop, with sms_flask being a sub-folder on the desktop. If you want to change this, just change the file paths in flask_sms.py.
I'll attach .stls for the case, which isn't amazing but it does have a hinge that I'm very proud of.
There's some setup involved with linking the 4G hat's serial connection, and i'm not 100% sure that it's the same for everyone, i've done a LOT of googling, but I'll put my process in at some point.


## Link to products:

[4G Hat from Core Electronics](https://core-electronics.com.au/waveshare-4g-hat-for-raspberry-pi-lte-cat-4-4g-3g-2g-gnss.html)

[Raspberry Pi 3B+](https://core-electronics.com.au/raspberry-pi-3-model-b-plus.html) You could probably use a different pi but this is what I had

[5-inch LCD Display](https://www.jaycar.com.au/5-inch-touchscreen-with-hdmi-and-usb/p/XC9024?pos=19&queryId=1e9a4a1daaf2ba708a8a63e453d139f2&sort=relevance&searchText=5%20inch) Also available elsewhere. I've had this for ages and it still hasn't turned into a touchscreen, there are probably better options

[Mini wireless keyboard](https://www.amazon.com.au/Rii-Wireless-Full-Featured-Multimedia-Shortcuts/dp/B07D3JWVQV) Found this on amazon, it's not amazing for typing but it's got a touchpad which is really useful

Optional: [Raspberry Pi Camera](https://raspberry.piaustralia.com.au/collections/cameras), there's a port for it in the case, and you can make a camera app pretty easily with raspistill commands


## Using the mobile network
The 4G hat is connected by a serial connection to the raspberry pi through a USB cable.
To control the HAT through the serial connection, you use AT commands, which are commonly used in modems.
I definitely recommend using the [Waveshare Documentation](https://www.waveshare.com/wiki/SIM7600E-H_4G_HAT) for research, or if you want to change the code. I haven't been able to get an internet connection yet, but there's a guide on there you can try.



## This is what the phone looks like

![phone1](https://github.com/boatartist/DIY_raspi_phone/blob/main/phone1.jpg)
![phone2](https://github.com/boatartist/DIY_raspi_phone/blob/main/phone2.jpg)
