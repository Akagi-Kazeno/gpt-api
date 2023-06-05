import os

import openai
from dotenv import load_dotenv
from revChatGPT.V1 import Chatbot, AsyncChatbot
import asyncio

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



convo_id = "1befe7a2-0dea-4287-b1b4-922cdf73a027"
message_id = "c4204ee8-c23a-40b5-bf6b-cec28172446a"
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ6b3V6aGFuZ2hhbzk4MDEwMUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci0zYXZIM0w1NElJaHEyckpaZXVWSmJVcFYifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTAzOTE0MzE4NDI5Mzk0ODk1MTMwIiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4NTAyOTM1MSwiZXhwIjoxNjg2MjM4OTUxLCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSJ9.QX898r-eCfLT0gdtXFIbrybbxAbtFCPNA-yeFjRmibLebemT2vLjXDCVwD44xqqOHSxsMY3yYVGc1spJw3926Lca1bwPEb8uwP_TKzKTXpNUi1qe1NkV_WGF4oYzDhn_rydlfTPleSAX1dMQsHAja9xhXdowwfViEvP2hv8X2sNbF7DsF2S-RAAehjr71X3mABneqRUNT1GMkDfH-0K4m8io1v_dsKe0Qjd9q5zQLK0jmZWjMUWQSUpyFAWtaijPcZiW8_1AtNYgrJajMsGZCLovU_8hDUOmt3bsiQnMRQlqOyUbIXK2JWFIFORB7Pcde9YT_Ez8MmgUbQ4sbpB3kw"

a = asyncio.run(chat_clear_conversations(token))

print(a)