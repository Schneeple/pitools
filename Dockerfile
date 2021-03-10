ARG BASE_CONTAINER=jupyter/tensorflow-notebook
ARG JUPYTER_ENABLE_LAB=yes
FROM $BASE_CONTAINER

LABEL maintainer="Colton Neary <schneeple@outlook.com>"

# USER root

ENV JUPYTER_ENABLE_LAB=$JUPYTER_ENABLE_LAB

COPY . /opt/conda/lib/pitools

EXPOSE 8888



