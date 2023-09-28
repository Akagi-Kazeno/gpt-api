import uuid


def simple_uuid() -> str:
    """
    获取uuid
    :return:
    """
    primer_uuid = str(uuid.uuid4())
    final_uuid = primer_uuid.replace("-", "")
    return final_uuid
