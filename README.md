# Elf-Mania
Pygame playground pour moi, et toi.

## Requirements

 - Python 3 (Note, there are some issues with this project and Python 3.7 on _Linux_, but Python 3.6 works! When the instructions below specify the `python` command, if you're on Linux you may need to use `python3.6` instead.)
 - vitrualenv
 - pip

## Nice to haves
 - autoenv * autoenv doesn't exist on Windows ¯\_(ツ)_/¯


## Getting Started

- clone this repo with `git clone https://github.com/th3coop/Elf-Mania.git`
- `cd Elf-Mania`

## Set up the Virtual environment

technically optional, but highly recommended. if you don't want to use a virtual environemt, skip to the installing dependencies section below.

- in the repe, `virtualenv env` # note that autoenv will try to start a non existant env... (on linux you may need to specify python 3.6 by running `python3.6 -m virtualenv env`)

*MAC*
 - `cd .. && cd [repo-name]` # This activates the virtual env or just `source env/bin/activate` in the repo
 
*Windows*
 - `env\bin\activate.bat` #activates the virtual env
- confirm that the virtual env activated by making sure it's using `pip` from your `env` folder

*Linux* 
- initialize / enter the virtual environment with `source env/bin/activate`

## Installing Dependencies

- `pip install -r requirements.txt` (again, on linux you may need to specify python 3.6 with `python3.6 -m pip install -r requirements.txt`)

## Running 

- `python elf.py`

## Workflow

### Formatting
- Use the `autopep8` formatter.  Ideally enable *format on save* in your editor using `autopep8`
- and use the `pylint` syntax checker

### Git
- work in a branch so if you need to push to `origin` (back to github)  `master`.
