# first build Alpine Base Image with Init
FROM alpine:3.12
RUN apk add --no-cache bash tzdata python3 py3-requests

# Image Description
LABEL version="1.0" description="Script to query all possible codes from SMA Inverter WebConnect Interface and translate them into readable description with actual values."

# Python Script to Container
COPY ./WebConnectCodes.py /WebConnectCodes.py

ENTRYPOINT ["/usr/bin/python3", "/WebConnectCodes.py"]
