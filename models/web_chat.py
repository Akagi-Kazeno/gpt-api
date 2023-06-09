from revChatGPT.V1 import AsyncChatbot
import asyncio

async def chat_ask(access_token: str, convo_id: str | None, parent_id: str, model: str, prompt: str) -> dict:
    """
    询问
    """
    chatbot = AsyncChatbot(config={
        "access_token": access_token
    })
    response = {}
    async for response_dict in chatbot.ask(prompt=prompt, model=model, conversation_id=convo_id, parent_id=parent_id):
        response = response_dict
    return response

# a = asyncio.run(chat_ask("eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJ6b3V6aGFuZ2hhbzk4MDEwMUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZX0sImh0dHBzOi8vYXBpLm9wZW5haS5jb20vYXV0aCI6eyJ1c2VyX2lkIjoidXNlci0zYXZIM0w1NElJaHEyckpaZXVWSmJVcFYifSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTAzOTE0MzE4NDI5Mzk0ODk1MTMwIiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY4NjI4MTg3MSwiZXhwIjoxNjg3NDkxNDcxLCJhenAiOiJUZEpJY2JlMTZXb1RIdE45NW55eXdoNUU0eU9vNkl0RyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgbW9kZWwucmVhZCBtb2RlbC5yZXF1ZXN0IG9yZ2FuaXphdGlvbi5yZWFkIG9yZ2FuaXphdGlvbi53cml0ZSJ9.CEPpNR8Uq2dodf0WYPGSe5ggJqj1YCylLQJ6xRHgqMUI6t0X8m4e2ZvsE4_Y-NxuliDwEgpyud_Cv69Vq8pV-ovAH0S6LqtFUWuRBGVUisLEfUPVifrPWnL_Qv8-5N7SxLOdEJyEfeSoSTRf7ISbQ6ytVSr_2WxuBbkvM-GvXwBUiGwHFjtPZK3qktPTU_uI-jazQr-_JgsR8asmgq-J2PgmMWtfKTiGruDHzW74xbaDTSoPQ6sXi7zuzesLGlzHVjBnyza3QLmOCHkgFYUhGObp2kolafTJ7wknFd65bt529LfUYd152R56gItFtSDUpKSCoSFeyU-945cYns2OlA",
#                          convo_id="fa50c0da-ed21-4f89-a248-d4c8bc010451", parent_id="23943f37-9078-4798-8acf-a3fc8db4fe1d", model="gpt-4", prompt="继续"))
# print(a)


async def chat_conversation(access_token: str) -> list:
    """
    获取 conversation
    """
    chatbot = AsyncChatbot(config={
        "access_token": access_token
    })
    data = await chatbot.get_conversations()
    return data


async def chat_msg_history(access_token: str, convo_id: str) -> dict:
    """
    根据id获取历史信息
    """
    chatbot = AsyncChatbot(config={
        "access_token": access_token
    })
    data = await chatbot.get_msg_history(convo_id)
    return data


# TODO:fix：无法测通，入参运行报错
async def chat_gen_title(access_token: str, convo_id: str, message_id: str) -> None:
    chatbot = AsyncChatbot(config={
        "access_token": access_token
    })
    data = await chatbot.gen_title(convo_id, message_id)
    return data


async def chat_change_title(access_token: str, convo_id: str, title: str) -> None:
    """
    修改 conversation 的标题
    """
    chatbot = AsyncChatbot(config={
        "access_token": access_token
    })
    data = await chatbot.change_title(convo_id, title)
    return data


async def chat_delete_conversation(access_token: str, convo_id: str) -> None:
    """
    删除 conversation
    """
    chatbot = AsyncChatbot(config={
        "access_token": access_token
    })
    data = await chatbot.delete_conversation(convo_id)
    return data


async def chat_clear_conversations(access_token: str) -> None:
    """
    清除所有 conversation
    """
    chatbot = AsyncChatbot(config={
        "access_token": access_token
    })
    data = await chatbot.clear_conversations()
    return data
