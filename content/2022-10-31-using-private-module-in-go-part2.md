Title: Using a Private Module in Go - Part 2, with Docker
Author: Pascal Bauermeister
Category: Programming
Tags: Golang, shell, Git, DevOps
Date: 2022-10-31
Summary: In a Dockerfile, how to use a Go module that is hosted in a private Git repo?

# TL;DR

In the Dockerfile:  
`RUN --mount=type=secret,id=ID_RSA ...`

In the container:  
`cat /run/secrets/ID_RSA | base64 -d > ~/.ssh/id_rsa`  
`ssh-keyscan -H github.com >> ~/.ssh/known_hosts`  
then, same as in Part 1

Building the container:  
`ID_RSA=$(cat ~/.ssh/id_rsa | base64 -w0)`  
`DOCKER_BUILDKIT=1 docker build --secret id=ID_RSA,src=<(set +x; echo $ID_RSA) ...`

# Summary

This is the 2nd post of the series "Using a Private Module in Go". In
the [part 1][1] we have seen how to do it natively.

In the present post, we will learn how to do it in Docker. I advise to
read the [part 1][1] first. The additional work with Docker is about
allowing SSH access to the repo, from within Docker.

# Concept

Like in [part 1][1], we assume that we (the native user) have SSH
access to the private Git repo.

We will use the `docker build --secret` option to copy our private SSH
key into the container, so that the container can access the private
repo as well.

# Solution

Docker version 20.10 or above is needed.

## Step 1 - The Dockerfile

Let us create this `Dockerfile`:
```
# Build stage
FROM golang:1.18rc1-bullseye as BUILD

WORKDIR /app
COPY *.go go.* build-app.sh ./
RUN --mount=type=secret,id=ID_RSA ./build-app.sh

# Final stage
FROM debian:11-slim

WORKDIR /app
COPY --from=BUILD /app/main .
CMD ./main
```

- In the build stage, in line 6, `--mount=type=secret,id=ID_RSA`
  mandates that the file `/run/secrets/ID_RSA`, inside the container,
  holds our secret, during the execution of `build-app.sh`.

- As its name indicates, `build-app.sh` is caring for the most part of
  the work.

## Step 2 - `build-app.sh`

The script `build-app.sh` runs in the build stage of the Dockerfile,
and essentially does what we have seen in [part 1][1], plus some
preparation work.

`build-app.sh`:

```bash
#!/bin/sh
set -ex

if [ ! -f /run/secrets/ID_RSA ]; then
    echo >&2 "Error: /run/secrets/ID_RSA is not available"
    exit 1
fi

# Prepare to access the repo via SSH
mkdir ~/.ssh
cat /run/secrets/ID_RSA | base64 -d > ~/.ssh/id_rsa
chmod og-rw ~/.ssh/id_rsa

ssh-keyscan -H github.com >> ~/.ssh/known_hosts

# Get module and build
export GOPRIVATE=github.com/pbauermeister
git config --global url."git@github.com:".insteadOf "https://github.com/"
go get github.com/pbauermeister/golang-example-private-module/v2
go build -o main main.go

# Cleanup
rm -rf ~/.ssh
```

- Lines 4 to 7: we check that the secret file `/run/secrets/ID_RSA`
  (as instructed by `RUN --mount=type=secret,id=ID_RSA` in Step 1)
  exists.

- Lines 10 to 12: we create the `~/.ssh/id_rsa` file, which is the
  private SSH key allowing us to access the private Git repo.

    - Line 11: we use `/run/secrets/ID_RSA` to create the file
      `~/.ssh/id_rsa`. The content of `ID_RSA` is base-64 encoded, so
      we use `base64 -d` to decode it.

- Line 14: we declare the Git server as a known host, so that we will
  not be prompted to validate it at line 21.

- Lines 17 to 20: like in the [part 1][1].

- Line 23: we remove the SSH private key, so that it does not remain
  in the image layer.

## Step 3 - Building the image

Time to build the image! The following build script includes the
handling of the secret.

`build-image.sh`:

```bash
#!/bin/bash
set -e
ID_RSA=$(cat ~/.ssh/id_rsa | base64 -w0)
set -x

DOCKER_BUILDKIT=1 docker build \
       --no-cache \
       --secret id=ID_RSA,src=<(set +x; echo $ID_RSA) \
       --tag golang-example-use-private-repo .
```

- Line 3: our ssh private key is read, packed as base64, and put into
  the variable `ID_RSA`.

- Line 6: `DOCKER_BUILDKIT=1` mandates to enable the BuildKit,
  required for `RUN --mount=type=secret`.

- Line 8:

    - `--secret id=ID_RSA,src=` mandates to put the secret to be
       available into the container, but not stored into the image.
    - `<(set +x; echo $ID_RSA)` creates a temporary file containing
      the value of `ID_RSA` created at line 3, and passes the tempory
      path to `src=`.

Sample session of running the build script:
```bash
$ ./build-image.sh
+ DOCKER_BUILDKIT=1
+ docker build --no-cache --secret id=ID_RSA,src=/dev/fd/63                --tag golang-example-use-private-repo .
++ set +x
[+] Building 7.0s (13/13) FINISHED
 => [internal] load build definition from Dockerfile                    0.0s
 => => transferring dockerfile: 38B                                     0.0s
 => [internal] load .dockerignore                                       0.0s
 => => transferring context: 2B                                         0.0s
 => [internal] load metadata for docker.io/library/debian:11-slim       1.2s
 => [internal] load metadata for docker.io/library/golang:1.18rc1-bull  0.0s
 => [build 1/4] FROM docker.io/library/golang:1.18rc1-bullseye          0.0s
 => [internal] load build context                                       0.0s
 => => transferring context: 112B                                       0.0s
 => [stage-1 1/3] FROM docker.io/library/debian:11-slim@sha256:e8ad0bc  0.0s
 => CACHED [stage-1 2/3] WORKDIR /app                                   0.0s
 => CACHED [build 2/4] WORKDIR /app                                     0.0s
 => [build 3/4] COPY *.go go.* build-app.sh ./                          0.0s
 => [build 4/4] RUN --mount=type=secret,id=ID_RSA ./build-app.sh        5.6s
 => [stage-1 3/3] COPY --from=BUILD /app/main .                         0.0s
 => exporting to image                                                  0.0s
 => => exporting layers                                                 0.0s
 => => writing image sha256:ee330b6cfd0692514de2f16851a1fb10185238266e  0.0s
 => => naming to docker.io/library/golang-example-use-private-repo      0.0s
```

## Step 4 - Running the image

Sample session of running the image:
```bash
$ docker run golang-example-use-private-repo
The value is 42
```

It works!

## Optional - Get the private module natively

If you develop with an IDE, or compile natively before building the
container, you will need to get the private module. Here is a handy
script for this.

`go-get-private-repo-natively.sh`:

```bash
#!/bin/sh
set -ex

export GOPRIVATE=github.com/pbauermeister
go get github.com/pbauermeister/golang-example-private-module/v2
```


# That's it!

Thanks for reading.

[1]: using-a-private-module-in-go-part-1-natively.html
