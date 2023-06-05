import os
import urllib.request
from io import BytesIO

from PIL import Image
from dotenv import load_dotenv

load_dotenv()


def get_file_size(filepath):
    """
    获取文件大小
    :param filepath:
    :return:
    """
    file = BytesIO(urllib.request.urlopen(filepath).read())
    img = Image.open(file)
    file_size = len(img.fp.read())
    return file_size


def get_image_size(img_path):
    """
    获取图片大小
    :param img_path:
    :return:
    """
    file = BytesIO(urllib.request.urlopen(img_path).read())
    img = Image.open(file)
    width, height = img.size
    return width, height


def image_mode_check(img_path):
    """
    检查图片模式并转换
    :param img_path:
    :return:
    """
    image = Image.open(img_path)
    if image.mode not in ["RGBA", "L", "LA"]:
        file, ext = os.path.splitext(img_path)
        filename = os.path.basename(file)
        new_name = filename + "_rebuild"
        rgba_image = image.convert("RGBA")
        img_url = os.getenv("IMAGE_PATH") + new_name + ".png"
        with open(img_url, "wb") as f:
            f.write(rgba_image.tobytes())
        image_path = img_url.split(".", 1)[1]
        img_url = os.getenv("BASE_URL") + image_path
        return img_url
    else:
        file, ext = os.path.splitext(img_path)
        filename = os.path.basename(file)
        img_url = os.getenv("IMAGE_PATH") + filename + ".png"
        with open(img_url, "wb") as f:
            f.write(image.tobytes())
        image_path = img_url.split(".", 1)[1]
        img_url = os.getenv("BASE_URL") + image_path
        return img_url
