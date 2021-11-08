# Python Challenge

## Connected Developers API

This project was born from a [Rviewer](https://go.rviewer.io/challenge-library/)
challenge. The goal was to create a REST API which would return whether two
_developers_ were fully connected or not. Given a pair of developer usernames, they
were considered connected if:

* They follow each other on Twitter.
* They have at least a Github organization in common.

_Note:_ Developers having the same username, both in Twitter and Github, are assumed
to be the same person.

## How it works?

The challenge required implementing a Python REST API with these 2 endpoints:

> #### Realtime Endpoint
> 
> ```bash
> GET /connected/realtime/dev1/dev2
> ```
> 
> This endpoint returns if two developers are connected and what GitHub organizations
> have they in common.
 
> #### Register Endpoint
> 
> ```bash
> GET /connected/register/dev1/dev2
> ```
> 
> This endpoint returns all the related information from the previous invocations to
> the real-time endpoint, including the date it was registered.

_Note:_ You could find the whole description of that API in the [OpenAPI description
file](/api.definition.yaml).

To accomplish this requirement, I have used [FastAPI](https://fastapi.tiangolo.com/) 
to handle routing, [pydantic](https://pydantic-docs.helpmanual.io/) for data 
validation, and [Tortoise](https://tortoise-orm.readthedocs.io/en/latest/index.html) 
to communicate with the database.

All structured with **domain-driven design** and **hexagonal architecture**.

## Design philosophy

One of the stated goals of the challenge, was to "create a **clean**,
**maintainable** and **well-designed** code".

I choose to combine **domain-driven design** and **hexagonal architecture** to
achieve this goal because they allow the project to be expanded in many ways.

For example, there could be several applications in the `apps` module. If we want to
add a <abbr title="Command-line interface">CLI</abbr> API, we can put it into the
`apps.api.cli` module. Or, if we want to create a back-office, we can split it into
`apps.backoffice.backend` and `apps.backoffice.frontend` modules.

Furthermore, **the business logic is decoupled from the application framework,** and
also from the libraries we use to communicate with the infrastructure.

<abbr title="Domain-Driven Design">DDD</abbr> allows us to separate the API logic
from the back-office logic (or from any application we want to add to the project).
It is now implemented with several modules with no dependencies on any other modules
except `shared` module. However, this loosely-coupled design would make easier to
move a part of the code to a separated microservice later on.

## Technical details

Most of my experience programming in Python is developing websites with Django.
However, my experience in PHP allowed me to learn about the architectures I mentioned
above. And using a microframework seemed easier for me in order to implement them.

Among the available microframeworks, I choose [FastAPI](https://fastapi.tiangolo.com/)
because it is easy to use, asynchronous, and generates documentation automatically.

_Note:_ You could find the automatic docs on the URLs [/docs](http://127.0.0.1:5000/docs)
and [/redoc](http://127.0.0.1:5000/redoc).

I choose [pydantic](https://pydantic-docs.helpmanual.io/) because its simplicity. It
allows data to be validated in many ways, while remaining simple.

I added [orjson](https://github.com/ijl/orjson) because it performs much better than
the standard JSON library. It does not add much to the end result, but each bean
helps to fill the barn.

I also added a dependency injector to make it easier to implement the dependency
inversion principle. I do not like this injector so much, but I had no time to find a
better alternative.

[Tortoise](https://tortoise-orm.readthedocs.io/en/latest/index.html) was the selected
ORM to connect to the database because it is also asynchronous and claims to have
good performance. Like pydantic, it makes extensive use of type hinting. And its
structure and query filters are based on Django, which I find very convenient.

Finally, the challenge authors expected the project to query the official
[Twitter](https://developer.twitter.com/en/docs) and
[Github](https://docs.github.com/en/rest) APIs. It was OK to use the existing client
libraries, but I have preferred to make two asynchronous clients using the
[httpx](https://www.python-httpx.org/) library. This allows some requests to be
parallelized and makes sense with my other choices.

## Local Deployment
 
To make it easier to run the API (and meet the challenge requirements), I have
prepared a Docker Compose file.

However, you need to first add an `.env` file to the root directory. That file must
contain the following entries:

- _DATABASE_URL:_ The database configuration in this form:
  
    `postgres://USERNAME:PASSWORD@HOST:PORT/DB_NAME?PARAM1=value&PARAM2=value`

- _GITHUB_LOGIN:_ The username you use for signing in to GitHub.

- _GITHUB_PERSONAL_ACCESS_TOKEN:_ The token you have generated to access the GitHub
    API.

    To generate a token, sign in to [GitHub](https://github.com/) and go to _Settings
    / Developer settings / Personal access tokens._

- _TWITTER_BEARER_TOKEN:_ An Access Token used in authentication that allows you to
    use the Twitter API.

    To generate a token, sign in [Twitter Developers](https://developer.twitter.com/en/portal/)
    and go to _Projects & Apps,_ create a project, then create an app on it, and
    generate a Bearer Token.

After doing this, you will be able to spin up the API and a database server. Just
place this inside the root folder:

```bash
docker-compose up
```

Also, you can run the API without the container, just place inside the root folder:

```bash
uvicorn apps.api.rest.main:app --port 5000
```

_Note:_ You could add `--reload` to tell [Uvicorn](https://www.uvicorn.org/) to
reload if the project code changes.

### End to end tests

To ensure that everything is working as expected, the challenge included an e2e test
suite. Those tests are created with [Cypress](https://www.cypress.io/) and are based 
on the OpenAPI specification file.

To execute them, just place inside `e2e-test` folder:

```bash
npm install
npm run e2e
```

### Unit tests

I have also added some unit tests created with [pytest](https://docs.pytest.org/en/latest/).

To execute all them, just place inside the root folder:

```bash
pytest tests
```
