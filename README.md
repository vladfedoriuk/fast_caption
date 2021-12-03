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

- Install development requirements:
```commandline
pip install -r requirements/dev.txt
```
or
```commandline
make install-dev
```
- Bring up the services (PostgreSQL database and pgAdmin4):
```commandline
make services
```
- To perform migrations on the database:
  
```commandline
alembic upgrade head
```

- To autogenerate new migrations:
  
```commandline
alembic revision --autogenerate -m "Your message goes here"
```
Though be careful and **always** review what gets generated!

- Some useful links:
  - Migrations [docs](https://alembic.sqlalchemy.org/en/latest/autogenerate.html)
    
  - Asyncio with Alembic [docs](https://alembic.sqlalchemy.org/en/latest/cookbook.html#using-asyncio-with-alembic)

  - Async SQLAlchemy ORM [docs](https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html)

  - SQLModel [docs](https://sqlmodel.tiangolo.com/features/)
  - Project setup [guide](https://testdriven.io/blog/fastapi-sqlmodel/)

- Run the development server as follows:
```commandline
uvicorn main:app --reload
```
