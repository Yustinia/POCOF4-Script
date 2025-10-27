FROM archlinux:latest

RUN pacman -Syyu --noconfirm

RUN pacman -S --needed --noconfirm python python-pip vim

WORKDIR /HOSPorter

COPY . /HOSPorter/

CMD [ "bash" ]
