<template>
  <div class="diagnose-container">
    <h1 class="title">青创 Pilot - 深度项目诊断与孵化</h1>

    <div v-if="!isLoading && !reportData" class="form-section">
      <div class="form-group">
        <label>1. 你的目标用户是谁？具体痛点是什么？</label>
        <textarea v-model="formData.target_user" placeholder="例如：缺乏商赛经验的澳门大学生，不知道怎么写BP..."></textarea>
      </div>
      <div class="form-group">
        <label>2. 你的产品独特优势是什么？</label>
        <textarea v-model="formData.unique_value" placeholder="例如：不是无脑代写，而是导师制引导..."></textarea>
      </div>
      <div class="form-group">
        <label>3. 目前团队最缺的资源是什么？</label>
        <textarea v-model="formData.missing_resources" placeholder="例如：缺懂前端的开发，缺推广资金..."></textarea>
      </div>
      <div class="form-group">
        <label>4. 产品初期的冷启动方案是什么？</label>
        <textarea v-model="formData.cold_start" placeholder="例如：先在自己学校的社团群里免费内测..."></textarea>
      </div>
      <div class="form-group">
        <label>5. 谁最终会为这个产品买单？</label>
        <textarea v-model="formData.payer" placeholder="例如：打算以SaaS形式卖给各大学的就业指导中心..."></textarea>
      </div>
      <div class="form-group">
        <label>6. 现有替代方案有什么缺陷？</label>
        <textarea v-model="formData.competitor_flaws" placeholder="例如：市面上的通用AI废话太多，评委一眼就能看穿..."></textarea>
      </div>

      <button class="submit-btn" @click="submitDiagnosis">开始 AI 深度诊断</button>
      <button class="submit-btn outline" @click="$router.push('/')" style="margin-top: 15px;">返回首页</button>
    </div>

    <div v-if="isLoading" class="loading-section">
      <div class="spinner"></div>
      <h2 class="loading-text">{{ currentLoadingText }}</h2>
      <p class="loading-subtext">AI 引擎全速运转中，请稍候...</p>
    </div>

    <div v-if="!isLoading && reportData" class="report-section">
      <h2 class="report-title">项目诊断报告</h2>
      <p class="overall-comment"><strong>导师总评：</strong>{{ reportData.overall_comment }}</p>

      <div class="report-content">
        <div class="chart-container">
          <div ref="radarChartRef" class="radar-chart"></div>
        </div>
        <div class="feedback-container">
          <div class="feedback-item">
            <h3>💡 項目創新性 ({{ reportData.radar_scores.innovation }}/10)</h3>
            <p>{{ reportData.detailed_feedback.innovation_feedback }}</p>
          </div>
          <div class="feedback-item">
            <h3>🚀 項目可行性 ({{ reportData.radar_scores.feasibility }}/10)</h3>
            <p>{{ reportData.detailed_feedback.feasibility_feedback }}</p>
          </div>
          <div class="feedback-item">
            <h3>💰 項目盈利能力 ({{ reportData.radar_scores.profitability }}/10)</h3>
            <p>{{ reportData.detailed_feedback.profitability_feedback }}</p>
          </div>
          <div class="feedback-item">
            <h3>⚔️ 市場競爭力 ({{ reportData.radar_scores.competitiveness }}/10)</h3>
            <p>{{ reportData.detailed_feedback.competitiveness_feedback }}</p>
          </div>
          <div class="feedback-item">
            <h3>👥 團隊綜合能力 ({{ reportData.radar_scores.team }}/10)</h3>
            <p>{{ reportData.detailed_feedback.team_feedback }}</p>
          </div>
        </div>
      </div>

      <div class="advanced-actions">
        <h3 class="action-title">下一步进阶操作</h3>
        <div class="action-buttons-row">
          <button class="btn-adv bp-btn" @click="generateBP" :disabled="bpData != null">
            📑 {{ bpData ? '已生成 BP 框架' : '生成防守型 BP 框架' }}
          </button>
          <button class="btn-adv pitch-btn" @click="generatePitch" :disabled="pitchData != null">
            🎤 {{ pitchData ? '已生成路演剧本' : '生成 5 分钟路演剧本' }}
          </button>
        </div>
      </div>
    </div>

    <div v-if="bpData" class="doc-section">
      <h2 class="report-title">📑 商业计划书 (BP) 核心框架</h2>
      <div class="highlight-box">
        <strong>一句话 Pitch：</strong> {{ bpData.one_sentence_pitch }}
      </div>
      <div class="modules-grid">
        <div v-for="(mod, index) in bpData.modules" :key="index" class="module-card">
          <h4>{{ mod.module_name }}</h4>
          <p class="judge-focus"><strong>评委视角：</strong>{{ mod.judge_focus }}</p>
          <ul>
            <li v-for="(pt, i) in mod.writing_bullet_points" :key="i">{{ pt }}</li>
          </ul>
          <div class="defense-shield">
            <strong>🛡️ 防守策略：</strong>{{ mod.defense_strategy }}
          </div>
        </div>
      </div>
    </div>

    <div v-if="pitchData" class="doc-section">
      <h2 class="report-title">🎤 沉浸式路演剧本 (预计耗时: {{ pitchData.total_time_estimated }})</h2>

      <div class="slides-container">
        <div v-for="(slide, index) in pitchData.slides" :key="index" class="slide-card">
          <div class="slide-header">
            <span class="slide-num">Slide {{ slide.slide_number }}</span>
            <span class="slide-time">⏱️ {{ slide.time_allocation }}</span>
          </div>
          <h4 class="slide-title">{{ slide.slide_title }}</h4>
          <div class="visual-cue"><strong>🖼️ 画面建议：</strong>{{ slide.visual_suggestion }}</div>
          <div class="script-box">
            <strong>🗣️ 台词与走位：</strong>
            <p>{{ slide.script }}</p>
          </div>
        </div>
      </div>

      <div class="qa-section">
        <h3>🔥 评委刁钻提问预判 (Q&A)</h3>
        <div v-for="(qa, index) in pitchData.q_and_a_prediction" :key="index" class="qa-card">
          <p class="q-text"><strong>Q:</strong> {{ qa.possible_question }}</p>
          <p class="a-text"><strong>A:</strong> {{ qa.suggested_answer }}</p>
        </div>
      </div>
    </div>

    <div v-if="!isLoading && reportData" class="bottom-actions">
      <button class="submit-btn outline" @click="resetForm">重新诊断新项目</button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, nextTick } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'

