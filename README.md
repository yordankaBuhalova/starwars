# Star Wars Explorer

This is a simple app which allows you to collect, resolve and inspect information about characters
in the Star Wars universe from the [SWAPI](https://pipedream.com/apps/swapi).

The entry endpoint for data retrieval is: `https://swapi.co/api/people/`

## Env-Requirements:

* Django>= 4.0
* psycopg2-binary>=2.9.1
* petl >= 1.7.12
* requests >= 2.28.2

## Setup

* Clone the repo

    ```
    git clone https://github.com/yordankaBuhalova/starwars.git
    ```

* [Install Docker](https://docs.docker.com/engine/install/)

* Open terminal in "starwars" file directory:

    * Build the Docker Image:

        ```
        docker-compose build
        ```

    * Start the Docker container:

        ```
        docker-compose up
        ```

* Access under [http://localhost:8000](http://localhost:8000/)

* Stop the Docker container:

    ```
    docker-compose down
    ```

## Lint

Bash:
```bash
docker run -v $(pwd)/code:/tmp/lint docker.io/oxsecurity/megalinter:latest
```

Powershell:
```
docker run -v <ABS_PATH_HERE>/code:/tmp/lint docker.io/oxsecurity/megalinter:latest
```
