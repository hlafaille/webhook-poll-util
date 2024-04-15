FROM python:3.11-bookworm AS build
RUN apt-get update && apt-get install make gcc patchelf ccache -y
RUN mkdir /tmp/build
COPY . /tmp/build
WORKDIR /tmp/build
RUN pip install -r requirements.txt
RUN make

FROM python:3.11-bookworm
# copy the binary, symlink it to bin
RUN mkdir /opt/webhookpollutil
COPY --from=build /tmp/build/target/webhookpollutil /opt/webhookpollutil/webhookpollutil
RUN ln -s /opt/webhookpollutil/webhookpollutil /usr/local/bin/webhookpollutil

# setup the handlers directory
RUN mkdir -p /etc/webhookpollutil/handlers
RUN ln -s /etc/webhookpollutil/handlers /opt/webhookpollutil/handlers

WORKDIR /opt/webhookpollutil
CMD [ "webhookpollutil" ]