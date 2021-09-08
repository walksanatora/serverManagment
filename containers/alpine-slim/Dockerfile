FROM        alpine:latest

LABEL       author="Walksanator" maintainer="walkerffo11@gmail.com"

RUN         apk add --no-cache --update ca-certificates tree \
            && mkdir /mnt/data

WORKDIR     /mnt/data

COPY        ./entrypoint.sh /entrypoint.sh
CMD         ["/bin/ash", "/entrypoint.sh"]