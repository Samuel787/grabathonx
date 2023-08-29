import datetime
import numpy as np
import os
import os.path as osp
import glob
import cv2
import insightface
from insightface.app import FaceAnalysis
from insightface.data import get_image as ins_get_image
import sys
from PIL import Image

def process_image():
    print("Hi there, processing image")

def merge_input_images(image_one_path, image_two_path, output_image_path):
    images_list = [image_one_path, image_two_path]

    images = [Image.open(x) for x in images_list]
    widths, heights = zip(*(i.size for i in images))

    total_width = sum(widths)
    max_height = max(heights)

    new_im = Image.new("RGB", (total_width, max_height))

    x_offset = 0

    for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

    new_im.save(output_image_path)

def insight_one_into_two(merged_image_name, swapped_image_path):
    app = FaceAnalysis(name="buffalo_l")
    app.prepare(ctx_id=0, det_size=(640, 640)) # check what these numbers mean
    swapper = insightface.model_zoo.get_model("inswapper_128.onnx", download=False, download_zip=False)

    img = ins_get_image(merged_image_name)
    faces = app.get(img)
    faces = sorted(faces, key = lambda x : x.bbox[0])

    source_face = faces[0]
    res = img.copy()
    for face in faces:
        res = swapper.get(res, face, source_face, paste_back=True)
    cv2.imwrite(swapped_image_path, res)
