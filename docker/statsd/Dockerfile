FROM arm32v7/node:6-slim
MAINTAINER Dimitrije Radojević <templaryum@gmail.com>

RUN apt-get update && apt-get -y upgrade && apt-get -y install git \
 && git clone -b v0.8.0 https://github.com/etsy/statsd.git /opt/statsd
ADD conf/opt/statsd/config.js /opt/statsd/

EXPOSE 8125/udp

ENTRYPOINT ["node", "/opt/statsd/stats.js", "/opt/statsd/config.js"]
