DISCLAIMER: Following library is for educational purposes only
reCall is an telecom software that executes recurring persistant calling of a target's phone number

The application uses Freeclimb API for maintaining an IVR that runs SIP connections to phones over an internet connection

Steps to run locally:

1. Run ```ngrok http 3001 ```
2. Register freeclimbe app at www.freeclimb.com and copy credentials to .env file
2. Set environmental variables and run ```src .env```
3. Run ```pip3 install -r requirements.txt ```
4. Run ```Run python3 app.py```


env variables:

ACCOUNT_ID='[FREECLIMB_ACCOUNT_ID]'
API_KEY='[FREECLIMB_API_KEY]'
APP_ID='[FREECLIMB_APP_ID]'
SRC_URL='[ngrok_host]'
export FC_NUMBER='[FREEECLIMB_NUMBER]'
export FC_URL='https://www.freeclimb.com/apiserver'