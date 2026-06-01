<template>
  <div class="home-container">
    <header class="top-nav">
      <div class="logo">🚀 青创 Pilot</div>
      <div class="nav-actions">
        <button class="nav-btn login-btn" @click="showLogin = true">登录</button>
        <button class="nav-btn register-btn" @click="showRegister = true">注册</button>
      </div>
    </header>

    <div class="hero-section">
      <h1 class="main-title">青创 Pilot</h1>
      <p class="subtitle">你的 AI 创业赛事专属辅导引擎</p>

      <div class="intro-card">
        <h3>欢迎来到创业第一站 🚀</h3>
        <p>无论你只是有一个模糊的念头，还是已经带着成型的商业计划书准备参赛，青创 Pilot 都能为你提供最犀利、最务实的诊断与孵化建议。</p>
      </div>

      <div class="action-buttons">
        <button class="btn btn-new" @click="$router.push('/ideation')">
          <strong>还没明确想法？</strong>
          <span>快速测试，生成创业方向</span>
        </button>
        <button class="btn btn-pro" @click="$router.push('/diagnose')">
          <strong>已有初步构想？</strong>
          <span>深度诊断，直击项目痛点</span>
        </button>
      </div>
    </div>

    <div v-if="showLogin" class="modal-overlay" @click.self="showLogin = false">
      <div class="modal-content">
        <button class="close-btn" @click="showLogin = false">×</button>
        <h2>欢迎回来 👋</h2>
        <p class="modal-subtitle">登录青创 Pilot，同步你的项目进度</p>

        <div class="form-group">
          <label>用户名 / 邮箱</label>
          <input type="text" v-model="loginForm.username" placeholder="请输入账号">
        </div>
        <div class="form-group">
          <label>密码</label>
          <input type="password" v-model="loginForm.password" placeholder="请输入密码">
        </div>

        <button class="submit-btn" @click="handleLogin">立即登录</button>
        <p class="toggle-text">还没有账号？ <span @click="switchModal('register')">马上注册</span></p>
      </div>
    </div>

    <div v-if="showRegister" class="modal-overlay" @click.self="showRegister = false">
      <div class="modal-content">
        <button class="close-btn" @click="showRegister = false">×</button>
        <h2>创建账号 🚀</h2>
        <p class="modal-subtitle">加入青创 Pilot，开启你的商赛之旅</p>

        <div class="form-group">
          <label>邮箱</label>
          <input type="email" v-model="registerForm.email" placeholder="你的常用邮箱">
        </div>
        <div class="form-group">
          <label>设置密码</label>
          <input type="password" v-model="registerForm.password" placeholder="至少 8 位包含字母和数字">
        </div>
        <div class="form-group">
          <label>确认密码</label>
          <input type="password" v-model="registerForm.confirmPassword" placeholder="请再次输入密码">
        </div>

        <button class="submit-btn" @click="handleRegister">注册账号</button>
        <p class="toggle-text">已有账号？ <span @click="switchModal('login')">直接登录</span></p>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

// 弹窗状态控制
const showLogin = ref(false)
const showRegister = ref(false)

// 表单数据绑定
const loginForm = reactive({ username: '', password: '' })
const registerForm = reactive({ email: '', password: '', confirmPassword: '' })

// 切换弹窗逻辑
const switchModal = (target) => {
  if (target === 'login') {
    showRegister.value = false
    showLogin.value = true
  } else {
    showLogin.value = false
    showRegister.value = true
  }
}

// 模拟登录提交 (API 还没好，先弹窗提示)
const handleLogin = () => {
  if (!loginForm.username || !loginForm.password) {
    alert("账号和密码不能为空！")
    return
  }
  // TODO: 后续在这里通过 Axios 发送请求到 FastAPI
  alert(`测试成功！正准备登录账号: ${loginForm.username}\n（后端 API 接入后将实现真正跳转）`)
  showLogin.value = false
}

// 模拟注册提交
const handleRegister = () => {
  if (!registerForm.email || !registerForm.password) {
    alert("请完整填写注册信息！")
    return
  }
  if (registerForm.password !== registerForm.confirmPassword) {
    alert("两次输入的密码不一致！")
    return
  }
  alert(`测试成功！邮箱 ${registerForm.email} 注册请求已截获\n（后端 API 接入后将写入数据库）`)
  showRegister.value = false
}
</script>

