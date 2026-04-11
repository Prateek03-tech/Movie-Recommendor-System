#!/bin/sh

# Create Streamlit config directory
mkdir -p ~/.streamlit/

# Create config file
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml