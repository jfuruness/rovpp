[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
![Tests](https://github.com/jfuruness/rovpp_pkg/actions/workflows/tests.yml/badge.svg)

# rovpp\_pkg
This package simulates ROV++. See paper (TODO: Add link) for further details

* [Description](#package-description)
* [Usage](#usage)
* [Installation](#installation)
* [Testing](#testing)
* [Development/Contributing](#developmentcontributing)
* [History](#history)
* [Credits](#credits)
* [Licence](#license)
* [TODO](#todo)

## Package Description

TODO

## Usage
* [rovpp\_pkg](#rovpp_pkg)

Note: the simulator takes about 1-2GB per core. Make sure you don't run out of RAM!

TODO

## Installation
* [rovpp\_pkg](#rovpp_pkg)

Install python and pip if you have not already. Then run:

```bash
# Needed for graphviz and Pillow
sudo apt-get install -y graphviz libjpeg-dev zlib1g-dev
pip3 install pip --upgrade
pip3 install wheel
```

For production:

```bash
pip3 install git@github.com:jfuruness/rovpp_pkg.git
```

This will install the package and all of it's python dependencies.

If you want to install the project for development:
```bash
git clone https://github.com/jfuruness/rovpp_pkg.git
cd rovpp_pkg
pip3 install -e .[test]
```

To test the development package: [Testing](#testing)


## Testing
* [rovpp\_pkg](#rovpp_pkg)

To test the package after installation:

```
cd rovpp_pkg
pytest rovpp_pkg
flake8 rovpp_pkg
mypy rovpp_pkg
```

If you want to run it across multiple environments, and have python 3.9 installed:

```
cd rovpp_pkg
tox
```


## Development/Contributing
* [rovpp\_pkg](#rovpp_pkg)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Add an engine test if you've made a change in the simulation_engine, or a system/unit test if the simulation_framework was modified
5. Run tox (for faster iterations: flake8, mypy, and pytest can be helpful)
6. Commit your changes: `git commit -am 'Add some feature'`
7. Push to the branch: `git push origin my-new-feature`
8. Ensure github actions are passing tests
9. Email me at jfuruness@gmail.com

## History
* [rovpp\_pkg](#rovpp_pkg)

* 0.1.0 First working version

## Credits
* [rovpp\_pkg](#rovpp_pkg)

Thanks to the SIDR team for their vast amount of help with this work. Namely Dr. Herzberg, Dr. Wang, Cameron Morris, and Reynaldo Morillo

## License
* [rovpp\_pkg](#rovpp_pkg)

BSD License (see license file)

## TODO
* [rovpp\_pkg](#rovpp_pkg)

See Jira
