#!/bin/sh

docker build -t web_frontend:local $(dirname "${0}")
