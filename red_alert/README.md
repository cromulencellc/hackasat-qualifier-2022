# Quals Challenge: Red Alert #

**Category:** I can haz satellite
**Relative Difficulty:** 3/5
**Author:** [Cromulence](https://cromulence.com/)

Someone is junking up our orbits again.
We've upgraded the space lasers from HAS2 to the new Femptosecond Laser Automated Gun system. Now you dont need to tell the lasers where to fire, you just need to activate the debris detection system and the lasers will automatically shoot down debris. Careful though, the debris detector and the lasers use a lot of power and generate a lot of heat!

You can access the ground station's Grafana dashboard on port XXXX

Grafana has access to the API through our internal network. Available commands:
```
http://groundstation:5000/laser-on
http://groundstation:5000/laser-off
http://groundstation:5000/detector-on
http://groundstation:5000/detector-off
```


# How to build 

This challenge uses sysbox to encapsulate docker compose and several containers and needs to be built in multiple steps.
To create the docker images you need to run the 'generate' command. This will create the docker image from scratch each time. This seperation from running the challenge is a result of using docker-in-docker

First sysbox must be installed on your computer:

```
install sysbox
```


```
make generate
```

After you have generated the challenge container you can run it at any time with 

```
make challenge
```
# Running the challenge locally

The challenge can be run locally **without** sysbox. 

To do this run the following:

```
make local
```
