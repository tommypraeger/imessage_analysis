#!/bin/bash

(trap 'kill 0' SIGINT; (python3 application.py) & (npm start --prefix ./ui))
