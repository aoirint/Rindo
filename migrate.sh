#!/bin/bash
sudo docker-compose run app alembic revision --autogenerate $1
