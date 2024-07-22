<div id="top"></div>

# OpenScan3

<!-- ABOUT THE PROJECT -->
## About The Project

OpenScan3 is a firmware for controlling OpenScan devices, a family of OpenSource and OpenHardware devices designed to make photogametry accessible to everyone.

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To run a copy of the firmware in your RPi you can follow of two routes

### Install OpenScanPi image (recommended)

TO BE DONE

### Install manually

#### Prerequisites

 - RPi running the latest image of Raspberry OS

#### Installation

1. Update the system

```sh
sudo apt update && sudo apt upgrade -y
```

2. Install some python packages system wide. 
We need to do this anyway because `python3-picamera2` can not be installed via pip on a RPI4 (Not enough RAM apparently). 

```sh
sudo apt install -y python3-pip python3-venv python3-uvicorn python3-gphoto2 python3-pillow python3-picamera2 python3-matplotlib python3-fastapi python3-numpy python3-rpi.gpio python3-libcamera
```

3. Create a python virtual environment, include system-wide packages, and activate venv. 

```sh
python3 -m venv --system-site-packages openscan-env
source openscan-env/bin/activate
```

4. Clone the repo

```sh
git clone https://github.com/OpenScan-org/OpenScan3.git
cd OpenScan3
```

5. Install the last necessary dependencies via pip. 

```sh
pip install v4l2py orjson python-dotenv
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

To run the api backend run:
```sh
source openscan-env/bin/activat
python3 -m uvicorn app.main:app --host 0.0.0.0
```

Now the api should be accessible from `http://local_ip:8000`

To access an api playground go to `http://local_ip:8000/docs`

_For more information, please refer to the [Documentation](https://example.com)_



**Add ramdisk to improve capturing speed (if space available)**


```ini
#/etc/fstab

proc            /proc           proc    defaults          0       0
PARTUUID=e46ea0e2-01  /boot           vfat    defaults          0       2
PARTUUID=e46ea0e2-02  /               ext4    defaults,noatime  0       1
# a swapfile is not a swap partition, no line here
#   use  dphys-swapfile swap[on|off]  for that


tmpfs /mnt/ramdisk tmpfs nodev,nosuid,size=256M 0 0

```
Then start the server

```sh
TMPDIR=/mnt/ramdisk uvicorn app.main:app --host 0.0.0.0
```

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Full camera control
- [ ] Full motor and other hardware control
- [ ] Extra features
    - [ ] Network drive
    - [ ] ...


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



<!-- CONTACT -->
## Contact

TO BE DONE

<p align="right">(<a href="#top">back to top</a>)</p>