const formData = reactive({
  target_user: '',
  unique_value: '',
  missing_resources: '',
  cold_start: '',
  payer: '',
  competitor_flaws: ''
})

const isLoading = ref(false)
const currentLoadingText = ref('')
let textInterval = null

// 存储三大块数据
const reportData = ref(null)
const bpData = ref(null)
const pitchData = ref(null)

const radarChartRef = ref(null)

// 启动轮播文案
const startLoading = (texts) => {
  isLoading.value = true
  let step = 0
  currentLoadingText.value = texts[0]
  textInterval = setInterval(() => {
    step = (step + 1) % texts.length
    currentLoadingText.value = texts[step]
  }, 2000)
}

// 停止轮播
const stopLoading = () => {
  isLoading.value = false
  clearInterval(textInterval)
}

// 1. 深度诊断
const submitDiagnosis = async () => {
  if (!formData.target_user || !formData.unique_value) {
    alert("请至少填写前两项核心信息！")
    return
  }
  startLoading(["正在分析可行性...", "正在评估痛点...", "正在生成诊断报告..."])
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/diagnose', formData)
    reportData.value = response.data
    await nextTick()
    renderRadarChart(reportData.value.radar_scores)
  } catch (error) {
    alert("请求服务器失败！")
  } finally {
    stopLoading()
  }
}

