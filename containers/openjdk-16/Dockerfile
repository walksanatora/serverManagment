FROM        openjdk:16-slim

LABEL       author="Walksanator" maintainer="walkerffo11@gmail.com"

RUN         apt-get update &&  apt-get install ca-certificates tree -y \
            && mkdir /mnt/data

WORKDIR     /mnt/data

COPY        ./entrypoint.sh /entrypoint.sh
CMD         ["/bin/sh", "/entrypoint.sh"]