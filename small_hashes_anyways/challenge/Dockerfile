FROM registry.mlb.cromulence.com/has3/quals/challenges/generator-base/generator-base AS generator-base

FROM registry.mlb.cromulence.com/has3/quals/microblaze-user-toolchain:bk-20220420

RUN apk add ruby

WORKDIR /generator
ADD . /generator/
COPY --from=generator-base /upload/ /upload

CMD ["/bin/bash", "-c", "ruby /generator/generate.rb | /upload/upload.sh"]