// 2. 生成 BP
const generateBP = async () => {
  startLoading(["正在重组商业逻辑...", "正在提取项目短板...", "正在构建防守反击 BP 框架..."])
  try {
    // 提取短板数据喂给下一个接口
    const weaknesses = Object.values(reportData.value.detailed_feedback).join(" ")
    const payload = {
      ...formData,
      diagnostic_weaknesses: weaknesses,
      gba_radar: "需要结合大湾区商赛标准"
    }
    const response = await axios.post('http://127.0.0.1:8000/api/generate_bp', payload)
    bpData.value = response.data
  } catch (error) {
    alert("BP生成失败！")
  } finally {
    stopLoading()
  }
}

// 3. 生成路演剧本
const generatePitch = async () => {
  startLoading(["正在设计舞台走位...", "预判评委刁钻问题...", "正在生成 5 分钟沉浸式路演剧本..."])
  try {
    const weaknesses = Object.values(reportData.value.detailed_feedback).join(" ")
    const payload = {
      project_name: "青创路演项目",
      one_sentence_pitch: bpData.value ? bpData.value.one_sentence_pitch : formData.unique_value,
      core_problem: formData.target_user,
      core_solution: formData.unique_value,
      business_model: formData.payer,
      diagnostic_weaknesses: weaknesses,
      gba_radar: "需要结合大湾区商赛标准"
    }
    const response = await axios.post('http://127.0.0.1:8000/api/generate_pitch', payload)
    pitchData.value = response.data
  } catch (error) {
    alert("剧本生成失败！")
  } finally {
    stopLoading()
  }
}

const renderRadarChart = (scores) => {
  if (!radarChartRef.value) return
  const myChart = echarts.init(radarChartRef.value)
  const option = {
    tooltip: {},
    radar: {
      indicator: [
        { name: '創新性', max: 10 }, { name: '可行性', max: 10 },
        { name: '盈利能力', max: 10 }, { name: '競爭力', max: 10 }, { name: '團隊能力', max: 10 }
      ],
      radius: '65%',
      axisName: { color: '#333', fontSize: 14, fontWeight: 'bold' }
    },
    series: [{
      type: 'radar',
      data: [{
        value: [scores.innovation, scores.feasibility, scores.profitability, scores.competitiveness, scores.team],
        name: 'AI 评委打分',
        areaStyle: { color: 'rgba(52, 152, 219, 0.4)' },
        lineStyle: { color: '#2980b9', width: 2 },
        itemStyle: { color: '#2980b9' }
      }]
    }]
  }
  myChart.setOption(option)
}

const resetForm = () => {
  reportData.value = null; bpData.value = null; pitchData.value = null;
  Object.keys(formData).forEach(key => formData[key] = '')
}
</script>

