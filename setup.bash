#!/bin/bash

if ! command -v virtualenv &>/dev/null; then
    echo "virtualenv is not installed, install with:"
    echo "  pip3 install --user virtualenv"
    exit 1
fi

if [ ! -f ".venv/bin/activate" ]; then
    echo "No virtual environment found, creating in .venv..."
    virtualenv .venv
fi

echo "Sourcing virtual environmnet..."
source .venv/bin/activate

echo "Installing dependencies..."
pip3 install -r requirements.txt

echo "Virtual environmnet ready!"
