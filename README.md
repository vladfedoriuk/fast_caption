# *FAST CAPTION*
The API for a selected image captioning model.


### Development

- Add a `PyCharm` [plugin](https://plugins.jetbrains.com/plugin/12861-pydantic) to enable a better autocompletion.
- Configure a virtual environment. The projects runs with `Python 3.8.12`. An example of a virtual environment created
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

- To  better manage the package versions and their dependencies consistency,
the project employs `pip-tools`.

* requirements compilation:
```
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
- The project uses `git pre-commit hooks` for a better development experience. To install the hooks run:
```commandline
pre-commit install
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
  - Setting up tests:
      - [DB setup](https://graspingtech.com/docker-compose-postgresql/)
      - [fastapi docs](https://fastapi.tiangolo.com/advanced/async-tests/)
      - [sync connection and session](https://www.mybluelinux.com/database-integration-tests-with-pytest-sqlalchemy-and-factory-boy-with-faker/)
      - [another sync setup](https://itnext.io/setting-up-transactional-tests-with-pytest-and-sqlalchemy-b2d726347629)
      - [async conection and session](https://rogulski.it/blog/fastapi-async-db/)
      - [the one used in the project](https://rogulski.it/blog/sqlalchemy-14-async-orm-with-fastapi/)
  - Tutorials:
    - https://testdriven.io/blog/topics/fastapi/
    - https://towardsdatascience.com/build-an-async-python-service-with-fastapi-sqlalchemy-196d8792fa08
    - https://stribny.name/blog/fastapi-asyncalchemy/
- Run the development server as follows:
```commandline
uvicorn main:app --reload
```
