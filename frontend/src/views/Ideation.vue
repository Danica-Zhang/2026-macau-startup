<template>
  <div class="ideation-container">
    <h1 class="title">💡 创业方向启发引擎</h1>

    <div v-if="!isLoading && !resultData" class="form-section">
      <div class="intro">请如实填写以下情况，AI导师将为你匹配最合适的商赛起步方向。</div>

      <div class="form-group">
        <label>1. 团队角色：你们团队目前有哪些核心技能？</label>
        <textarea v-model="formData.team_role" placeholder="例如：一个懂Python后端的，一个擅长做PPT和演讲的..."></textarea>
      </div>
      <div class="form-group">
        <label>2. 手头资源：除了热情，你们能撬动什么社会/学校资源？</label>
        <textarea v-model="formData.resources" placeholder="例如：认识学生会主席能发问卷，或者亲戚家有工厂...（如果没有就填无）"></textarea>
      </div>
      <div class="form-group">
        <label>3. 个人偏好：你更倾向于做哪种类型的项目？</label>
        <textarea v-model="formData.preference" placeholder="例如：想做能赚钱的软件，或者想做有社会价值的公益项目..."></textarea>
      </div>
      <div class="form-group">
        <label>4. 大湾区雷达：项目是否需要结合大湾区/澳门本地特色？</label>
        <textarea v-model="formData.gba_radar" placeholder="例如：希望结合澳门的旅游业，或者大湾区的硬件供应链..."></textarea>
      </div>
      <div class="form-group">
        <label>5. 日常吐槽：生活中最让你心烦的一个痛点是什么？</label>
        <textarea v-model="formData.complaint" placeholder="例如：学校食堂排队太久，或者找不到靠谱的兼职..."></textarea>
      </div>

      <button class="submit-btn" @click="submitIdeation">测一测我的创业天命</button>
      <button class="submit-btn outline" @click="$router.push('/')" style="margin-top: 15px;">返回首页</button>
    </div>

    <div v-if="isLoading" class="loading-section">
      <div class="spinner"></div>
      <h2 class="loading-text">{{ currentLoadingText }}</h2>
      <p class="loading-subtext">AI 导师正在匹配你的资源与痛点，严格排雷中...</p>
    </div>

    <div v-if="!isLoading && resultData" class="result-section">
      <h2 class="report-title">🎯 专属方向启发报告</h2>

      <div class="result-card highlight">
        <h3>🔥 推荐主攻方向：{{ resultData.primary_direction }}</h3>
      </div>

      <div class="result-grid">
        <div class="grid-item">
          <h4>👤 你的创业画像</h4>
          <p>{{ resultData.user_persona }}</p>
        </div>
        <div class="grid-item warning">
          <h4>⛔ 绝对不要碰</h4>
          <p>{{ resultData.not_recommended }}</p>
        </div>
        <div class="grid-item alert">
          <h4>🩸 致命短板警告</h4>
          <p>{{ resultData.current_shortboard }}</p>
        </div>
        <div class="grid-item">
          <h4>备选方向</h4>
          <p>{{ resultData.alternative_direction }}</p>
        </div>
      </div>

      <div class="action-steps">
        <h3>🏃‍♂️ 接下来你该怎么做？(破局三步走)</h3>
        <ul>
          <li v-for="(step, index) in resultData.next_3_steps" :key="index">
            {{ step }}
          </li>
        </ul>
      </div>

      <div class="tips-box">
        <p><strong>💡 AI 建议：</strong>{{ resultData.ai_assistance }}</p>
        <p><strong>🌉 大湾区资源指路：</strong>{{ resultData.gba_resource }}</p>
      </div>

      <button v-if="resultData.enter_full_diagnosis" class="submit-btn" @click="$router.push('/diagnose')" style="margin-top: 20px;">
        我觉得可以！带这个方向去深度诊断 👉
      </button>
      <button class="submit-btn outline" @click="resetForm" style="margin-top: 15px;">我不满意，重新填写</button>
      <button class="submit-btn outline" @click="$router.push('/')" style="margin-top: 15px; border-color: #7f8c8d; color: #7f8c8d;">返回首页</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import axios from 'axios'

