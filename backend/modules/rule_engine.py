import json
import os

def load_rules():
    rules_path = os.path.join(os.path.dirname(__file__), 'rules.json')
    with open(rules_path, 'r', encoding='utf-8') as f:
        return json.load(f)

RULES = load_rules()

def apply_rules(extracted_data):
    """
    根据提取的字段匹配规则
    extracted_data: dict，例如 {"payment_term": "逾期按万分之五", "dispute_clause": "有管辖权争议"}
    返回风险点列表
    """
    risks = []
    for rule in RULES:
        condition = rule["condition"]
        field = condition["field"]
        value = extracted_data.get(field)
        if not value:
            continue
        # 简单字符串包含匹配（可根据需要扩展）
        if condition["operator"] == "contains" and condition["value"] in value:
            risks.append({
                "clause": condition.get("clause_name", field),
                "reason": rule["reason"],
                "severity": rule["risk"]["level"],
                "suggestion": rule["risk"]["suggestion"]
            })
    return risks