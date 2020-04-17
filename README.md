# Keyed-In
replace background in live webcam stream with no green screen

To get started, open terminal and execute the following commands:

1. Clone this repo with ```git clone https://github.com/paidforby/Keyed-In``` 
2. Move into the repo with ```cd Keyed-In``` or copy the contents in to a different folder
2. Install dependencies (inside of a virtualenv is recommended)  
```
sudo apt-get install v4l2loopback-utils
virtualenv .env  
source .env/bin/activate
pip install opencv-python ffmpeg-python
sudo modprobe v4l2loopback
```
4. Run `python main.py`
