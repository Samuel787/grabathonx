from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from examples.in_swapper.inswapper_main import (
    merge_input_images,
    insight_one_into_two,
    cut_out_second_image
)
import requests
import json
from urllib.parse import parse_qs
import random
import time
import urllib.request
from fastapi.staticfiles import StaticFiles
import threading

APP_BASE_URL = "https://bb7e-202-73-59-34.ngrok-free.app"
GIORGY_API_ENDPOINT = "https://next-fast-midjourney.vercel.app/api/imagine"

app = FastAPI()
app.mount("/upload", StaticFiles(directory="upload"), name="upload")
random.seed(int(time.time()))

# Allow Cross-Origin Resource Sharing (CORS)
origins = ["*"]  # You can restrict origins for security purposes
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

# Temporary directory to store uploaded files
UPLOAD_DIR = "upload" # "myenv/lib/python3.9/site-packages/insightface/data/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def send_message_to_slack_bot(message, slack_webhook_url):
    custom_headers = {
        "Content-Type": "application/json",
    }
    data = {
       "text": message,
       "response_type": "in_channel"
    }
    try:
        print(f"sending to slack bot: {data}")
        response = requests.post(slack_webhook_url, headers=custom_headers, json=data)
        print(f"sent to slack bot successfully")
    except Exception as e:
        print(f"Something went wrong when sending message back to slack bot: {str(e)}")

@app.get("/")
async def server():
    return {"status": "up and running"}

@app.post("/insight")
async def insight(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        # Save uploaded images to the temporary directory
        file1_path = os.path.join(UPLOAD_DIR, file1.filename)
        file2_path = os.path.join(UPLOAD_DIR, file2.filename)
        merged_file_path = os.path.join(UPLOAD_DIR, "mergedimage.jpg")
        swapped_file_path = os.path.join(UPLOAD_DIR, "swapped.jpg")
        final_file_path = os.path.join(UPLOAD_DIR, "final.jpg")

        with open(file1_path, "wb") as f1, open(file2_path, "wb") as f2:
            shutil.copyfileobj(file1.file, f1)
            shutil.copyfileobj(file2.file, f2)

        # You can now process the images or perform any other required operations
        print("processing image")

        merge_input_images(file1_path, file2_path, merged_file_path)
        insight_one_into_two("mergedimage", swapped_file_path)
        cut_out_second_image(file1_path, file2_path, swapped_file_path, final_file_path)
        
        return FileResponse(final_file_path, headers={"Content-Disposition": "attachment; filename=result.jpg"})
    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)

def download_image(image_url, file_path_to_save):
    urllib.request.urlretrieve(image_url, file_path_to_save)

def download_and_save_image(url, save_folder, image_name):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            image_path = os.path.join(save_folder, image_name)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Image saved as {image_path}")
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def process_images_and_send_back_slack(file_url_one, file_url_two, slack_webhook_url):
    try:
        file1_path = os.path.join(UPLOAD_DIR, "file1.jpg")
        file2_path = os.path.join(UPLOAD_DIR, "file2.jpg")
        print("two")
        # download these images from the url
        # download_image(file_url_one, file1_path)
        # download_image(file_url_two, file2_path)

        download_and_save_image(file_url_one, UPLOAD_DIR, "file1.jpg")
        download_and_save_image(file_url_two, UPLOAD_DIR, "file2.jpg")

        print("trhee")
        rand_number = random.randint(0,100000)
        merged_file_path = os.path.join(UPLOAD_DIR, "mergedimage.jpg")
        swapped_file_path = os.path.join(UPLOAD_DIR, "swapped.jpg")
        final_file_path = os.path.join(UPLOAD_DIR, str(rand_number) + ".jpg")
        print("four")
        merge_input_images(file1_path, file2_path, merged_file_path)
        insight_one_into_two("mergedimage", swapped_file_path)
        cut_out_second_image(file1_path, file2_path, swapped_file_path, final_file_path)
        print("five")

        final_image_location = APP_BASE_URL + "/upload/" +str(rand_number) + ".jpg"
        print("six")
        send_message_to_slack_bot(final_image_location, slack_webhook_url)
    except Exception as e:
        send_message_to_slack_bot("Something went wrong when generating the image with the ML model. Please try again...", slack_webhook_url)
        print(f"An exception occurred: {str(e)}")

