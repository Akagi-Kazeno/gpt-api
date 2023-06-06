import asyncio
import os
from datetime import timedelta

import openai
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

import models.chat
import models.completions
import models.image
import utils.db_utils
import utils.log_utils
import utils.session_utils

load_dotenv()
app = Flask(__name__)
cors = CORS(app)
app.secret_key = os.getenv("SECRET_KEY")
openai.api_key = os.getenv("OPENAI_API_KEY")
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
        json_data = models.chat.chat(creative, content)
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
        json_data = models.chat.chat_completion(message)
        utils.db_utils.chat_db_commit(json_data)
        utils.db_utils.user_chat_completion_to_db(message)
        return json_data


@app.route('/chat/completion', methods=("GET", "POST"))
def chat_completion():
    create_session_id()
    if request.method == "POST":
        data = request.get_json()
        message = data["message"]
        json_data = models.chat.use_chat_completion(message)
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
    create_session_id()
    if request.method == 'POST':
        data = request.get_json()
        token = data.get('token')
        model = data.get('model')
        prompt = data.get('prompt')
        response = asyncio.run(models.chat.chat_ask(token, model, prompt))
        return jsonify({'response': response})


@app.route('/api/chat/conversation', methods=['POST'])
def chat_conversation():
    create_session_id()
    if request.method == 'POST':
        data = request.get_json()
        token = data.get('token')
        response = asyncio.run(models.chat.chat_conversation(token))
        return jsonify({'response': response})


@app.route('/api/chat/msg/history', methods=['POST'])
def chat_msg_history():
    create_session_id()
    if request.method == 'POST':
        data = request.get_json()
        token = data.get('token')
        convo_id = data.get('convo_id')
        response = asyncio.run(models.chat.chat_msg_history(token, convo_id))
        return jsonify({'response': response})


@app.route('/api/chat/gen/title', methods=['POST'])
def chat_gen_title():
    create_session_id()
    if request.method == 'POST':
        data = request.get_json()
        token = data.get('token')
        convo_id = data.get('convo_id')
        message_id = data.get('message_id')
        response = asyncio.run(models.chat.chat_gen_title(token, convo_id, message_id))
        return jsonify({'response': response})


@app.route('/api/chat/change/title', methods=['POST'])
def chat_change_title():
    create_session_id()
    if request.method == 'POST':
        data = request.get_json()
        token = data.get('token')
        convo_id = data.get('convo_id')
        title = data.get('title')
        response = asyncio.run(models.chat.chat_change_title(token, convo_id, title))
        return jsonify({'response': response})


@app.route('/api/chat/delete/conversation', methods=['POST'])
def chat_delete_conversation():
    create_session_id()
    if request.method == 'POST':
        data = request.get_json()
        token = data.get('token')
        convo_id = data.get('convo_id')
        response = asyncio.run(models.chat.chat_delete_conversation(token, convo_id))
        return jsonify({'response': response})


@app.route('/api/chat/clear/conversations', methods=['POST'])
def chat_clear_conversations():
    create_session_id()
    if request.method == 'POST':
        data = request.get_json()
        token = data.get('token')
        response = asyncio.run(models.chat.chat_clear_conversations(token))
        return jsonify({'response': response})


if __name__ == '__main__':
    app.run(host=os.getenv("HOST"), port=os.getenv("PORT"))
