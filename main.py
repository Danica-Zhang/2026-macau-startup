import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# ==========================================
# 0. 环境初始化与配置
# ==========================================
load_dotenv()
app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 加上这行允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


# ==========================================
# 1. 数据模型定义 (Pydantic Models)
# ==========================================
# 步骤1：问卷1（无想法用户）的数据模型
class IdeationData(BaseModel):
    team_role: str
    resources: str
    preference: str
    gba_radar: str
    complaint: str


# 步骤2 & 3：问卷2（有想法用户）的核心项目数据模型
class ProjectData(BaseModel):
    target_user: str
    unique_value: str
    missing_resources: str
    cold_start: str
    payer: str
    competitor_flaws: str


# 步骤4：BP 生成的数据模型 (需接收前期诊断短板)
class BPRequestData(BaseModel):
    target_user: str
    unique_value: str
    missing_resources: str
    cold_start: str
    payer: str
    competitor_flaws: str
    diagnostic_weaknesses: str
    gba_radar: str


# 步骤5：路演讲稿生成的数据模型
class PitchRequestData(BaseModel):
    project_name: str
    one_sentence_pitch: str
    core_problem: str
    core_solution: str
    business_model: str
    diagnostic_weaknesses: str
    gba_radar: str


# ==========================================
# 2. 核心接口定义 (API Endpoints)
# ==========================================

# 接口一：问卷1 - 快速诊断与方向启发
@app.post("/api/ideation")
async def fast_ideation(data: IdeationData):
    system_prompt = """
    # Role
    你是一名极其务实、极其犀利的青年创业孵化器导师。你的任务是根据毫无经验的大学生填写的趣味问卷，准确评估他们的基础条件，并为他们指明最可行的商赛起始方向。绝不盲目鼓励，必须严格执行降权规则。

    # Objective
    基于用户提供的能力、资源、偏好、地域属性和痛点吐槽，按照给定的 10 个维度输出高度结构化的快速诊断报告。

    # Direction Categories (仅限以下 6 类)
    1. 内容传播 / 知识服务型项目
    2. 专业服务 / 解决方案型项目
    3. 校园场景创新型项目
    4. 资源整合平台型项目
    5. AI工具应用 / 效率提升型项目
    6. 青年成长与就业支持型项目

    # Strict Downgrade Rules (核心降权逻辑，必须遵守)
    1. 资源门槛限制：如果用户表示“没有任何资源”或“只有一腔热血”，绝对禁止推荐“校园场景创新型”、“资源整合平台型”和“内容传播型”作为主方向。
    2. 技术门槛限制：如果用户缺乏技术能力且没有技术圈人脉，必须将“AI工具应用型”强行降权，转而推荐服务型项目。
    3. 本地化门槛：如果用户明确表示不需要本地特色，或缺乏大湾区/澳门资源，绝对禁止推荐“资源整合平台型”。

    # Output Format (Strict JSON)
    你必须严格输出以下 JSON 格式，内容要求口语化、犀利且极其具体。不要包含任何 Markdown 标记：
    {
      "status": "success",
      "current_stage": "（如：想法探索期、项目雏形期等，一句话说明原因）",
      "user_persona": "（如：资源驱动型、想法探索型等，结合其能力和资源给出定义）",
      "primary_direction": "（必须从 6 类方向中选出最匹配的 1 类，并结合其‘痛点吐槽’给出一个具体的虚拟项目点子）",
      "alternative_direction": "（给出 1 个备选方向类目，若条件极差可填‘暂无’）",
      "not_recommended": "（必须明确指出 1 个绝对不要碰的方向类目，并严厉说明缺乏什么资源/能力）",
      "current_shortboard": "（一针见血指出其目前的致命短板，如：无技术、无资金、痛点太弱）",
      "next_3_steps": [
        "第一步行动指南（必须具体到明天能做的事）",
        "第二步行动指南（如小规模验证方法）",
        "第三步行动指南"
      ],
      "ai_assistance": "（推荐平台后续的 AI 功能，如：AI痛点验证、AI目标用户梳理）",
      "gba_resource": "（如果不涉及大湾区填‘暂不需要’；若涉及，具体推荐某类孵化器或政策）",
      "enter_full_diagnosis": true_or_false
    }
    """
    user_input = f"团队角色: {data.team_role}\n资源: {data.resources}\n偏好: {data.preference}\n大湾区需求: {data.gba_radar}\n吐槽: {data.complaint}"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


