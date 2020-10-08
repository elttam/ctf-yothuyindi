# Overview

**Title:** yothuyindi  
**Category:** Web  
**Flag:** libctf{it's a short song but it's a hell of a story}  
**Difficulty:** easy to moderate

# Usage

The following will pull the latest 'elttam/ctf-yothuyindi' image from DockerHub, run a new container named 'libctfso-yothuyindi', and publish the vulnerable service on port 80:

```sh
docker run --rm \
  --read-only \
  --tmpfs /tmp:size=4k \
  --publish 8080:8080 \
  --name libctfso-yothuyindi \
  elttam/ctf-yothuyindi:latest
```

# Build (Optional)

If you prefer to build the 'elttam/ctf-yothuyindi' image yourself you can do so first with:

```sh
docker build ${PWD} \
  --tag elttam/ctf-yothuyindi:latest
```
