# Realtime Blacklist (RBL) Checker

This docker container regularly checks one or multiple email servers against a number of RBL blacklists in a customizable interval. If one of the specified server is listed on one or more blacklists, it sends a pushover notification.

## Usage

The container can be configured using environment variables. These are:

| Variable              | Mandatory/Optional | Usage |
| --------------------- | ------------------ | ----- |
| RBL_HOSTS             | Mandatory          | The hosts to monitor, given either as IP-Address or as FQDN. Multiple hosts have to be comma-separated |
| RBL_PUSHOVER_TOKEN    | Mandatory          | Your pushover application token. May be aquired [here](https://pushover.net/apps/build) |
| RBL_PUSHOVER_USER_KEY | Mandatory          | Your pushover user key |
| RBL_INTERVAL          | Optional           | The interval in which the blacklists should be checked, given in minutes. Default: 60 |
| RBL_HEALTHCHECK_URL   | Optional           | This URL is fetched (GET-request) after each execution to indicate, that the service was executed. This may be used in conjunction with e.g. [healthchecks.io](https://healthchecks.io). This is skipped, if the variable is not set |

## Run as a docker container

This container can be run with the following docker command:

```sh
docker run -d --name rbl-checker -e RBL_HOSTS=mail.example.com,mail.example.org -e RBL_PUSHOVER_TOKEN=xyz -e RBL_PUSHOVER_USER_KEY=abc sbonfert/rbl-checker
```

## docker-compose example configuration

```yaml
rbl-checker:
    image: sbonfert/rbl-checker:latest
    restart: always
    container_name: rbl-checker
    environment:
      - RBL_HOSTS=mail.example.com,mail.example.org
      - RBL_PUSHOVER_TOKEN=xyz
      - RBL_PUSHOVER_USER_KEY=abc
```
