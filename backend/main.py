from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from utils.ocr import ocr_from_file
from modules.agent import react_agent
from modules.rule_engine import apply_rules
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== 保留的 OCR 测试接口 ==========
@app.post("/api/ocr-test")
async def test_ocr(file: UploadFile = File(...)):
    contents = await file.read()
    text = ocr_from_file(contents, file.filename)
    return {"filename": file.filename, "text": text}

# ========== 核心分析接口 ==========
@app.post("/api/analyze")
async def analyze(
    description: str = Form(None),
    file: UploadFile = File(None)
):
    # 1. 获取文本输入
    if not description and not file:
        raise HTTPException(status_code=400, detail="至少提供描述或文件")
    
    text = ""
    if file:
        contents = await file.read()
        text = ocr_from_file(contents, file.filename)
    if description:
        text = description + "\n" + text if text else description
    
    # 2. 调用 Agent 进行分析（返回的是文本报告）
    try:
        agent_output = react_agent(text)   # 这是纯文本
        # 尝试解析 JSON（如果 agent 返回的是 JSON）
        try:
            analysis = json.loads(agent_output)
            print(f"stage: {analysis.get('stage')}")
        except json.JSONDecodeError:
            # 如果解析失败，就构建一个结构化结果，把 agent 的输出作为 summary
            analysis = {
                "total_score": 50,
                "dimensions": {
                    "权利义务": 50,
                    "违约责任": 50,
                    "模糊条款": 50,
                    "合规风险": 50,
                    "缺失条款": 50
                },
                "risk_points": [],
                "summary": agent_output,   # 直接把整个报告放在这里
                "extracted_fields": {}     # 供规则引擎使用
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI分析失败: {str(e)}")
    
    # 3. 应用规则引擎（基于 extracted_fields，这里暂时为空）
    extracted_fields = analysis.get("extracted_fields", {})
    rule_risks = apply_rules(extracted_fields)   # 即使 extracted_fields 为空也不会报错
    # 合并风险点（如果 agent 已经生成了风险点，则追加；否则只使用规则引擎的）
    analysis["risk_points"] = analysis.get("risk_points", []) + rule_risks
    
    # 4. 返回结果
    analysis["text"] = analysis["summary"]  # 兼容前端
    return analysis

@app.get("/api/health")
def health():
    return {"status": "ok"}