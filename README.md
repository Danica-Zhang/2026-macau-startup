# 🚀 青创 Pilot (Macau Startup Pilot) - 极速演示部署指南

本项目采用前后端分离架构，后端为基于 Python 的 FastAPI 引擎，前端为基于 Vue 3 + Vite 的交互页面。
本指南专为**快速团队内部演示**与**公网穿透访问**设计。

## 🛠️ 环境准备

在开始之前，请确保你的本地计算机已安装以下环境：
- [Python 3.10+](https://www.python.org/)
- [Node.js (含 npm)](https://nodejs.org/)
- 有效的 DeepSeek API Key

---

## 📦 第一阶段：本地服务启动

### 1. 启动后端引擎 (FastAPI)
打开终端，进入项目根目录：
```bash
# 安装后端依赖
pip install -r requirements.txt

# 启动 FastAPI 服务 (默认监听 8000 端口)
uvicorn main:app --reload
