# Realtime Blacklist (RBL) Checker

This docker container regularly checks one or multiple email servers against a number of RBL blacklists in a customizable interval. If one of the specified server is listed on one or more blacklists, it sends a notification via Apprise.

## Features

- Supports IPv4 and IPv6
- Notifications via Apprise whenever a new listing is found or an existing one is removed
- Runs inside a docker container, which is fully configurable by environment variables
- Optional integration of healthchecks.io
  
## Usage

The container can be configured using environment variables. These are:

| Variable              | Mandatory/Optional | Usage |
| --------------------- | ------------------ | ----- |
| RBL_HOSTS             | Mandatory          | The hosts to monitor, given either as IP-Address or as FQDN. Multiple hosts have to be comma-separated. If a FQDN is provided, all available IPv4 and IPv6 addresses will be checked |
| RBL_APPRISE_URL       | Mandatory          | A string representing the notification endpoint. Format according to the [Apprise Documentation](https://github.com/caronc/apprise) |
| RBL_INTERVAL          | Optional           | The interval in which the blacklists should be checked, given in minutes. Default: 60 |
| RBL_HEALTHCHECK_URL   | Optional           | This URL is fetched (GET-request) after each execution to indicate, that the service was executed. This may be used in conjunction with e.g. [healthchecks.io](https://healthchecks.io). This is skipped, if the variable is not set |

## Run as a docker container

This container can be run with the following docker command:

```sh
docker run -d --name rbl-checker -e RBL_HOSTS=mail.example.com,mail.example.org -e RBL_APPRISE_URL=pover://abc@xyz sbonfert/rbl-checker
```

## docker-compose example configuration

```yaml
rbl-checker:
    image: sbonfert/rbl-checker:latest
    restart: always
    container_name: rbl-checker
    environment:
      - RBL_HOSTS=mail.example.com,mail.example.org
      - RBL_APPRISE_URL=pover://abc@xyz
```