@app.post("/insight_images")
async def insight_images(payload: dict):
    try:
        print(f"this is the payload: {payload}")
        print("one")
        file_url_one = payload.get("one")
        file_url_two = payload.get("two")
        slack_webhook_url = payload.get("webhookUrl")
        background_thread = threading.Thread(target=process_images_and_send_back_slack, args=(file_url_one, file_url_two, slack_webhook_url))
        background_thread.start()
        return JSONResponse(content={"message": "success"}, status_code=200)

        # file1_path = os.path.join(UPLOAD_DIR, "file1.jpg")
        # file2_path = os.path.join(UPLOAD_DIR, "file2.jpg")
        # print("two")
        # # download these images from the url
        # # download_image(file_url_one, file1_path)
        # # download_image(file_url_two, file2_path)

        # download_and_save_image(file_url_one, UPLOAD_DIR, "file1.jpg")
        # download_and_save_image(file_url_two, UPLOAD_DIR, "file2.jpg")

        # print("trhee")
        # rand_number = random.randint(0,100000)
        # merged_file_path = os.path.join(UPLOAD_DIR, "mergedimage.jpg")
        # swapped_file_path = os.path.join(UPLOAD_DIR, "swapped.jpg")
        # final_file_path = os.path.join(UPLOAD_DIR, str(rand_number) + ".jpg")
        # print("four")
        # merge_input_images(file1_path, file2_path, merged_file_path)
        # insight_one_into_two("mergedimage", swapped_file_path)
        # cut_out_second_image(file1_path, file2_path, swapped_file_path, final_file_path)
        # print("five")

        # final_image_location = APP_BASE_URL + "/upload/" +str(rand_number) + ".jpg"
        # print("six")
        # return JSONResponse(content={"message": final_image_location}, status_code=200)
    except Exception as e:
        print(f"This is the error: {str(e)}")
        return JSONResponse(content={"message": str(e)}, status_code=500)

# def send_message_to_slack_bot(message, slack_webhook_url):
#     custom_headers = {
#         "Content-Type": "application/json",
#     }
#     data = {
#        "text": message,
#        "response_type": "in_channel"
#     }
#     try:
#         response = requests.post(slack_webhook_url, headers=custom_headers, json=data)
#     except Exception as e:
#         print(f"Something went wrong when sending message back to slack bot: {str(e)}")

def call_giorgy_endpoint(giorgy_endpoint, data, slack_webhook_url):
    print("Calling giorgy endpoint")
    custom_headers = {
        "Content-Type": "application/json",
    }
    try:
        response = requests.post(giorgy_endpoint, headers=custom_headers, json=data)
        if response.status_code != 200:
            send_message_to_slack_bot("Something went wrong :( Please try again!", slack_webhook_url)
        else:
            send_message_to_slack_bot("Give me a few minutes to cook up something for you...", slack_webhook_url)
            print("Successfully called giorgy's API")
    except Exception as e:
        send_message_to_slack_bot("Something went wrong :( Please try again!", slack_webhook_url)

@app.post("/slack")
async def get_text_from_slack_payload(request: Request):
    request_body = await request.body()
    request_text = request_body.decode("utf-8")
    parsed_data = parse_qs(request_text)
    text_value = parsed_data.get("text", [""][0])[0].strip()
    
    reference_url = None
    print(f"This is the original text value: {text_value}")
    tokens = text_value.split(" ")
    if len(tokens) > 1 and tokens[-1].startswith("http"):
        reference_url = tokens[-1]
    webhook_url = parsed_data.get("response_url", [""][0])[0]

    if reference_url != None:
        text_value = text_value.replace(reference_url, "")
        text_value = text_value.strip()
    
    print(f"This is the text_value now: {text_value}")

    data = {
        "prompt": text_value,
        "webhookUrl": webhook_url
    }

    if reference_url != None:
        data["reference"] = reference_url

    custom_headers = {
        "Content-Type": "application/json",
    }

    print(f"This is the paylo ad to Giorgy's api: {data}")
    background_thread = threading.Thread(target=call_giorgy_endpoint, args=(GIORGY_API_ENDPOINT, data, webhook_url))
    background_thread.start()
    return JSONResponse(content={"text": "I got your request"}, status_code=200)
    # try:
    #     response = requests.post(GIORGY_API_ENDPOINT, headers=custom_headers, json=data)

    #     if response.status_code != 200:
    #         print(f"Something went wrong when calling Giorgy's endpoint. Status code: {response.status_code}")
    #         return JSONResponse(content={"text": "Something went wrong... Please try again later"}, status_code=200)
    #     return JSONResponse(content={"text": "Give me a few minutes to cook up something for you..."}, status_code=200)
    # except Exception as e:
    #     return JSONResponse(content={"text": "A server exception has occurred: " + str(e)}, status_code=500)