from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
from imageprocessing.image_processing import (
    process_image,
    merge_input_images,
)
from examples.in_swapper.inswapper_main import (
    insight_one_into_two_test,
    cut_out_second_image_test
)

app = FastAPI()

# Allow Cross-Origin Resource Sharing (CORS)
origins = ["*"]  # You can restrict origins for security purposes
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"])

# Temporary directory to store uploaded files
UPLOAD_DIR = "myenv/lib/python3.9/site-packages/insightface/data/images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
        process_image()

        merge_input_images(file1_path, file2_path, merged_file_path)
        insight_one_into_two_test(merged_file_path, swapped_file_path)
        cut_out_second_image_test(file1_path, file2_path, swapped_file_path, final_file_path)
        return JSONResponse(content={"message": "Images uploaded successfully"}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)
