import requests
import os

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

if __name__ == "__main__":
    url = "https://cdn.discordapp.com/attachments/1143545161914273917/1146266982853902366/timshim_thomas_the_train_3973ceb4-300f-4cc1-91f0-bc76fda99e94.png"
    save_folder = "upload"
    image_name ="test123.jpg"
    download_and_save_image(url, save_folder, image_name)