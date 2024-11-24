# simulazoo

Simulateur de zoo

## install

```shell
pipenv shell
pip install -r ./requirements.txt
```

## Usage

### Classic CLI

This CLI allow you to make call and simulation from the command line

```shell
 python -m simulazoo -h
```

### Interactive prompt

This CLI is an interactive prompte. Suitable for Human, but not so much for automatisation.

```shell
 python -m simulazoo.prompt
```

## Docker image

### Build

```shell
docker build -t simulazoo .
```

### Usage

The docker image use the Interactive prompt by default

```shell
docker run -it --rm simulazoo
```

## Run Test

```shell
python -m pytest
```