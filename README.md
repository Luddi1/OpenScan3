<div id="top"></div>

# OpenScan3

<!-- ABOUT THE PROJECT -->
## About The Project

OpenScan3 is a firmware for controlling OpenScan devices, a family of OpenSource and OpenHardware devices designed to make photogrammetry accessible to everyone.

This fork of OS3 is currently only tested on an OpenScan midi, with RPi4, the new (black) shield, and imx519 camera. 

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

### Install manually

#### Prerequisites

Install Raspberry Pi OS with the [Raspberry Pi Imager](https://www.raspberrypi.com/software/), supplying wifi and ssh login credentials. 

#### Installation

Log-in via SSH to the RPi and issue the following commands. 

1. Update the system

```sh
sudo apt update && sudo apt upgrade -y
```

2. If using imx519: Install driver, following the guide at [Arducam](https://docs.arducam.com/Raspberry-Pi-Camera/Native-camera/16MP-IMX519/). 
Here is the short version:
```sh
mkdir ~/imx519
cd ~/imx519
wget -O install_pivariety_pkgs.sh https://github.com/ArduCAM/Arducam-Pivariety-V4L2-Driver/releases/download/install_script/install_pivariety_pkgs.sh
chmod +x install_pivariety_pkgs.sh
./install_pivariety_pkgs.sh -p libcamera_dev
./install_pivariety_pkgs.sh -p libcamera_apps
cd ~
rm -rf ~/imx519
sudo sh -c "echo 'dtoverlay=imx519' >> /boot/firmware/config.txt"
```

3. Install some python packages system wide. 
We need to do this anyway because `python3-picamera2` can not be installed via pip on a RPi4 (Not enough RAM apparently). 

```sh
sudo apt install -y git python3-pip python3-venv python3-uvicorn python3-gphoto2 python3-pillow python3-picamera2 python3-matplotlib python3-fastapi python3-numpy python3-rpi.gpio python3-libcamera
```

4. Create a python virtual environment, include system-wide packages, and activate venv. 

```sh
cd
python3 -m venv --system-site-packages openscan-env
source openscan-env/bin/activate
```

5. Clone the repo

```sh
git clone https://github.com/Luddi1/OpenScan3.git
cd OpenScan3
```

6. Install the last necessary dependencies via pip. 

```sh
pip install v4l2py orjson python-dotenv pydantic
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
### Usage

To run the api backend run:
```sh
source ~/openscan-env/bin/activate
cd ~/OpenScan3
python3 -m uvicorn app.main:app --host 0.0.0.0
```
Adjust the pin numbers for your setup in `app/config/openscan.py`. 
Currently, it is setup for the new (black) shield. 

Now the api should be accessible from `http://local_ip:8000`. 
To access an api playground go to `http://local_ip:8000/docs`

If you don't need a GUI you can already do a focus stack set with `tests/photoset.py`. 
Open another SSH session, then run 
```sh
source ~/openscan-env/bin/activate
cd ~/OpenScan3/tests
python3 photoset.py
```
Adjust values to your needs, before. 

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- Add safety timeout to endstop homing routine
- Check if motor dir settings works with endstop_angle, max_angle in both directions
- Rotate images 90 degrees
- Adjust /scanning for focus stacking
- OpenScanConfig from single settings file
- Download zip via API (compress_project_photos())
- Add histogram to preview

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GPL-3.0 license. See `LICENSE` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>


