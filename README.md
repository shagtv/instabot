# Instagram bot

A bot likes posts on Instagram

## Installation:

1 Init virtualenv:

~~~~
virtualenv --python=python3 env
~~~~

2 Activate virtualenv:

~~~~
source /env/bin/activate
~~~~

3 Download web driver:

Firefox:  https://github.com/mozilla/geckodriver/releases

Chrome: http://chromedriver.chromium.org/downloads


3 Add a geckodriver or chromedriver path to PATH:

~~~~
export PATH=$PATH:/path/to/geckodriver
~~~~

3 Install packages:

~~~~
pip install --requirement requirements.txt`

~~~~

6 Run a bot:

~~~~
python3 app.py
~~~~
