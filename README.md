# 简单部署

```shell
pip install poetry    # 安装poetry
poetry install        # 安装依赖
# 开始运行
poetry shell          # 进入虚拟环境
python app.py         # 运行
```

# 简单配置

```text
修改.env中的配置
```

# Ubuntu数据库配置

## 1.安装

```shell
sudo apt update
sudo apt install postgresql postgresql-contrib
```

## 2.创建数据库和用户(依次输入)

```shell
sudo su - postgres  # 切换用户
psql
        #  用户名↓                # 密码↓
# CREATE USER uname WITH PASSWORD "gpt-api";      # 创建用户（可不执行）

                                  # 密码↓
alter user postgres with password "password";    # 修改postgres的密码

        # 数据库名称↓    所有者(用户名)↓
CREATE DATABASE "gpt-api" OWNER postgres;             # 创建数据库
```

## 3.配置外网连接(可省略)

### 1.编辑数据库配置文件(路径请已自己的为准)

- 打开数据库配置文件

```shell
          # 数据库版本↓ 
vim /etc/postgresql/14/main/postgresql.conf
```

- 找到 listen_addresses: "*" 取消前面的 # 注释，使用:wq保存退出(建议公网ip同时修改 Port)
- 打开 pg_hba.conf

```shell
          # 数据库版本↓ 
vim /etc/postgresql/14/main/pg_hba.conf
```

- 在最下添加或修改后，使用:wq保存退出

```text
    # 允许任意用户从任意机器上以密码方式访问数据库
    host    all             all             0.0.0.0/0               md5
```

### 重启数据库

```shell
sudo systemctl restart postgresql
```

# Linux下持久化运行(Ubuntu)

1.安装screen

```shell
sudo apt install screen
```

2.创建会话

```shell
screen -S gpt-api
```

3.进入项目目录

```shell
cd ..
```

4.启动

```shell
poetry shell
python3 app.py
```

## 退出或关闭后

### 使用以下命令恢复会话

```shell
screen -r gpt-api
```

# Windows/Mac数据库配置

## 使用Docker拉取postgres镜像
```shell
docker pull postgres:latest
```

