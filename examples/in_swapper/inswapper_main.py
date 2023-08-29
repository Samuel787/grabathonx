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


assert insightface.__version__>='0.7'

# image_one_path = "/Users/samuel.sutherdavid/Desktop/samuel/plusgst/insightface/myenv/lib/python3.9/site-packages/insightface/data/images/t10.jpg"
# image_two_path = "/Users/samuel.sutherdavid/Desktop/samuel/plusgst/insightface/myenv/lib/python3.9/site-packages/insightface/data/images/t20.jpg"

# def merge_input_images():
#     # image_one_path = "/Users/samuel.sutherdavid/Desktop/samuel/plusgst/insightface/myenv/lib/python3.9/site-packages/insightface/data/images/t10.jpg"
#     # image_two_path = "/Users/samuel.sutherdavid/Desktop/samuel/plusgst/insightface/myenv/lib/python3.9/site-packages/insightface/data/images/t20.jpg"
#     images_list = [image_one_path, image_two_path]

#     images = [Image.open(x) for x in images_list]
#     widths, heights = zip(*(i.size for i in images))

#     total_width = sum(widths)
#     max_height = max(heights)

#     new_im = Image.new("RGB", (total_width, max_height))

#     x_offset = 0

#     for im in images:
#         new_im.paste(im, (x_offset, 0))
#         x_offset += im.size[0]

#     new_im.save("t10t20.jpg")


# def insight_one_into_two():
#     app = FaceAnalysis(name="buffalo_l")
#     app.prepare(ctx_id=0, det_size=(640, 640)) # check what these numbers mean
#     swapper = insightface.model_zoo.get_model("inswapper_128.onnx", download=False, download_zip=False)

#     img = ins_get_image("t10t20")
#     faces = app.get(img)
#     faces = sorted(faces, key = lambda x : x.bbox[0])

#     source_face = faces[0]
#     res = img.copy()
#     for face in faces:
#         res = swapper.get(res, face, source_face, paste_back=True)
#     cv2.imwrite("./t10t20swapped.jpg", res)

# def cut_out_second_image():
#     im1 = Image.open(image_one_path)
#     im2 = Image.open(image_two_path)

#     horizontal_offset = im1.size[0] # from left
#     vertical_offset = im2.size[1] # from bottom

#     swapped_img = Image.open("/Users/samuel.sutherdavid/Desktop/samuel/plusgst/insightface/examples/in_swapper/t10t20swapped.jpg")
#     total_width = swapped_img.size[0]
#     final_img = swapped_img.crop((horizontal_offset + 1, 0, total_width, vertical_offset))
#     final_img.save("./t10t20swapped_final.jpg")

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

def cut_out_second_image(image_one_path, image_two_path, swapped_path, final_path):
    im1 = Image.open(image_one_path)
    im2 = Image.open(image_two_path)

    horizontal_offset = im1.size[0] # from left
    vertical_offset = im2.size[1] # from bottom

    swapped_img = Image.open(swapped_path)
    total_width = swapped_img.size[0]
    final_img = swapped_img.crop((horizontal_offset + 1, 0, total_width, vertical_offset))
    final_img.save(final_path)

if __name__ == '__main__':

    '''
    Experimentation section
    '''

    # merge_input_images()

    # insight_one_into_two()

    # cut_out_second_image()

    '''
    app = FaceAnalysis(name='buffalo_l')
    app.prepare(ctx_id=0, det_size=(640, 640))
    # swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=True, download_zip=True)
    swapper = insightface.model_zoo.get_model('inswapper_128.onnx', download=False, download_zip=False)

    img = ins_get_image('t1')
    faces = app.get(img)
    faces = sorted(faces, key = lambda x : x.bbox[0])
    assert len(faces)==6
    source_face = faces[2]
    res = img.copy()
    for face in faces:
        res = swapper.get(res, face, source_face, paste_back=True)
    cv2.imwrite("./t1_swapped.jpg", res)
    res = []
    for face in faces:
        _img, _ = swapper.get(img, face, source_face, paste_back=False)
        res.append(_img)
    res = np.concatenate(res, axis=1)
    cv2.imwrite("./t1_swapped2.jpg", res)
    '''