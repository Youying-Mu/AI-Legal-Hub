# upload_data.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
import time

load_dotenv()

# 初始化 Pinecone
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index_name = os.getenv("PINECONE_INDEX")

# 检查索引是否存在
if index_name not in pc.list_indexes().names():
    print(f"创建索引 {index_name}...")
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='cosine',
        spec=ServerlessSpec(cloud='aws', region='us-west-2')  # 使用免费区
    )
    time.sleep(10)  # 等待索引就绪

index = pc.Index(index_name)

# 准备数据（示例：民法典相关条款）
data = [
    {
        "id": "art_722",
        "text": "《民法典》第722条：承租人无正当理由未支付或者迟延支付租金，经催告后在合理期限内仍不支付的，出租人可以解除合同。",
        "metadata": {"source": "民法典", "category": "租赁合同"}
    },
    {
        "id": "art_724",
        "text": "《民法典》第724条：有下列情形之一，非因承租人原因致使租赁物无法使用的，承租人可以解除合同：（一）租赁物被司法机关或者行政机关依法查封、扣押；（二）租赁物权属有争议；（三）租赁物具有违反法律、行政法规关于使用条件的强制性规定情形。",
        "metadata": {"source": "民法典", "category": "租赁合同"}
    },
    {
        "id": "art_563",
        "text": "《民法典》第563条：有下列情形之一的，当事人可以解除合同：（一）因不可抗力致使不能实现合同目的；（二）在履行期限届满前，当事人一方明确表示或者以自己的行为表明不履行主要债务；（三）当事人一方迟延履行主要债务，经催告后在合理期限内仍未履行；（四）当事人一方迟延履行债务或者有其他违约行为致使不能实现合同目的；（五）法律规定的其他情形。",
        "metadata": {"source": "民法典", "category": "合同解除"}
    },
    {
        "id": "art_584",
        "text": "《民法典》第584条：当事人一方不履行合同义务或者履行合同义务不符合约定，造成对方损失的，损失赔偿额应当相当于因违约所造成的损失，包括合同履行后可以获得的利益；但是，不得超过违约一方订立合同时预见到或者应当预见到的因违约可能造成的损失。",
        "metadata": {"source": "民法典", "category": "违约责任"}
    },
    {
        "id": "clause_rent_term",
        "text": "房屋租赁合同标准条款：租赁期内，如一方提前解除合同，应提前60日书面通知对方，并支付相当于2个月租金的违约金。",
        "metadata": {"source": "合同范本", "category": "提前解约"}
    }
]

# 生成嵌入向量（使用通义千问 embeddings，或简单使用随机数演示，但实际应调用模型）
# 这里简化：使用随机向量（仅用于测试，实际需用真实 embedding）
import numpy as np
embeddings = [np.random.rand(1536).tolist() for _ in data]

# 上传数据
vectors = []
for item, emb in zip(data, embeddings):
    vectors.append((item["id"], emb, item["metadata"]))
index.upsert(vectors=vectors, namespace="legal")

print("数据上传完成")