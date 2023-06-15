import asyncio
import os
from datetime import timedelta

import openai
from dotenv import load_dotenv
from flask import Flask, request, jsonify, session
from flask_cors import CORS

import models.completions
import models.gpt_chat
import models.image
import models.web_chat
import utils.db_utils
import utils.log_utils
import utils.session_utils

load_dotenv()
app = Flask(__name__)
cors = CORS(app)
app.secret_key = os.getenv("SECRET_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_ACCESS_TOKEN: str = os.getenv("OPENAI_ACCESS_TOKEN")
app.permanent_session_lifetime = timedelta(days=float(os.getenv("SESSION_LIFETIME")))


@app.before_request
def new_log():
    """
    请求前创建log
    :return:
    """
    utils.log_utils.create_log("app.log")


@app.before_request
def create_session_id():
    """
    请求前创建session_id
    :return:
    """
    utils.session_utils.create_session_id()


@app.route('/chat', methods=("GET", "POST"))
def create_chat():
    """
    创建chat请求
    :return:
    """
    create_session_id()
    if request.method == "POST":
        data = request.get_json()
        creative = data["creative"]
        content = data["content"]
        json_data = models.gpt_chat.chat(creative, content)
        utils.db_utils.chat_db_commit(json_data)
        utils.db_utils.user_chat_db_commit(content)
        return json_data


@app.route('/chat/completions', methods=("GET", "POST"))
def completions_chat():
    """
    创建连续对话请求
    :return:
    """
    create_session_id()
    if request.method == "POST":
        data = request.get_json()
        message = data["message"]
        json_data = models.gpt_chat.chat_completion(message)
        utils.db_utils.chat_db_commit(json_data)
        utils.db_utils.user_chat_completion_to_db(message)
        return json_data


@app.route('/chat/completion', methods=("GET", "POST"))
def chat_completion():
    create_session_id()
    if request.method == "POST":
        data = request.get_json()
        message = data["message"]
        json_data = models.gpt_chat.use_chat_completion(message)
        utils.db_utils.chat_db_commit(json_data)
        utils.db_utils.user_chat_completion_to_db(message)
        return json_data


@app.route('/completion', methods=("GET", "POST"))
def create_completions():
    """
    创建completions请求
    :return:
    """
    create_session_id()
    if request.method == "POST":
        data = request.get_json()
        creative = data["creative"]
        prompt = data["prompt"]
        json_data = models.completions.completions(creative, prompt)
        utils.db_utils.completion_db_commit(json_data)
        utils.db_utils.user_completion_db_commit(prompt)
        return json_data


@app.route('/image/gpt', methods=("GET", "POST"))
def create_image():
    """
    创建生成图片请求
    :return:
    """
    create_session_id()
    if request.method == "POST":
        data = request.get_json()
        description = data["description"]
        num = data["num"]
        size = data["size"]
        json_data = models.image.gpt_create_image(description, num, size)
        utils.db_utils.gpt_image_db_commit(json_data)
        utils.db_utils.user_gpt_image_db_commit(description)
        return json_data


@app.route('/image/edit/gpt', methods=("GET", "POST"))
def edit_image():
    create_session_id()
    if request.method == "POST":
        data = request.get_json()
        image_path = data["imagePath"]
        description = data["description"]
        num = data["num"]
        mask_path = data["maskPath"]
        return models.image.gpt_edit_image(image_path, description, num, mask_path)


@app.route('/api/chat/ask', methods=['POST'])
def chat_ask():
    """
    询问
    """
    if request.method == 'POST':
        data = request.get_json()
        access_token = OPENAI_ACCESS_TOKEN
        model = data.get('model')
        prompt = data.get('prompt')
        parent_id = data.get('parent_id')
        convo_id = data.get('convo_id')
        try:
            utils.db_utils.user_web_chat_to_db(prompt)
        except:
            raise Exception
        response = asyncio.run(
            models.web_chat.chat_ask(access_token, convo_id=convo_id, model=model, prompt=prompt, parent_id=parent_id))
        print(response)
        # 将回复数据插入数据库
        utils.db_utils.web_chat_res_to_db(response)
        return jsonify({'response': response})

@app.route('/api/chat/continue_write', methods=['POST'])
def chat_continue_write():
    """
    询问
    """
    if request.method == 'POST':
        data = request.get_json()
        access_token = OPENAI_ACCESS_TOKEN
        model = data.get('model')
        parent_id = data.get('parent_id')
        convo_id = data.get('convo_id')
        response = asyncio.run(
            models.web_chat.continue_write(access_token, convo_id=convo_id, model=model,parent_id=parent_id))
        print(response)
        # 将回复数据插入数据库
        utils.db_utils.web_chat_res_to_db(response)
        return jsonify({'response': response})


@app.route('/api/chat/conversation', methods=['POST'])
def chat_conversation():
    """
    获取 conversation
    """
    create_session_id()
    if request.method == 'POST':
        access_token = OPENAI_ACCESS_TOKEN
        response = asyncio.run(models.web_chat.chat_conversation(access_token))
        return jsonify({'response': response})


@app.route('/api/chat/msg/history', methods=['POST'])
def chat_msg_history():
    """
    根据id获取历史信息
    """
    create_session_id()
    if request.method == 'POST':
        data = request.get_json()
        access_token = OPENAI_ACCESS_TOKEN
        convo_id = data.get('convo_id')
        response = asyncio.run(models.web_chat.chat_msg_history(access_token, convo_id))
        return jsonify({'response': response})


@app.route('/api/chat/gen/title', methods=['POST'])
def chat_gen_title():
    create_session_id()
    if request.method == 'POST':
        data = request.get_json()
        access_token = OPENAI_ACCESS_TOKEN
        convo_id = data.get('convo_id')
        message_id = data.get('message_id')
        response = asyncio.run(models.web_chat.chat_gen_title(access_token, convo_id, message_id))
        return jsonify({'response': response})


@app.route('/api/chat/change/title', methods=['POST'])
def chat_change_title():
    """
    修改 conversation 的标题
    """
    create_session_id()
    if request.method == 'POST':
        data = request.get_json()
        access_token = OPENAI_ACCESS_TOKEN
        convo_id = data.get('convo_id')
        title = data.get('title')
        response = asyncio.run(models.web_chat.chat_change_title(access_token, convo_id, title))
        return jsonify({'response': response})


@app.route('/api/chat/delete/conversation', methods=['POST'])
def chat_delete_conversation():
    """
    删除 conversation
    """
    create_session_id()
    if request.method == 'POST':
        data = request.get_json()
        access_token = OPENAI_ACCESS_TOKEN
        convo_id = data.get('convo_id')
        response = asyncio.run(models.web_chat.chat_delete_conversation(access_token, convo_id))
        return jsonify({'response': response})


@app.route('/api/chat/clear/conversations', methods=['POST'])
def chat_clear_conversations():
    """
    清除所有 conversation
    """
    create_session_id()
    if request.method == 'POST':
        access_token = OPENAI_ACCESS_TOKEN
        response = asyncio.run(models.web_chat.chat_clear_conversations(access_token))
        return jsonify({'response': response})


if __name__ == '__main__':
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT"))
