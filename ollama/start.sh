#!/bin/bash

ollama serve &
sleep 10
ollama pull qwen2.5-coder:7b
wait