FROM mhart/alpine-node:6
MAINTAINER Dimitrije Radojević <templaryum@gmail.com>

RUN apk update && apk upgrade && apk add git \
 && git clone -b v0.8.0 https://github.com/etsy/statsd.git /opt/statsd
ADD conf/opt/statsd/config.js /opt/statsd/

EXPOSE 8125/udp

ENTRYPOINT ["node", "/opt/statsd/stats.js", "/opt/statsd/config.js"]
