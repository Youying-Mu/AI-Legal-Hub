from modules.rag import upsert_documents, search_similar

# 示例法律条款数据（你可以根据实际知识库扩展）
docs = [
    {
        "id": "001",
        "text": "甲方应在收到货物后三日内支付合同约定的全部货款。",
        "metadata": {"clause_type": "付款条款"}
    },
    {
        "id": "002",
        "text": "乙方应保证所交付产品符合国家相关质量标准，如不符合应负责免费更换。",
        "metadata": {"clause_type": "质量保证"}
    },
    {
        "id": "003",
        "text": "如任一方违约，守约方有权要求对方赔偿全部损失。",
        "metadata": {"clause_type": "违约责任"}
    },
    {
        "id": "004",
        "text": "租赁期间，出租人不得单方面解除合同，除非承租人严重违约。",
        "metadata": {"clause_type": "租赁合同"}
    }
]

# 插入数据
print("正在插入数据...")
upsert_documents(docs)
print("插入完成。")

# 检索测试
print("\n测试检索：房屋租赁合同 提前解约")
results = search_similar("房屋租赁合同 提前解约", top_k=2)
for r in results:
    print(f"相似度: {r['score']:.3f} | 文本: {r['text']}")