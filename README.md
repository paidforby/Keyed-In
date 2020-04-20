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

After running `main.py`, you should have another webcam device, such as `/dev/video1`, you can test this video device by running something like `ffplay /dev/video1`  
NOTE: this code barely works. Unless you have a specific use case in mind, I highly recommend to just buy a stack of green construction paper and tape it to your wall and then use the chroma key feature in an open source software suite such as, [OBS-Studio](https://github.com/obsproject/obs-studio).
