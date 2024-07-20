from typing import Optional
import fire
import os
import torch
import base64
from io import BytesIO

from avatar_generator import PixarAvatarGenerator
from image_utils import extract_image


from flask import Flask, request, jsonify
 
app = Flask(__name__)

def generate_avatar(
    image_base: str,
    num_avatars: int,
    crop: str = "center",
    generate_prompt_from_image: bool = False,
    device: Optional[str] = None,
):
    """Generates Pixar-style avatars of people based on an image.

    Args:
        url (str): URL of the image.
        num_avatars (int): Number of avatars to generate.
        crop (str, optional): How to crop the image. One of "center", "top", "bottom", or "none". Defaults to "center".
        generate_prompt_from_image (bool, optional): Whether to generate the prompt based on the image. Defaults to False.
        device (Optional[str], optional): Device to place the model on. Defaults to "cuda" if available, otherwise "cpu".
    """
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    image = extract_image(image_base, crop=crop)
    avatar_generator = PixarAvatarGenerator(
        generate_prompt_from_image=generate_prompt_from_image, device=device
    )

    # generate avatars
    if num_avatars == 1:
        avatars = [avatar_generator.generate_avatar(image)]
    else:
        avatars = avatar_generator.generate_multiple_avatars(
            image, num_avatars=num_avatars
        )

    avatar_base64_list = []
    for avatar in avatars:
        buffered = BytesIO()
        avatar.save(buffered, format="PNG")
        avatar_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
        avatar_base64_list.append(avatar_base64)

    return avatar_base64_list

@app.route('/post_endpoint', methods=['POST'])
def post_endpoint():
    # 获取POST请求的数据
    data = request.get_json()
    # 假设我们期望接收一个名为'name'的字段
    image_base = data.get('image_base')
    num_avatars = data.get('num_avatars')
    #crop = data.get('crop')
    #generate_prompt_from_image = data.get('generate_prompt_from_image')
    #device = data.get('device')
    
    # 处理数据，例如将数据保存到数据库中
    # imagelist= generate_avatar(
    #     image_base, num_avatars, crop, device, generate_prompt_from_image
    # )
    imagelist= generate_avatar(
        image_base, num_avatars,crop="center",generate_prompt_from_image=False
        ,device="cuda"
    )
     
    
    # 返回响应
    return imagelist
 
if __name__ == '__main__':
    app.run()
