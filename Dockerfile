FROM python:3.12.2-alpine3.19

RUN apk update \
    && apk add --no-cache wireguard-tools-wg-quick iptables dnsmasq curl openrc
RUN mkdir /etc/wireguard
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt && rm /requirements.txt
RUN echo "net.ipv4.ip_forward=1" > /etc/sysctl.d/10-custom-rules.conf
RUN echo -e "server=8.8.8.8\nserver=1.1.1.1" >> /etc/dnsmasq.conf

WORKDIR /app
COPY ./src/ /app/src/
COPY ./start.sh /app/start.sh
