import requests
import time

'''
    Cron job script that periodically calls the api
'''

UPSCALE_START_URL = "https://next-fast-midjourney.vercel.app/api/upscale/start"
UPSCALE_CHECK_URL = "https://next-fast-midjourney.vercel.app/api/upscale/check"

def upscale_start():
    try:
        response = requests.get(UPSCALE_START_URL)
    except Exception as e:
        print(f"An exception occurred: {str(e)}")

def upscale_check():
    try:
        response = requests.get(UPSCALE_CHECK_URL)
    except Exception as e:
        print(f"An exception ocurred: {str(e)}")

def cron_job():
    while True:
        print("New cron job cycle starting")
        upscale_start()
        upscale_check()
        print("cron job work is done and going to sleep for 60 seconds")
        time.sleep(60)

if __name__ == "__main__":
    cron_job()


def send_message_to_slack_bot(message, slack_webhook_url):
    custom_headers = {
        "Content-Type": "application/json",
    }
    data = {
       "text": message,
       "response_type": "in_channel"
    }
    try:
        response = requests.post(slack_webhook_url, headers=custome_headers, json=data)
    except Exception as e:
        print(f"Something went wrong when sending message back to slack bot: {str(e)}")

def call_giorgy_endpoint(giorgy_endpoint, data, slack_webhook_url):
    custom_headers = {
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(giorgy_endpoint, headers=custom_headers, json=data)
        if response.status_code != 200:
            send_message_to_slack_bot("Something went wrong :( Please try again!", slack_webhook_url)
        else:
            send_message_to_slack_bot("Give me a few minutes to cook up something for you...", slack_webhook_url)
    except Exception as e:
        send_message_to_slack_bot("Something went wrong :( Please try again!", slack_webhook_url)