const formData = reactive({
  team_role: '',
  resources: '',
  preference: '',
  gba_radar: '',
  complaint: ''
})

const isLoading = ref(false)
const resultData = ref(null)

const loadingTexts = [
  "正在扫描你的团队基因...",
  "正在过滤不切实际的想法...",
  "匹配大湾区相关政策与痛点...",
  "正在生成防守反击策略..."
]
const currentLoadingText = ref(loadingTexts[0])
let textInterval = null

const submitIdeation = async () => {
  if (!formData.team_role || !formData.complaint) {
    alert("至少填一下团队角色和日常吐槽吧！这是AI启发的核心！")
    return
  }

  isLoading.value = true
  let step = 0
  currentLoadingText.value = loadingTexts[0]
  textInterval = setInterval(() => {
    step = (step + 1) % loadingTexts.length
    currentLoadingText.value = loadingTexts[step]
  }, 1500)

  try {
    const response = await axios.post('http://127.0.0.1:8000/api/ideation', formData)
    resultData.value = response.data
  } catch (error) {
    console.error("请求出错:", error)
    alert("请求服务器失败，请检查 FastAPI 后端状态！")
  } finally {
    isLoading.value = false
    clearInterval(textInterval)
  }
}

const resetForm = () => {
  resultData.value = null
  Object.keys(formData).forEach(key => formData[key] = '')
}
</script>

<style scoped>
.ideation-container { max-width: 900px; margin: 0 auto; padding: 40px 20px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
.title { text-align: center; color: #2c3e50; margin-bottom: 10px; }
.intro { text-align: center; color: #7f8c8d; margin-bottom: 30px; }
.form-group { margin-bottom: 20px; }
label { display: block; font-weight: bold; margin-bottom: 8px; color: #34495e; text-align: left; }
textarea { width: 100%; height: 80px; padding: 12px; border: 1px solid #bdc3c7; border-radius: 8px; resize: vertical; font-size: 14px; box-sizing: border-box; }
textarea:focus { outline: none; border-color: #3498db; box-shadow: 0 0 5px rgba(52, 152, 219, 0.3); }
.submit-btn { display: block; width: 100%; padding: 15px; background-color: #2980b9; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: background 0.3s; }
.submit-btn:hover { background-color: #3498db; }
.submit-btn.outline { background-color: transparent; color: #2980b9; border: 2px solid #2980b9; }
.submit-btn.outline:hover { background-color: #ecf0f1; }
.loading-section { text-align: center; padding: 60px 0; }
.spinner { border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto 20px auto; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
.loading-text { color: #2980b9; margin-bottom: 10px; }
.loading-subtext { color: #7f8c8d; }

/* 结果页样式 */
.result-section { background: #fdfdfd; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
.report-title { text-align: center; color: #2c3e50; border-bottom: 2px solid #ecf0f1; padding-bottom: 15px; margin-bottom: 25px; }
.result-card.highlight { background: #e8f4f8; padding: 20px; border-radius: 8px; margin-bottom: 25px; border-left: 5px solid #2980b9; }
.result-card.highlight h3 { margin: 0; color: #2980b9; }
.result-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 25px; }
.grid-item { background: #f8f9fa; padding: 15px; border-radius: 8px; }
.grid-item h4 { margin: 0 0 10px 0; font-size: 15px; color: #34495e; }
.grid-item p { margin: 0; font-size: 14px; color: #555; line-height: 1.5; }
.grid-item.warning { background: #fcf3cf; border-left: 4px solid #f1c40f; }
.grid-item.alert { background: #fadbd8; border-left: 4px solid #e74c3c; }
.action-steps { margin-bottom: 25px; }
.action-steps h3 { color: #2c3e50; font-size: 18px; }
.action-steps ul { padding-left: 20px; line-height: 1.8; color: #444; }
.tips-box { background: #eaeded; padding: 15px; border-radius: 8px; font-size: 14px; color: #555; }
.tips-box p { margin: 5px 0; }
</style>