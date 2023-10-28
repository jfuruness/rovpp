[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3100/)
![Tests](https://github.com/jfuruness/rovpp/actions/workflows/tests.yml/badge.svg)

# rovpp\_pkg

This package simulates ROV++. See ROV++ paper for further details. This package also currently extends BGPy (See CSET2023 BGPy paper for further details)

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

This package simulates ROV++. See ROV++ paper for further details. This package also currently extends BGPy (See CSET2023 BGPy paper for further details)

Everything described in the ROV++ paper has been implemented in the ROV++ package as an extension of BGPy.

In the as_classes folder you can see all of the various routing policies described in the paper.

rovpp_ann contains the ROV++ announcements used

In the tests directory, it contains the hundreds of system tests used to ensure that ROV++ is functioning properly.

In dunder main, it contains the code to create the graphs that were ultimately used in the final paper and can be used to reproduce results.

## Usage
* [rovpp\_pkg](#rovpp)

Note: the simulator takes about 1-2GB per core. Make sure you don't run out of RAM!

To reproduce the results in the paper, simply install the package in a pypy environment.
Then, simply type pypy3 -m rovpp

This will run the script used to generate all of the graphs used within the paper

Note: This takes a long time. We ran this on an AWS machine that has 128 cores, if you want to generate all of these graphs on a laptop it will take a day or two.

## Installation
* [rovpp\_pkg](#rovpp)

Install python and pip if you have not already. Then run:

```bash
# Needed for graphviz and Pillow
sudo apt-get install -y graphviz libjpeg-dev zlib1g-dev
pip3 install pip --upgrade
pip3 install wheel
pip install numpy --config-settings=setup-args="-Dallow-noblas=true"
```

For production:

```bash
pip3 install git@github.com:jfuruness/rovpp.git
```

This will install the package and all of it's python dependencies.

If you want to install the project for development:
```bash
git clone https://github.com/jfuruness/rovpp.git
cd rovpp
pip3 install -e .[test]
```

To test the development package: [Testing](#testing)


## Testing
* [rovpp\_pkg](#rovpp)

To test the package after installation:

```
cd rovpp
pytest rovpp --view
ruff rovpp
```

If you want to run it across multiple environments, and have python 3.9 installed:

```
cd rovpp
tox
```


## Development/Contributing
* [rovpp\_pkg](#rovpp)

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Add an engine test if you've made a change in the simulation_engine, or a system/unit test if the simulation_framework was modified
5. Run tox (for faster iterations: flake8, mypy, and pytest can be helpful)
6. Commit your changes: `git commit -am 'Add some feature'`
7. Push to the branch: `git push origin my-new-feature`
8. Ensure github actions are passing tests
9. Email me at jfuruness@gmail.com

## Credits
* [rovpp\_pkg](#rovpp)

Thanks to the SIDR team for their vast amount of help with this work. Namely Dr. Herzberg, Dr. Wang, Cameron Morris, and Reynaldo Morillo

## License
* [rovpp\_pkg](#rovpp)

BSD License (see license file)

## TODO
* [rovpp\_pkg](#rovpp)

See Jira

# Design Decisions

MYPY NOTES: Unfortunately, mypy seems to be completely broken for subclassing when the parent class has functions across multiple files.

Or perhaps it's just broken for subclassing in general.
Regardless, super dissapointing.
Because of this, so many lines need type ignores.
(because they have the error of incompatible with supertype, even though type hints are the same!)
I hope they fix this tool.

Ugh, multiple inheritance also completely breaks. ignoring everything is pointless, so I'm removing this alltogether

