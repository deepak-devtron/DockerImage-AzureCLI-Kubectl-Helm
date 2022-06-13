FROM alpine:latest as build
MAINTAINER Deepak Panwar <erdipak.panwar@gmail.com>
ARG HELM_LATEST_VERSION=v3.8.2
WORKDIR /
RUN apk add --update --no-cache ca-certificates git curl tar gzip unzip

# Installing Helm3
RUN curl -LO "https://get.helm.sh/helm-${HELM_LATEST_VERSION}-linux-amd64.tar.gz"
RUN tar -xzvf helm-${HELM_LATEST_VERSION}-linux-amd64.tar.gz

# Installing kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
RUN chmod +x kubectl

FROM ubuntu:20.04
#COPY az-cluster-create.py .
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3 && apt-get install -y python3-pip
RUN apt-get install -y ca-certificates curl apt-transport-https lsb-release gnupg
RUN pip3 install azure-cli
COPY --from=build /linux-amd64/helm /usr/local/bin/helm
COPY --from=build /kubectl /usr/local/bin/kubectl


