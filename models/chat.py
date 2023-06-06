import os

import openai
from dotenv import load_dotenv
from revChatGPT.V1 import AsyncChatbot

import utils.json_utils
import utils.limit_utils

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def chat(creative: float, content: str):
    # 限制接口请求次数
    utils.limit_utils.check_limit()
    # 请求openai的chat接口
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                              messages=[
                                                  # Change the prompt parameter to the messages parameter
                                                  {'role': 'user', 'content': content}
                                              ],
                                              # 0~2,default 1, 0:precision; 1:balance; 2:creative
                                              temperature=creative,
                                              stop=None)
    return completion
    # return chat_completion['choices'][0]['message']['content']


def chat_completion(message: list):
    # 限制接口请求次数
    utils.limit_utils.check_limit()
    # 请求openai的连续对话接口
    if type(message) != list:
        raise Exception('输入内容应如下格式:\neg:[{"role": "system", "content": "You are a helpful assistant."},\n{"role": '
                        '"user", "content": "Who won the world series in 2020?"},\n{"role": "assistant", "content": '
                        '"The Los Angeles Dodgers won the World Series in 2020."},\n{"role": "user", "content": '
                        '"Where was it played?"}]')
    for roles in message:
        if roles['role'] not in {"system", "user", "assistant"}:
            raise Exception('输入角色仅支持"system","user","assistant"')
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                        messages=message,
                                        stop=None)
    return chat


def use_chat_completion(message: str):
    # 限制接口请求次数
    utils.limit_utils.check_limit()
    message_list: list = utils.json_utils.create_user_chat_message_list(message)
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                        messages=message_list,
                                        stop=None)
    return chat


async def chat_ask(token, model, prompt) -> str:
    chatbot = AsyncChatbot(config={
        "access_token": token
    })
    response = ""
    async for d in chatbot.ask(prompt=prompt, model=model):
        response = d["message"]
    return response


async def chat_conversation(token) -> str:
    chatbot = AsyncChatbot(config={
        "access_token": token
    })
    data = await chatbot.get_conversations()
    return data


async def chat_msg_history(token, convo_id) -> str:
    chatbot = AsyncChatbot(config={
        "access_token": token
    })
    data = await chatbot.get_msg_history(convo_id)
    return data


# TODO:fix：无法测通，入参运行报错
async def chat_gen_title(token, convo_id, message_id) -> str:
    chatbot = AsyncChatbot(config={
        "access_token": token
    })
    data = await chatbot.gen_title(convo_id, message_id)
    return data


async def chat_change_title(token, convo_id, title) -> str:
    chatbot = AsyncChatbot(config={
        "access_token": token
    })
    data = await chatbot.change_title(convo_id, title)
    return data


async def chat_delete_conversation(token, convo_id) -> str:
    chatbot = AsyncChatbot(config={
        "access_token": token
    })
    data = await chatbot.delete_conversation(convo_id)
    return data


async def chat_clear_conversations(token) -> str:
    chatbot = AsyncChatbot(config={
        "access_token": token
    })
    data = await chatbot.clear_conversations()
    return data
