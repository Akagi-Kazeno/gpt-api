from revChatGPT.V1 import AsyncChatbot


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
