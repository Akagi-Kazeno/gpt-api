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
# CREATE USER uname WITH PASSWORD 'gpt-api';      # 创建用户（可不执行）

                                  # 密码↓
alter user postgres with password 'password';    # 修改postgres的密码

        # 数据库名称↓    所有者(用户名)↓
CREATE DATABASE gpt-api OWNER postgres;             # 创建数据库
```

## 3.配置外网连接(可省略)

### 1.编辑数据库配置文件(路径请已自己的为准)

- 打开数据库配置文件

```shell
          # 数据库版本↓ 
vim /etc/postgresql/14/main/postgresql.conf
```

- 找到 listen_addresses: '*' 取消前面的 # 注释，使用:wq保存退出(建议公网ip同时修改 Port)
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
