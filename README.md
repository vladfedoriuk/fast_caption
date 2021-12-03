# *FAST CAPTION*
The API for a selected image captioning model.


### Development

- Add a `PyCharm` [plugin](https://plugins.jetbrains.com/plugin/12861-pydantic) to enable a better autocompletion.
- Configure a virtual environment. The projects runs with `Python 3.10.0`. An example of a virtual environment created 
  via `pyenv`:
  
```commandline
pyenv install 3.10.0
pyenv virtualenv 3.10.0 fast_caption
pyenv local fast_caption
```

- To  better manage the package versions and their dependencies consistency,
the project employs `pip-tools`.
  
* `pip-tools` installation and requirements compilation:
```
pip install pip-tools==6.4.0
make requirements
```

- Run the development server as follows:
```commandline
uvicorn main:app --reload
```
