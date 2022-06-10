FROM alpine:latest as build
MAINTAINER Deepak Panwar <erdipak.panwar@gmail.com>
ARG HELM_LATEST_VERSION=v3.8.2
WORKDIR /
RUN apk add --update --no-cache ca-certificates git curl tar gzip unzip python3 py3-pip

# Installing Helm3
RUN curl -LO "https://get.helm.sh/helm-${HELM_LATEST_VERSION}-linux-amd64.tar.gz"
RUN tar -xzvf helm-${HELM_LATEST_VERSION}-linux-amd64.tar.gz

# Installing kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
RUN chmod +x kubectl

FROM alpine:latest
RUN apk add --update --no-cache ca-certificates python3 py3-pip
COPY --from=build /linux-amd64/helm /usr/local/bin/helm
COPY --from=build /kubectl /usr/local/bin/kubectl
RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash






