#!/bin/bash


#activate the  admin rights for user 
 Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
    
# Install the required packages
pip install accelerate
pip install -i https://pypi.org/simple/ bitsandbytes

# Verify installation
pip list | grep -E 'accelerate|bitsandbytes'

# Update transformers library (optional but recommended)
pip install --upgrade transformers

# Clear Streamlit cache (optional)
streamlit cache clear

# Restart Streamlit app
streamlit run ./src/app.py
