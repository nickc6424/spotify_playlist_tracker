# spotify_playlist_tracker

## Introduction
This is a demo project which queries a "Top X songs"-type playlist via the Spotify API, stores the data in a containerised data lake, and transforms the data within a database. The purpose is to enable analytics to be performed on the playlist using the entry, movement and exit of songs over time.


## What does it actually do?
There are 4 main steps to the pipeline:
1. Query the Spotify API of a specific playlist
2. Store the response in S3
3. Load the data into Postgres
4. Transform the data and insert it into a data model

Key settings are driven by the config file, and the Make utility is used to simplify setup and execution.


## Pre-requisites
- Python v3.10.6 (plus the "python3.10-venv" package)
- GNU Make v4.3
- Docker v20.10.22
- AWS CLI

Useful links for installing pre-requisites:
- https://docs.docker.com/engine/install/ubuntu/
- https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
- https://stackoverflow.com/questions/69503329/pip-is-not-working-for-python-3-10-on-ubuntu

You are also required to generate a one-time client ID and client secret on Spotify to authenticate the API calls. These credentials must then be copied into the config file.

Generation of these credentials can be done by creating an application here:
https://developer.spotify.com/dashboard/applications

