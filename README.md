# Music Discovery
Introducing a Music Discovery Web Application (API and user-friendly interface). The platform is enhanced with Google API integration for song detection.

## Prerequisites
1. Install [docker engine](https://docs.docker.com/engine/install/)
2. Install YTmusicapi library
   ```
    pip install ytmusicapi
    ```
3. Generate google account authentification and follow the steps
   ```
   cd /flask/gcp
   ytmusicapi oauth
   ```
4. Copy the UI from [this repository](https://github.com/glennprays/music-discovery-ui) into `./next` directory.

## Get started
### Docker
To start this project in docker:
1. Build the Docker Compose first
   ```
   docker compose build
   ```
2. Execute the Docker Compose useing 'up' command
   ```
   docker compose up
   ```
- Stopping Docker Compose
  ```
  docker compose down
  ```
