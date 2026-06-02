# 🚀 青创 Pilot (Macau Startup Pilot) - 极速演示部署指南

本项目采用前后端分离架构，后端为基于 Python 的 FastAPI 引擎，前端为基于 Vue 3 + Vite 的交互页面。
本指南专为**快速团队内部演示**与**公网穿透访问**设计。

##  环境准备

在开始之前，请确保你的本地计算机已安装以下环境：
- [Python 3.10+](https://www.python.org/)
- [Node.js (含 npm)](https://nodejs.org/)
- 有效的 DeepSeek API Key

---

##  第一阶段：本地服务启动

### 1. 启动后端引擎 (FastAPI)
打开终端，进入项目根目录：
```bash
# 安装后端依赖
pip install -r requirements.txt

# 启动 FastAPI 服务 (默认监听 8000 端口)
uvicorn main:app --reload
```
*终端保持开启，不要关闭。*

### 2. 配置并启动前端页面 (Vue + Vite)
新开一个终端，进入 `frontend` 目录：
```bash
# 安装前端依赖
npm install
```

**关键安全配置：** 
确保 `frontend/vite.config.js` 中已配置允许外部网络访问（突破 Vite 的 DNS 重绑定拦截）：
```javascript
import { fileURLToPath, URL } from 'node:url'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    allowedHosts: true, // 允许 localtunnel 等穿透域名访问
    host: '0.0.0.0'     // 监听所有网络接口
  },
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
```

```bash
# 启动前端服务 (默认监听 5173 端口)
npm run dev
```
*终端保持开启，不要关闭。*

---

##  第二阶段：内网穿透公网发布 (Localtunnel)

为了让队友在公网通过手机或电脑直接访问，我们将使用 `localtunnel` 将本地端口映射到公网。

### 1. 穿透后端接口
新开第三个终端，执行以下命令：
```bash
npx localtunnel --port 8000
```
> **注意：** 终端会输出一个绿色的公网网址（例：`https://xxx.loca.lt`）。这就是你后端的公网 API 地址。

### 2. 更新前端请求地址
拿到后端公网地址后，打开前端代码：
- `src/views/Diagnose.vue`
- `src/views/Ideation.vue`
将其中的后端请求地址（原为 `http://127.0.0.1:8000/api/...`）**全部替换为刚刚生成的后端公网地址**，然后保存文件。

### 3. 穿透前端页面
新开第四个（最后一个）终端，执行以下命令：
```bash
npx localtunnel --port 5173
```
> **注意：** 终端会再次输出一个绿色的公网网址（例：`https://yyy.loca.lt`）。**这就是最终发给队友的演示链接！**

---

## 🚨 常见问题排查 (Troubleshooting)

1. **手机端打开报错 "Blocked request..."**
   - **原因：** Vite 安全机制拦截了外网域名。
   - **解决：** 检查 `vite.config.js` 中是否正确添加了 `server: { allowedHosts: true, host: '0.0.0.0' }`，修改后需重启 `npm run dev`。

2. **手机端显示 "无法正常运作 / 504 Gateway Time-out"**
   - **原因：** localtunnel 免费通道不稳定，隧道意外断开。
   - **解决：** 在终端中按 `Ctrl + C` 强制关闭对应的 localtunnel 进程，重新执行穿透命令获取新网址即可。*(若后端网址更新，记得同步修改 Vue 代码)*

3. **第一次打开网址出现英文安全提示页**
   - **原因：** localtunnel 的防滥用机制。
   - **解决：** 直接点击页面上的蓝色按钮 **"Click to Continue"** 即可正常进入青创 Pilot 页面。
