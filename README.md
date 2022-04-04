# Elf-Mania
Pygame playground pour moi, et toi.

![](https://github.com/th3coop/Elf-Mania/workflows/lint_python/badge.svg)

## Requirements

 - Python 3
    > python -V
    Python 3.10.4
 - vitrualenv
 - pip

## Nice to haves
 - autoenv * autoenv doesn't exist on Windows ¯\_(ツ)_/¯


# Getting Started

### Clone it
- clone this repo with `git clone https://github.com/th3coop/Elf-Mania.git`
- `cd Elf-Mania`

### Set up the Virtual environment

Technically optional, but highly recommended.  If you don't want to use a virtual environemt, skip to the installing dependencies section below.

- In the repo, `virtualenv env`
- Activate the virtualenv (VE).  This depends on your setup so hopefully you know how to activate a VE on your computer.  I'm using powershell so I run `env\Scripts\activate.ps1`

*MAC*
- `cd .. && cd [repo-name]` # This activates the virtual env or just `source env/bin/activate` in the repo
 
*Windows Command Prompt*
- `env\bin\activate.bat` #activates the virtual env

*Linux* 
- initialize / enter the virtual environment with `source env/bin/activate`

### Installing Dependencies

- `pip install -r requirements.txt`

# Contributing

### Formatting
- autopep8

### Linting
- flake8

### Git
- work in a branch.  Everything should get a review.
