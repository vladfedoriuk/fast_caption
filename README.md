# *FAST CAPTION*
The API for a selected image captioning model.


### Development

- Add a `PyCharm` [plugin](https://plugins.jetbrains.com/plugin/12861-pydantic) to enable a better autocompletion.
- Configure a virtual environment. The projects runs with `Python 3.10.0`. An example of a virtual environment created 
  via `pyenv`:
  
```commandline
pyenv install 3.8.12
pyenv virtualenv 3.8.12 fast_caption
pyenv local fast_caption
```

- Create a `.env` file with the following environment variables:
```commandline
# PGADMIN
PGADMIN_DEFAULT_EMAIL=...  # insert your values
PGADMIN_DEFAULT_PASSWORD=...
PGADMIN_LISTEN_PORT=...

# DB
POSTGRES_USER=...
POSTGRES_PASSWORD=...
POSTGRES_DB=...

# Test DB
TEST_POSTGRES_DB=...
```

- Do not forget to modify the `alembic.ini` file:`sqlalchemy.url` must match the environment variables setup 

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
- Apparently, pip-tools do not handle tensorflow well, so install it manually:
  
```commandline
pip install tensorflow keras
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
  - Pydantic [docs](https://pydantic-docs.helpmanual.io/)
  - FastAPI [docs](https://fastapi.tiangolo.com/)

- Run the development server as follows:
```commandline
uvicorn main:app --reload
```
