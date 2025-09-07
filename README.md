# 云审通 AI 工具

---

## 🤖 工具表单

| 模块 | 功能 | 开发 | 语言 | 备注 |
|:------:|:-------:|:------:|:------:|:------:|
| `zerocrash` | 相似对比 | 陆佳伟 | Rust | 核心业务，路由管理、流量控制、访问控制 |
| `embedding` | 文本嵌入 | 陆佳伟 | Python | 独立模块，嵌入计算 |
| `microsoft` | 文档处理 | 陆佳伟 | Python | 独立模块，文档读取 |
| `codespace` | 数据分析 | 陆佳伟 | Python | 独立模块，编写代码 |
| `paddleocr` | 图像识别 | 宋馥呈 | Python | 独立模块，发票识别、文字识别 |

---

## 💿 拉取镜像

```bash
# 用于相似对比的基础镜像
sudo docker pull mysql:8.0
sudo docker pull alpine:3.21
sudo docker pull rust:alpine3.21

# 用于数据分析的基础镜像
sudo docker pull ubuntu:22.04

# 用于发票识别的基础镜像
sudo docker pull python:3.8.18-slim

# 用于文本嵌入的基础镜像
sudo docker pull nvidia/cuda:12.8.0-cudnn-runtime-ubuntu22.04
```

---

## 🛠️ 构建镜像

> 通过设置环境变量 `TARGETARCH` 来指定目标平台架构。

```bash
# 构建适用于 `x86_64` 架构的镜像
export TARGETARCH=x86_64-unknown-linux-musl
sudo docker-compose build

# 构建适用于 `aarch64` 架构的镜像
export TARGETARCH=aarch64-unknown-linux-musl
sudo docker-compose build
```

---

## 🚀 启动服务

```bash
sudo docker-compose up -d
```

---

## 🛑 停止服务

```bash
sudo docker-compose down
```

---

## 💻 常用命令

```bash
1️⃣ > docker system prune -a -f
清理所有未使用的资源，不会删除正在运行的容器和被使用的镜像：
 - 所有构建缓存
 - 所有停止的容器
 - 所有未被使用的镜像
 - 所有未被任何容器使用的卷
 - 所有未被任何容器引用的网络
```