# 接口二：问卷2 - 完整项目诊断与打分 (雷达图)
@app.post("/api/diagnose")
async def diagnose_project(data: ProjectData):
    system_prompt = """
    # Role & Objective
    你是一名“2026澳門青年創新創業大賽”的硬核评委。基于用户提供的商业项目信息，按照大赛规定的五大核心准则进行量化打分（1-10分），并给出犀利、一针见血的扣分原因和改进建议。

    # Evaluation Criteria
    1. 項目創新性：热词堆砌打低分；底层逻辑差异化打高分。
    2. 項目可行性：技术门槛高但资源匮乏、冷启动天真打低分。
    3. 項目盈利能力：买单方不明确打低分；To B/C 闭环清晰打高分。
    4. 市場競爭力：赛道拥挤易被大厂复制打低分。
    5. 團隊綜合能力：核心依赖外包打低分。

    # Output Format (Strict JSON)
    不要包含 Markdown 标记：
    {
      "status": "success",
      "radar_scores": {"innovation": 0, "feasibility": 0, "profitability": 0, "competitiveness": 0, "team": 0},
      "overall_comment": "（整体定性评价）",
      "detailed_feedback": {
        "innovation_feedback": "...", "feasibility_feedback": "...", "profitability_feedback": "...", "competitiveness_feedback": "...", "team_feedback": "..."
      }
    }
    """
    user_input = f"目标用户: {data.target_user}\n独特优势: {data.unique_value}\n资源缺口: {data.missing_resources}\n冷启动: {data.cold_start}\n买单方: {data.payer}\n竞品缺陷: {data.competitor_flaws}"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


# 接口三：调研准备 (生成工具包)
@app.post("/api/research")
async def generate_research_plan(data: ProjectData):
    system_prompt = """
    # Role & Objective
    你是一名资深市场调研专家，为缺乏经验的大学生生成可直接落地的实地调研方案。

    # Output Format (Strict JSON)
    不要包含 Markdown 标记：
    {
      "status": "success",
      "user_persona": {"demographics": "...", "core_scenarios": "..."},
      "questionnaire": [
        {"id": 1, "question": "...", "type": "单选/多选/开放式", "options": ["...", "..."]}
      ],
      "interview_questions": ["...", "...", "..."],
      "competitor_analysis": {"direct_competitor_direction": "...", "indirect_competitor_direction": "..."}
    }
    """
    user_input = f"目标用户: {data.target_user}\n独特优势: {data.unique_value}\n资源缺口: {data.missing_resources}\n冷启动: {data.cold_start}\n买单方: {data.payer}\n竞品缺陷: {data.competitor_flaws}"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


# 接口四：BP 框架生成 (防守反击型)
@app.post("/api/generate_bp")
async def generate_bp_framework(data: BPRequestData):
    system_prompt = """
    # Role & Objective
    你是顶级VC兼大湾区商赛导师。基于用户项目和前期的“诊断短板”，输出模块化的 BP 框架及“防御提示”。

    # Output Format (Strict JSON)
    不要包含 Markdown 标记：
    {
      "status": "success",
      "bp_title_suggestion": "...",
      "one_sentence_pitch": "...",
      "modules": [
        {
          "module_name": "1. 痛点与需求 (Problem)",
          "judge_focus": "...",
          "writing_bullet_points": ["...", "..."],
          "defense_strategy": "（结合 diagnostic_weaknesses，指导如何防守）"
        }
      ]
    }
    """
    user_input = f"目标用户: {data.target_user}\n独特优势: {data.unique_value}\n买单方: {data.payer}\n冷启动: {data.cold_start}\n竞品缺陷: {data.competitor_flaws}\n资源缺口: {data.missing_resources}\n大湾区意向: {data.gba_radar}\n诊断短板: {data.diagnostic_weaknesses}"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


# ==========================================
# 接口五：5分钟路演讲稿生成
# ==========================================
@app.post("/api/generate_pitch")
async def generate_pitch_deck(data: PitchRequestData):
    system_prompt = """
    # Role & Objective
    你是顶级路演教练。将商业计划转化为 5 分钟内极具感染力的路演剧本，并提前预判评委刁钻提问。

    # Output Format (Strict JSON)
    不要包含 Markdown 标记：
    {
      "status": "success",
      "total_time_estimated": "约 4分45秒",
      "slides": [
        {
          "slide_number": 1,
          "slide_title": "...",
          "visual_suggestion": "...",
          "script": "（加入 [停顿] 等舞台提示，主动化解 diagnostic_weaknesses）",
          "time_allocation": "30秒"
        }
      ],
      "q_and_a_prediction": [
        {"possible_question": "...", "suggested_answer": "..."}
      ]
    }
    """  # 👈 就是这里！绝对不能漏掉这三个双引号！

    user_input = f"项目名称: {data.project_name}\n一句话介绍: {data.one_sentence_pitch}\n核心痛点: {data.core_problem}\n解决方案: {data.core_solution}\n商业模式: {data.business_model}\n大湾区意向: {data.gba_radar}\n诊断短板: {data.diagnostic_weaknesses}"

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)