<style scoped>
.diagnose-container { max-width: 1000px; margin: 0 auto; padding: 40px 20px; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
.title { text-align: center; color: #2c3e50; margin-bottom: 30px; }
.form-group { margin-bottom: 20px; }
label { display: block; font-weight: bold; margin-bottom: 8px; color: #34495e; text-align: left; }
textarea { width: 100%; height: 80px; padding: 12px; border: 1px solid #bdc3c7; border-radius: 8px; resize: vertical; font-size: 14px; box-sizing: border-box; }
.submit-btn { display: block; width: 100%; padding: 15px; background-color: #2980b9; color: white; border: none; border-radius: 8px; font-size: 16px; font-weight: bold; cursor: pointer; transition: 0.3s; }
.submit-btn:hover { background-color: #3498db; }
.submit-btn.outline { background-color: transparent; color: #7f8c8d; border: 1px solid #bdc3c7; }
.loading-section { text-align: center; padding: 60px 0; }
.spinner { border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 50px; height: 50px; animation: spin 1s linear infinite; margin: 0 auto 20px auto; }
@keyframes spin { 100% { transform: rotate(360deg); } }
.loading-text { color: #2980b9; margin-bottom: 10px; }
.loading-subtext { color: #7f8c8d; }

/* 诊断报告样式 */
.report-section, .doc-section { background: #fdfdfd; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-top: 30px;}
.overall-comment { font-size: 16px; color: #e74c3c; background: #fadbd8; padding: 15px; border-radius: 8px; margin-bottom: 30px; }
.report-content { display: flex; gap: 30px; flex-wrap: wrap; }
.chart-container { flex: 1; min-width: 300px; display: flex; justify-content: center; align-items: center; }
.radar-chart { width: 100%; height: 400px; }
.feedback-container { flex: 1.5; min-width: 300px; }
.feedback-item { margin-bottom: 15px; padding-bottom: 15px; border-bottom: 1px solid #eee; }
.feedback-item h3 { margin: 0 0 8px 0; font-size: 16px; color: #2c3e50; }

/* 进阶操作区 */
.advanced-actions { margin-top: 40px; padding-top: 30px; border-top: 2px dashed #bdc3c7; text-align: center; }
.action-title { color: #2c3e50; margin-bottom: 20px; }
.action-buttons-row { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }
.btn-adv { flex: 1; min-width: 250px; padding: 15px; border-radius: 8px; font-size: 16px; font-weight: bold; border: none; cursor: pointer; transition: 0.3s; }
.btn-adv:disabled { opacity: 0.6; cursor: not-allowed; }
.bp-btn { background-color: #27ae60; color: white; }
.bp-btn:not(:disabled):hover { background-color: #2ecc71; transform: translateY(-3px); box-shadow: 0 5px 15px rgba(46, 204, 113, 0.4); }
.pitch-btn { background-color: #8e44ad; color: white; }
.pitch-btn:not(:disabled):hover { background-color: #9b59b6; transform: translateY(-3px); box-shadow: 0 5px 15px rgba(155, 89, 182, 0.4); }

/* BP & Pitch 渲染样式 */
.report-title { text-align: center; color: #2c3e50; border-bottom: 2px solid #ecf0f1; padding-bottom: 15px; margin-bottom: 25px; }
.highlight-box { background: #e8f4f8; padding: 15px; border-radius: 8px; color: #2980b9; margin-bottom: 20px; font-size: 18px; text-align: center;}
.modules-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
.module-card { background: #f8f9fa; padding: 20px; border-radius: 8px; border: 1px solid #e9ecef; }
.module-card h4 { margin-top: 0; color: #2c3e50; font-size: 18px; }
.judge-focus { color: #e67e22; font-size: 14px; margin-bottom: 10px; }
.module-card ul { padding-left: 20px; color: #34495e; font-size: 15px; line-height: 1.6; }
.defense-shield { margin-top: 15px; background: #eaeded; padding: 10px; border-radius: 6px; font-size: 14px; color: #16a085; }

.slides-container { display: flex; flex-direction: column; gap: 20px; }
.slide-card { background: white; border: 2px solid #ecf0f1; border-radius: 10px; padding: 20px; position: relative; }
.slide-header { display: flex; justify-content: space-between; margin-bottom: 15px; font-weight: bold; color: #7f8c8d; border-bottom: 1px solid #eee; padding-bottom: 10px; }
.slide-title { color: #8e44ad; font-size: 20px; margin: 0 0 15px 0; }
.visual-cue { background: #fdf2e9; color: #d35400; padding: 10px; border-radius: 6px; margin-bottom: 15px; font-size: 14px; }
.script-box { background: #f4f6f7; padding: 15px; border-radius: 6px; border-left: 4px solid #8e44ad; line-height: 1.8; color: #2c3e50; font-size: 16px;}
.qa-section { margin-top: 40px; }
.qa-card { background: #fdedec; padding: 15px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #e74c3c; }
.q-text { color: #c0392b; margin: 0 0 10px 0; }
.a-text { color: #27ae60; margin: 0; }
.bottom-actions { margin-top: 30px; }
</style>