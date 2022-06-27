FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        pip \
        software-properties-common

RUN pip install --upgrade pip ;\
    pip install --no-cache-dir \
        skyfield \
        timeout

RUN add-apt-repository ppa:gnuradio/gnuradio-releases && \
    apt update && \
    apt install -y --no-install-recommends gnuradio

RUN volk_profile

WORKDIR /generator
COPY --from=generator-base /upload/ /upload
COPY make_challenge.sh pkt*.txt sat.tle path_effects.py doppler.py /generator/

CMD ["/bin/bash", "-c", "sh make_challenge.sh; echo \"/generator/sat_downlink_120ksps.iq\" | /upload/upload.sh"]
