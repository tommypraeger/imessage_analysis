#!/bin/bash

source venv/bin/activate
(trap 'kill 0' SIGINT; (python3 application.py) & (npm start --prefix ./ui))
