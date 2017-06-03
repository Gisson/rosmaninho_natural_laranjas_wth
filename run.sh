#!/bin/bash

if [[ -z "$GITHUB_API_TOKEN" ]];then
	echo "Token not set. please export GITHUB_API_TOKEN with your token"
	echo "Continue?(press Ctrl+c to exit)"
 	read
fi	

python3 src/server.py