## 使用postgres镜像创建容器
```shell
                                                              # 密码↓
docker run --name postgres -d -p 5432:5432 -e POSTGRES_PASSWORD=password postgres
```
-----
# API接口
* [chat](#chat)
  1. [chat_ask](#1-chatask)
  2. [chat_conversation](#2-chatconversation)
  3. [chat_msg_history](#3-chatmsghistory)
  4. [chat_change_title](#4-chatchangetitle)
  5. [chat_delete_conversation](#5-chatdeleteconversation)
  6. [chat_clear_conversations](#6-chatclearconversations)

-----
## chat
### 1. chat_ask
询问
### 请求方法：
```bash
Method: POST
Type: RAW
URL: http://localhost:5000/api/chat/ask
```
### 请求体：
```json
{
  "prompt": "内容"
}
```
### 返回示例：
```json
{
    "response": {
        "author": {
            "metadata": {},
            "name": null,
            "role": "assistant"
        },
        "citations": [],
        "conversation_id": "47e1f050-0456-4c68-839b-36c3087492e6",
        "end_turn": true,
        "finish_details": "stop",
        "message": "Hello! How can I assist you today?",
        "model": "text-davinci-002-render-sha",
        "parent_id": "8ee0b295-793a-4696-b1f2-ab5054351bc5",
        "recipient": "all"
    }
}
```

-----

### 2. chat_conversation
获取 conversation
### 请求方法：
```bash
Method: POST
Type: RAW
URL: http://localhost:5000/api/chat/conversation
```
### 请求体：
```json
{
  "prompt": "内容"
}
```
### 返回示例：
```json
{
  "id": "1befe7a2-0dea-4287-b1b4-922cdf73a027",
  "title": "New chat",
  "create_time": "2023-06-05T13:17:06.358291+00:00",
  "update_time": "2023-06-05T13:17:09+00:00",
  "mapping": null,
  "current_node": null
}
```

-----

### 3. chat_msg_history
获取信息历史
### 请求方法：
```bash
Method: POST
Type: RAW
URL: http://localhost:5000/api/chat/msg/history
```
### 请求体：
```json
{
  "convo_id": "5b001ff5-93c3-4844-b190-3ce35ca0466e"
}
```
### 返回示例：
```json
{
	"title": "在GitHub创建pull request",
	"create_time": 1685962397.799465,
	"update_time": 1685966615.0,
	"mapping": {
		"ed62b6fe-5c2d-4173-9067-ad62f4a93d9a": {
			"id": "ed62b6fe-5c2d-4173-9067-ad62f4a93d9a",
			"message": {
				"id": "d9180354-2737-429a-8cd3-68c089501e6f",
				"author": {
					"role": "system",
					"metadata": {}
				},
				"create_time": 1685966597.037927,
				"content": {
					"content_type": "text",
					"parts": [""]
				},
				"status": "finished_successfully",
				"end_turn": true,
				"weight": 1.0,
				"metadata": {},
				"recipient": "all"
			},
			"parent": "aaa19ea2-78e0-48bc-98a8-f692a3dd4815",
			"children": ["aaa2ba4a-b175-4af7-88ce-e42bdc3f1816"]
		},
		"aaa19ea2-78e0-48bc-98a8-f692a3dd4815": {
			"id": "aaa19ea2-78e0-48bc-98a8-f692a3dd4815",
			"children": ["ed62b6fe-5c2d-4173-9067-ad62f4a93d9a"]
		},
		"aaa2ba4a-b175-4af7-88ce-e42bdc3f1816": {
			"id": "aaa2ba4a-b175-4af7-88ce-e42bdc3f1816",
			"message": {
				"id": "aaa2ba4a-b175-4af7-88ce-e42bdc3f1816",
				"author": {
					"role": "user",
					"metadata": {}
				},
				"create_time": 1685962397.800721,
				"content": {
					"content_type": "text",
					"parts": ["怎么在github上创建一个pull request"]
				},
				"status": "finished_successfully",
				"weight": 1.0,
				"metadata": {
					"timestamp_": "absolute"
				},
				"recipient": "all"
			},
			"parent": "ed62b6fe-5c2d-4173-9067-ad62f4a93d9a",
			"children": ["4c5b8fe4-8b2c-473a-bdfc-af23905ff927"]
		},
		"4c5b8fe4-8b2c-473a-bdfc-af23905ff927": {
			"id": "4c5b8fe4-8b2c-473a-bdfc-af23905ff927",
			"message": {
				"id": "4c5b8fe4-8b2c-473a-bdfc-af23905ff927",
				"author": {
					"role": "assistant",
					"metadata": {}
				},
				"create_time": 1685962424.848656,
				"content": {
					"content_type": "text",
					"parts": ["在 GitHub 上创建 pull request 的步骤如下：\n\n1. **Fork**：首先，你需要对你想做出贡献的仓库进行分叉（Fork）。你可以在仓库的主页上找到 'Fork' 按钮，点击它，GitHub 会创建一个该仓库的副本在你的账户下。\n\n2. **Clone**：接下来，你需要把分叉后的仓库克隆到你的本地电脑上。在你分叉后的仓库主页上，你会看到 'Code', 按钮，点击它然后复制 HTTPS URL。打开你的命令行界面，输入 `git clone [复制的URL]`。\n\n3. **创建新的分支**：在你的本地仓库上创建一个新的分支，分支的命名最好能反映你打算做的改动。在命令行界面，输入 `git checkout -b [分支名称]`。\n\n4. **做出改动**：在新的分支上做出你想要的改动，然后将这些改动添加到 git 的暂存区。在命令行界面，输入 `git add .`。如果你只想添加部分改动，你可以替换 `.` 为具体的文件名。\n\n5. **提交改动**：然后，你需要对这些改动进行提交，并给出描述性的提交信息。在命令行界面，输入 `git commit -m '[提交信息]'`。\n\n6. **推送改动**：将你的改动推送到你的远程仓库。在命令行界面，输入 `git push origin [分支名称]`。\n\n7. **创建 Pull Request**：最后，回到你在 GitHub 上的仓库主页，你会看到一个 'New pull request' 按钮，点击它。确保比较的分支是你刚才创建的分支，然后填写有关你改动的信息，最后点击 'Create pull request' 按钮。\n\n以上就是在 GitHub 上创建 Pull Request 的基本步骤。"]
				},
				"status": "finished_successfully",
				"end_turn": true,
				"weight": 1.0,
				"metadata": {
					"model_slug": "gpt-4",
					"finish_details": {
						"type": "stop",
						"stop": "<|diff_marker|>"
					},
					"timestamp_": "absolute"
				},
				"recipient": "all"
			},
			"parent": "aaa2ba4a-b175-4af7-88ce-e42bdc3f1816",
			"children": ["aaa21bf5-40ab-467c-8d12-190ec77bdf5e"]
		}
	},
	"moderation_results": [],
	"current_node": "13ad9ffc-b2ed-412c-9e4a-c87c153a2325"
}
```

-----

### 4. chat_change_title
修改 conversation 的标题
### 请求方法：
```bash
Method: POST
Type: RAW
URL: http://localhost:5000/api/chat/change/title
```
### 请求体：
```json
{
  "convo_id": "1befe7a2-0dea-4287-b1b4-922cdf73a027",
  "title": "测试"
}
```
### 返回示例：
```json
null
```

-----

### 5. chat_delete_conversation
删除 conversation
### 请求方法：
```bash
Method: POST
Type: RAW
URL: http://localhost:5000/api/chat/delete/conversation
```
### 请求体：
```json
{
  "convo_id": "1befe7a2-0dea-4287-b1b4-922cdf73a027"
}
```
### 返回示例：
```json
null
```
### 返回实例：
```json
null
```

-----

### 6. chat_clear_conversations
清除所有 conversation
### 请求方法：
```bash
Method: POST
Type: RAW
URL: http://localhost:5000/api/chat/clear/conversations
```
### 请求体：
```json
{}
```
### 返回示例：
```json
null
```
-----
[Back to api](#chat)