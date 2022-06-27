# Quals Challenge: Power Point #

**Category:** RF
**Relative Difficulty:** 4/5
**Author:** [Cromulence](https://cromulence.com/)

Break out Microsoft Office because its time to make some slides..... just kidding! 

There is a satellite out there transmitting a flag. You are on a moving platform and you dont know how you will be moving or where the transmitter is or how the transmitter is moving. Luckily you have a steerable antenna! To get the flag:

1. Find the transmitter by steering the antenna.
1. Keep the antenna pointed at the transmitter and try to maximize signal power.
1. Decode the samples coming in from your receiver.

Your co-worker told you they think the satellites is "North-ish and sort of close to the horizon"

- Send az, el commands to the antenna using TCP/IP over port. A antenna command is formatted as a string...to send az=77.1 el=73.2
```
77.10,22.2\n
```
Please send one command at a time
- After you send a command the receiver will reply with a fixed number of IQ samples via TCP


