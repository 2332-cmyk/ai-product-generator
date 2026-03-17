#!/bin/bash
# Make sure PORT is set (Render sets it automatically)
export PORT=${PORT:-7860}

# Run Gradio app
python app.py
