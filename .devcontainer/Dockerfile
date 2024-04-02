FROM python:3.12.2-alpine3.19

RUN apk update \
    && apk add --no-cache wireguard-tools-wg-quick iptables dnsmasq curl
RUN mkdir /etc/wireguard
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt && rm /requirements.txt
RUN echo "net.ipv4.ip_forward=1" >> /etc/sysctl.d/10-custom-rules.conf