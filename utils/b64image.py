import base64
import os
import uuid

from dotenv import load_dotenv

load_dotenv()


def b64_to_image(b64image) -> str:
    """
    将base64转换为图片并保存
    :param b64image:
    :return:
    """
    image_data = base64.b64decode(b64image)
    new_uuid = str(uuid.uuid4())
    img_uuid = new_uuid.replace("-", "")
    image_url = os.getenv("IMAGE_PATH") + img_uuid + ".png"
    with open(image_url, "wb") as f:
        f.write(image_data)
    img_path = image_url.split('.', 1)[1]
    request_url = os.getenv("BASE_URL") + img_path
    return request_url


def image_to_b64(img_path):
    """
    将图片转换为base64并保存为文件
    :param img_path:
    :return:
    """
    with open(img_path, "rb") as f:
        b64_data = base64.b64encode(f.read())
        new_uuid = str(uuid.uuid4())
        file_uuid = new_uuid.replace("-", "")
        file_name = file_uuid + ".txt"
        file = open(file_name, "wt")
        file.write(str(b64_data, encoding="utf-8"))
        file.close()
    return file_name
