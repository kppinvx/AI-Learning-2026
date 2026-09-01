## Install the required packages
sudo apt update
sudo apt install python3-full python3-venv

## Create a python virtual environment
python3 -m venv venv

## Copy Environment variables
cp .env.example .env

## Activate it
source venv/bin/activate

## To deactivate
deactivate

## Upgrade pip
pip install --upgrade pip

## Install the packages
pip install langchain langchain-google-genai langchain-groq langchain-mistralai python-dotenv
