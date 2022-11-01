Title: Using a Private Module in Go - Part 1, natively
Author: Pascal Bauermeister
Category: Programming
Tags: Golang, shell, Git, DevOps
Date: 2022-10-30
Summary: How to use a Go module that is hosted in a private Git repo?

# TL;DR

To use a private Go repo (say
`github.com/pbauermeister/golang-example-private-module`), have SSH access to the repo, and, before building, do:

- `export GOPRIVATE=github.com/pbauermeister`
- `git config --global url."git@github.com:".insteadOf "https://github.com/"`

This is the 1st post of the series "Using a Private Module in Go". In
[part 2](using-a-private-module-in-go-part-2-with-docker.html) we will
extend the solution to Docker containers.

# Background

## Context

Mostly, Go modules are hosted on public repositories. You import a
module (e.g. `yaml`) by having in your Go source file:

```golang
import "gopkg.in/yaml.v3"
```

and run:

```bash
go get gopkg.in/yaml.v3
```

When, for some reasons, you are to use a module that is hosted on a
private repo, things become a bit more complex. Read on.

## Sample private module

In this post, we are supposing we want to use a private module hosted
at `github.com/pbauermeister/golang-example-private-module` and
described by its `go.mod` file:

```golang
module github.com/pbauermeister/golang-example-private-module/v2

go 1.18
```

and containing this single source file, `example.go`:

```golang
package example_package

import "fmt"

func ExampleFunc(value int) {
        fmt.Println("The value is", value)
}
```

## Your code

Let us assume your `main.go` file looks like this:

```golang
package main

import lib "github.com/pbauermeister/golang-example-private-module/v2"

func main() {
        lib.ExampleFunc(42)
}
```

When running your program, you expect the output to be `The value is 42`.

## The issue

The command `go get ...` will yield an error, like in this session:

```
$ go get github.com/pbauermeister/golang-example-private-module/v2
go: module github.com/pbauermeister/golang-example-private-module:
git ls-remote -q origin in /home/pascal/go/pkg/mod/cache/vcs/e542c...: exit status 128:
	ERROR: Repository not found.
	fatal: Could not read from remote repository.

	Please make sure you have the correct access rights
	and the repository exists.
```

As we are sure that the repository exists, it must be an access rights
issue, which is not a surprise because the repo is private.

# Solution

Assuming the Git URL to be
`github.com/pbauermeister/golang-example-private-module`...

## Step 1 - Check you have SSH access to the repo

1. Check that you have your SSH keys pair:

    - `~/.ssh/id_rsa`
    - `~/.ssh/id_rsa.pub`

      If not, then create a key pair: `ssh-keygen -b 4096 -C "INSERT
      YOUR E-MAIL ADDRESS HERE"`.

2. Display your public key: `cat ~/.ssh/id_rsa.pub` and copy it.

3. Ensure your SSH public key is authorized by the repo:

     - if you own the repo, add the (above copied) key to your
       settings (look for access SSH keys),
     - or, depending on the hosting: ask the owner of the repo to
       authorize your SSH key, or add you as collaborator, or add you
       to the organization/project.

## Step 2 - Call the necessary commands

The needed commands are, for the given repo:

- `export GOPRIVATE=github.com/pbauermeister`
- `git config --global url."git@github.com:".insteadOf "https://github.com/"`

then, build as usual.

## Step 3 - Pack commands into a script

To automate the step 2, include the commands in whatever build script
you are using for your project.

For instance, `build.sh`:

```bash
#!/bin/sh
set -ex

export GOPRIVATE=github.com/pbauermeister
git config --global url."git@github.com:".insteadOf "https://github.com/"
go get github.com/pbauermeister/golang-example-private-module/v2
go build -o main main.go
```

Now the build does not complain, and you can run the result, as in
this sample session:

```
$ ./build.sh
+ export GOPRIVATE=github.com/pbauermeister
+ git config --global url.git@github.com:.insteadOf https://github.com/
+ go get github.com/pbauermeister/golang-example-private-module/v2
+ go build -o main main.go

$ ./main
The value is 42
```

# That's it!

Thanks for reading.

In [part 2](using-a-private-module-in-go-part-2-with-docker.html) we
will extend the solution to Docker containers.