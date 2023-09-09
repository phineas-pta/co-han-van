# using multi-stage: 2 build steps auto run in parallel

###############################################################################
# super lightweight webserver

FROM ubuntu:latest AS serverbuilder

WORKDIR /home

# assembler to binary
RUN apt update &&\
    apt install -y git make yasm as31 nasm binutils &&\
    git clone --depth=1 https://github.com/nemasu/asmttpd.git &&\
    cd asmttpd &&\
    make release

###############################################################################
# nodejs build

FROM node:latest AS pagebuilder

WORKDIR /home

# install deps (docker cache)
COPY package.json .
RUN npm install

# build
COPY . .
RUN npx sass --no-source-map assets &&\
    npx @11ty/eleventy --pathprefix='//'
# hack to overwrite path to root

###############################################################################
# run

FROM scratch

LABEL name="Cổ Hán Văn"
LABEL description="collection of some classical chinese texts"
LABEL author="PTA"

COPY --from=serverbuilder /home/asmttpd/asmttpd /
COPY --from=pagebuilder /home/_site /web_root
# default dir name of asmttpd

# any port of choice, here python default port
EXPOSE 8000

CMD ["/asmttpd", "/web_root", "8000"]