<style scoped>
/* 容器与基础排版 */
.home-container {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
  background-color: #f8f9fa;
  position: relative;
}

/* 顶部导航栏 */
.top-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 40px;
  background: transparent;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
}
.logo { font-size: 1.5rem; font-weight: bold; color: #2c3e50; }
.nav-actions { display: flex; gap: 15px; }
.nav-btn {
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 15px;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}
.login-btn { background: transparent; color: #2980b9; border: 2px solid #2980b9; }
.login-btn:hover { background: #e8f4f8; }
.register-btn { background: #2980b9; color: white; border: 2px solid #2980b9; box-shadow: 0 4px 6px rgba(41, 128, 185, 0.2); }
.register-btn:hover { background: #3498db; transform: translateY(-2px); box-shadow: 0 6px 12px rgba(41, 128, 185, 0.3); }

/* 原有主视觉区微调 */
.hero-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  max-width: 800px;
  margin: 0 auto;
  padding: 100px 40px 40px 40px; /* 顶部留出导航栏空间 */
}
.main-title { font-size: 3rem; color: #2c3e50; margin-bottom: 10px; }
.subtitle { font-size: 1.5rem; color: #7f8c8d; margin-bottom: 40px; }
.intro-card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 40px; text-align: left; }
.intro-card h3 { margin-top: 0; color: #2980b9; }
.intro-card p { line-height: 1.6; color: #34495e; font-size: 16px; }
.action-buttons { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }
.btn { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px 30px; border: none; border-radius: 12px; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; width: 260px; }
.btn:hover { transform: translateY(-5px); box-shadow: 0 8px 20px rgba(0,0,0,0.1); }
.btn-new { background: #e8f4f8; color: #2980b9; border: 2px solid #2980b9; }
.btn-pro { background: #2980b9; color: white; }
.btn strong { font-size: 1.2rem; margin-bottom: 8px; }
.btn span { font-size: 0.9rem; opacity: 0.9; }

/* 弹窗遮罩层 */
.modal-overlay {
  position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.5); backdrop-filter: blur(5px);
  display: flex; justify-content: center; align-items: center;
  z-index: 100;
  animation: fadeIn 0.3s ease;
}
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

/* 弹窗内容 */
.modal-content {
  background: white; padding: 40px; border-radius: 16px;
  width: 100%; max-width: 400px; box-shadow: 0 10px 25px rgba(0,0,0,0.2);
  position: relative; animation: slideUp 0.3s ease;
}
@keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
.close-btn { position: absolute; top: 15px; right: 20px; font-size: 24px; background: none; border: none; color: #95a5a6; cursor: pointer; transition: color 0.2s; }
.close-btn:hover { color: #2c3e50; }
.modal-content h2 { margin: 0 0 10px 0; color: #2c3e50; }
.modal-subtitle { color: #7f8c8d; font-size: 14px; margin-bottom: 25px; }

/* 表单样式 */
.form-group { margin-bottom: 20px; text-align: left; }
.form-group label { display: block; font-weight: bold; margin-bottom: 8px; color: #34495e; font-size: 14px; }
.form-group input { width: 100%; padding: 12px; border: 1px solid #bdc3c7; border-radius: 8px; font-size: 14px; box-sizing: border-box; transition: border-color 0.3s; }
.form-group input:focus { outline: none; border-color: #3498db; box-shadow: 0 0 5px rgba(52, 152, 219, 0.3); }

/* 弹窗按钮与文字 */
.submit-btn { width: 100%; padding: 14px; background-color: #2980b9; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background 0.3s; margin-top: 10px; }
.submit-btn:hover { background-color: #3498db; }
.toggle-text { text-align: center; margin-top: 20px; font-size: 14px; color: #7f8c8d; }
.toggle-text span { color: #2980b9; font-weight: bold; cursor: pointer; text-decoration: underline; }
.toggle-text span:hover { color: #1abc9c; }
</style>