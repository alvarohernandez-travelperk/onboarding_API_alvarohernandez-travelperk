# recipe-app-api

Backend for the recipe app created by Alvaro Hernandez as a part of the onboarding exercise.

- branch recipe-endpoints

- Docker required to run it locally.

### `docker-compose build`

Builds the container.

### `docker-compose up`

Runs the container.

### `docker-compose run --rm app sh -c "python manage.py test"`

Runs the tests.

### `docker-compose run --rm app sh -c "flake8"`

Runs the linter.

### `http://127.0.0.1:8000/api/docs/`

By default, the API documentation.
