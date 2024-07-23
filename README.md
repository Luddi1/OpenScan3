<div id="top"></div>

# OpenScan3

<!-- ABOUT THE PROJECT -->
## About The Project

OpenScan3 is a firmware for controlling OpenScan devices, a family of OpenSource and OpenHardware devices designed to make photogrammetry accessible to everyone.

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

2. Install some python packages system wide. 
We need to do this anyway because `python3-picamera2` can not be installed via pip on a RPi4 (Not enough RAM apparently). 

```sh
sudo apt install -y python3-pip python3-venv python3-uvicorn python3-gphoto2 python3-pillow python3-picamera2 python3-matplotlib python3-fastapi python3-numpy python3-rpi.gpio python3-libcamera
```

3. Create a python virtual environment, include system-wide packages, and activate venv. 

```sh
cd
python3 -m venv --system-site-packages openscan-env
source openscan-env/bin/activate
```

4. Clone the repo

```sh
git clone https://github.com/Luddi1/OpenScan3.git
cd OpenScan3
```

5. Install the last necessary dependencies via pip. 

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

Now the api should be accessible from `http://local_ip:8000`

To access an api playground go to `http://local_ip:8000/docs`

If don't need a GUI you can already do a focus stack set with `tests/photoset.py`. 



<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- OpenScanConfig from single settings file
- Endstop homing routine
- Fix gphoto2 in get_cameras()
- picamera2 _get_camera() should not stop when focus or exposure settings are changed. 
- get_number_stacks() is hacky
- Download zip via API (compress_project_photos())

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


