import json
import os
import urllib.request
from io import BytesIO

import openai
from PIL import Image
from dotenv import load_dotenv

import utils.b64image
import utils.fileutils
import utils.limit_utils

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def gpt_create_image(description: str, num: int, size: str):
    # 限制接口请求次数
    utils.limit_utils.check_limit()
    # 请求openai的图片接口
    if size not in ["256x256", "512x512", "1024x1024"]:
        raise Exception("图片尺寸仅支持 256x256, 512x512, 1024x1024")
    created_image = openai.Image.create(prompt=description, n=num, size=size, response_format="b64_json")
    # json_obj = json.loads(str(created_image))
    # b64_data = json_obj["data"][0]["b64_json"]
    # image_url = utils.b64image.b64_to_image(b64_data)
    # image_data = {"image_url": image_url}
    # json_data = json.dumps(image_data)
    return created_image


# TODO: fix: openai.error.InvalidRequestError: Uploaded image must be a PNG and less than 4 MB.
#            TypeError: a bytes-like object is required, not 'PngImageFile'
def gpt_edit_image(image_path, description, num, mask_path):
    if utils.fileutils.get_file_size(image_path) > 4.0 * 1024 * 1024:
        raise Exception("图片大小应小于4MB")
    file = BytesIO(urllib.request.urlopen(image_path).read())
    image = Image.open(file).tobytes()
    width, height = utils.fileutils.get_image_size(image_path)
    if mask_path is not None:
        if utils.fileutils.get_file_size(mask_path) > 4.0 * 1024 * 1024:
            raise Exception("图片大小应小于4MB")
        else:
            mask_file = BytesIO(urllib.request.urlopen(mask_path).read())
            if Image.open(file).size != Image.open(mask_file).size:
                raise Exception("待修改图片大小应与参照图片大小一致")
    image_edit = openai.Image.create_edit(
        image=image,
        mask=None,
        prompt=description,
        n=num,
        size=f"{width}x{height}",
        response_format="b64_json"
    )
    json_obj = json.loads(str(image_edit))
    b64_data = json_obj["data"][0]["b64_json"]
    image_url = utils.b64image.b64_to_image(b64_data)
    return image_url
