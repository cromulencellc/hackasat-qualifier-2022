# Quals Challenge: Basic Service #

This is our sample service for Hack-a-Sat, repackaged as an actual challenge.
We decided to include it in the actual game to give new players something to
test their assumptions on before actually getting to the real challenges.


## Building ##

This repository contains two Docker images: The `challenge` and the `solver`.
You can build both with:

```sh
make build
```

The resulting Docker images will be tagged as `basic-service:challenge` and
`basic-service:solver`.

You can also build just one of them with `make challenge` or `make solver`
respectively.

