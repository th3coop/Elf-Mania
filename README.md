# Elf-Mania
Pygame playground pour moi, et toi.

## Requirements

 - Python 3
 - vitrualenv

## Nice to haves
 - autoenv * autoenv doesn't exist on Windows ¯\_(ツ)_/¯

## Run

- clone this repo
- in the repe, `virtualenv env` # note that autoenv will try to start a non existant env...

*MAC*
 - `cd .. && cd [repo-name]` # This activates the virtual env or just `source env/bin/activate` in the repo
 
*Windows*
 - `env\bin\activate.bat` #activates the virtual env
- confirm that the virtual env activated by making sure it's using `pip` from your `env` folder

*MAC*
 - `which pip`
 
*Windows*
 - `where pip`
- if it's not using it...well, i'm not sure why the activation step wouldn't have worked for you but...get digging.  Feel free to let me know if you found an issue and i'll update this for the usecase you hit.
- `pip install -r requirements.txt`
- `python elf.py`

## Workflow

### Formatting
- Use the `autopep8` formatter.  Ideally enable *format on save* in your editor using `autopep8`
- and use the `pylint` syntax checker

### Git
- work in a branch so if you need to push to `origin` (back to github)  `master`.
