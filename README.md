# Hack-a-Sat 3 Qualifier

This repository contains the open source release for the Hack-a-Sat 3
qualifier from 2022.

Released artifacts include:

* Source code for all challenges
* Source code for all challenge solutions
* Infrastructure to build all challenges and their solutions
* Notes on how to build and solve challenges

Released artifacts *do not* include:

* Infrastructure used to host and run the game
* Source code for the score board
* Source code for the "ticket taker" or "lifecycle manager" (used to host
  randomized challenges within the live game infrastructure)
* Source code for the "sat solver" (used to test challenges before deployment)


## Repository Structure ##

The infrastructure for Hack-a-Sat 2022 deployed challenges from self-contained
[Docker](https://www.docker.com/) images. Each challenge has an internal
name that is used to refer to that challenge's containers. These names are not
necessarily the same as the name that was used on the scoreboard. Folders
within this repository are named according to each challenge's internal name,
rather than its external one.

The following is a mapping of all names by category:

| Category | Challenge Name | Short Name |
| ------ | ------ | -- |
|The Danger Room|Juggernaut|basic-file|
|The Danger Room|Magneto|basic_service|
|The Danger Room|Prof. X|basic_handoff|
|Crypto Category Placeholder Name|Black Hole|black_hole|
|Crypto Category Placeholder Name|Leggo My Steggo!|leggo|
|Crypto Category Placeholder Name|Screaming Fist|screaming_fist|
|Crypto Category Placeholder Name|Welcome to the Spiderverse|spiderverse|
|I Can Haz Satellite|F'DA Approved Beef|fda_approved_beef|
|I Can Haz Satellite|Fun in the Sun|sunfun|
|I Can Haz Satellite|Red Alert|red_alert|
|Revenge of the Space Math|(Don't) Fly Me to the Moon|fly_me_to_the_moon |
|Revenge of the Space Math|Crosslinks|crosslinks1|
|Revenge of the Space Math|Matters of State|matters_of_state|
|Revenge of the Space Math|Navigation Rebooting|crosslinks2|
|Rocinante Strikes Back|Once Unop a Djikstar|djikstar|
|Rocinante Strikes Back|Stars Above|starsabove|
|Rocinante Strikes Back|The Authenticator Equivalence Principle|authentication_equivalence_principle|
|Rocinante Strikes Back|The Wrath of Khan|khan|
|The Only Good Bug is a Dead Bug|Bit Flipper|bitflipper|
|The Only Good Bug is a Dead Bug|Blazin' Etudes|blazin_etudes|
|The Only Good Bug is a Dead Bug|It's A Wrap|its_a_wrap|
|The Only Good Bug is a Dead Bug|Ominous Etude|ominous_etude|
|The Only Good Bug is a Dead Bug|Small Hashes Anyways|small_hashes_anyways|
|We Get Signal|Doppler|doppler|
|We Get Signal|Power Level|power_level|
|We Get Signal|Power Point|power_point|
|We Get Signal|Space Jam|space_jam|

The `generator-base` folder is included to build the base image for all
challenges that use a generator (see below).


## Building and Deploying Challenges ##

For instructions on how to build each challenge's Docker images, please refer
to each folder's `README.md`. Each challenge may have up to 3 separate images:

* `generator` - Used to generate any static files necessary to give to teams.
* `challenge` - Used to host the actual challenge on the game infrastructure.
* `solver` - Used to ensure the challenge would be solvable for a given team.

### Missing Infrastructure ###

This repository does not contain the `ticket-taker`, `lifecycle-manager`, or
`sat-solver` programs (or their source code).

During the live Hack-a-Sat 3 qualifier, challenges were deployed with a
program called `ticket-taker`. This program would take a supplied ticket and
use it to generate a seed value and flag specific to that ticket. It would then
launch an instance of the challenge container, passing any options necessary
via environment variables.

Using `ticket-taker` posed a problem for certain challenges: External tools we
expected players to use, like Google Maps, don't understand "tickets". A
second program called `lifecycle-manager` was used for these challenges.
`ticket-taker` would launch an instance of `lifecycle-manager` to "manage" the
connection between the player and the challenge after the player authenticated
with their ticket.

The commands below are from our internal test tool (called `sat-solver`), that
was capable of testing the solver against a specific seed in a managed
environment without `ticket-taker` or `lifecycle-manager`. These commands
should be sufficient for anyone using this repository to quickly host
challenges locally for testing.

[This file](tickets_export_2022_06_27.csv) can
be used as a "decoder ring" for turning tickets from the live event into seed
values that allow you to run the same copy of the challenge your team got in
the 2022 qualifier.

#### Microblaze User Toolchain

Three challenges, 
`small_hashes_anyways`, `ominous_etude`, and `blazing_etudes`,
depend on a `microblaze-user-toolchain` docker image.
The Dockerfile and script to generate that image are in the 
`microblaze-user-toolchain` directory.

For the source tarballs it depends on, read the `build_cross_gcc`
script for URLs.

### Generators ###

These were run in a job queue prior to the release of a challenge to generate
the unique status files for each team's challenge seed:

```sh
docker run -t --rm -v <dir>:/out -e SEED=<seed> -e FLAG=<flag> <container>:generator
```

* `dir` is the output directory on the host where you want generated files
  to be stored.
* `seed` is the random seed you want files to be generated for.
* `flag` is the flag you expect the team to submit to the scoreboard.
* `container` is the internal name of the challenge (see above).

Generators were typically built off of the `generator-base` Docker image. As a
result, you'll need to build the image in the `generator-base` folder before
building any generator images.

### Challenges ###

These were run on hardened AWS VMs that were provisioned by a central
[Puppet](https://puppet.com/) Master. Every VM only hosted a single challenge.
Multiple VMs were used with a round-robin DNS loadbalancer to spread connections
across all VMs provisioned for that challenge.

Puppet would install [`xinetd`](https://en.wikipedia.org/wiki/Xinetd), which
would open up a single port for incoming connections for `ticket-taker`.
`ticket-taker` would be responsible for executing one of the commands below
based on a configuration file after the player's ticket was verified:

```sh
# use this if the challenge only needs basic options
docker run --rm -i -e SEED=<seed> -e FLAG=<flag> <container>:challenge

# use this if the challenge needs generated files to run
docker run --rm -i -e DIR=/mnt -v <dir>:/mnt -e SEED=<seed> -e FLAG=<flag> <container>:challenge

# use this if the challenge is required to have its connections managed
docker run --rm -i -e SERVICE_HOST=<host> -e SERVICE_PORT=<port> -e SEED=<seed> -e FLAG=<flag> <container>:challenge

# use this if the challenge needs both generated files and a managed connection
docker run --rm -i -e DIR=/mnt -v <dir>:/mnt -e SERVICE_HOST=<host> -e SERVICE_PORT=<port> -e SEED=<seed> -e FLAG=<flag> <container>:challenge
```

* `seed` is the random seed to use when running the challenge.
* `flag` is the flag you expect the team to submit to the scoreboard.
* `container` is the internal name of the challenge (see above).
* `host` is the IP or address of the host this container is running on.
* `port` is the additional port the challenge should open.
* `dir` is the directory on the host where generated files are stored.

To re-host these challenges *without* `xinetd`, you can use `socat` like so:

```sh
# remember to escape any colons (":") in the commands above with backslashes!
socat -v tcp-listen:<port>,reuseaddr "exec:<command from above>"
```

### Solvers ###

These were run in batches on a server with tons of cores to ensure every team
would be able to solve their randomized version of each challenge. They were
also run any time a team wanted verification that a challenge was working as
intended during the live game.

```sh
# use this if the solver only needs basic options
docker run -it --rm -e HOST=<host> -e PORT=<port> <container>:solver

# use this if the solver needs generated files to run
docker run -it --rm -e HOST=<host> -e PORT=<port> -e DIR=/mnt -v <dir>:/mnt <container>:solver

# use this if you want to solve with a specific ticket
docker run -it --rm -e HOST=<host> -e PORT=<port> -e TICKET=<ticket> <container>:solver

# use this if you want to solve with a specific ticket and need generated files
docker run -it --rm -e HOST=<host> -e PORT=<port> -e DIR=/mnt -v <dir>:/mnt -e TICKET=<ticket> <container>:solver
```

* `seed` is the random seed of the challenge you're trying to solve.
* `ticket` is the ticket for your team.
* `container` is the internal name of the challenge (see above).
* `host` is the IP or address of the challenge host.
* `port` is the port on the challenge host for this challenge.
* `dir` is the directory on the host where generated files are stored.

It should be noted that these solvers implement *a* solution for their
challenge, not *the* solution. Many challenges had alternative ways of solving
them (some easier, some harder) that were not tested by (and, in some cases, not
intended by) the organizers.


## License ##

Challenges in this repository are provided as-is under the MIT license.
See [LICENSE.md](LICENSE.md) for more details.


## Contact ##

Questions, comments, or concerns can be sent to `hackasat[at]cromulence.com`.
