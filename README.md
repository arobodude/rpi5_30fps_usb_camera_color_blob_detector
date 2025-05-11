# rpi5_30fps_usb_camera_color_blob_detector
Color detector for the Raspberry Pi 5. Runs at 30fps with a USB camera

Create a python virtual environment

cd ~
python3 -m venv colordetect
source colordetect/bin/activate

Install OpenCV
pip install opencv-python

Run the detector
python3 red_detector_fps.py


Currently it's set to detect the color red but that can be adjusted
