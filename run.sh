#!/bin/bash

(trap 'kill 0' SIGINT; (venv/bin/python3 application.py) & (npm start --prefix ./ui))
