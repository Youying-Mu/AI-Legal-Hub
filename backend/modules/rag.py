# modules/rag.py
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec, CloudProvider, AwsRegion
import time

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
PINECONE_INDEX = os.getenv("PINECONE_INDEX", "legal-clauses")

# 全局变量，缓存索引对象
_index = None

def init_pinecone():
    """初始化 Pinecone 客户端并返回索引对象"""
    global _index
    if _index is not None:
        return _index

    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY 环境变量未设置")

    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # 检查索引是否存在，如果不存在则创建（首次运行时）
    existing_indexes = [idx.name for idx in pc.list_indexes()]
    if PINECONE_INDEX not in existing_indexes:
        print(f"索引 {PINECONE_INDEX} 不存在，正在创建...")
        pc.create_index(
            name=PINECONE_INDEX,
            dimension=1024,  # 对于 multilingual-e5-large 模型，维度是 1024
            metric="cosine",
            spec=ServerlessSpec(
                cloud=CloudProvider.AWS,
                region=AwsRegion.US_EAST_1
            )
        )
        # 等待索引就绪
        while not pc.describe_index(PINECONE_INDEX).status.ready:
            time.sleep(1)
        print(f"索引 {PINECONE_INDEX} 创建成功")

    _index = pc.Index(PINECONE_INDEX)
    return _index

def upsert_documents(docs):
    """
    批量插入文档到 Pinecone（使用 Pinecone 的 Integrated Embedding）
    docs: 列表，每个元素为 {"id": str, "text": str, "metadata": dict}
    """
    index = init_pinecone()
    try:
        # 准备记录
        records = []
        for doc in docs:
            record = {
                "_id": doc["id"],
                "text": doc["text"],   # 这是用于生成向量的字段
            }
            # 合并元数据
            if doc.get("metadata"):
                record.update(doc["metadata"])
            records.append(record)
        
        # 使用 upsert_records 方法（适用于 Integrated Embedding）
        result = index.upsert_records(
            namespace="legal_knowledge",
            records=records
        )
        print(f"成功插入 {len(records)} 条记录")
        return result
    except Exception as e:
        print(f"插入文档失败: {e}")
        raise

def search_similar(query, top_k=3, namespace="legal_knowledge"):
    """
    检索与 query 类似的法律条款
    返回: 列表，每个元素包含 text, score, metadata
    """
    try:
        index = init_pinecone()
    except Exception as e:
        print(f"Pinecone 初始化失败: {e}")
        return []
    
    try:
        # 使用 search_records 方法（文本检索，Pinecone 自动转向量）
        response = index.search_records(
            namespace=namespace,
            query={
                "inputs": {"text": query},
                "top_k": top_k
            },
            fields=["text"]  # 返回的字段
        )
        
        matches = []
        if response and 'result' in response and 'hits' in response['result']:
            for hit in response['result']['hits']:
                text = hit['fields'].get('text', '') if hit.get('fields') else ''
                score = hit.get('_score', 0)
                # 收集其他元数据
                metadata = {}
                if hit.get('fields'):
                    for k, v in hit['fields'].items():
                        if k != 'text':
                            metadata[k] = v
                matches.append({
                    "text": text,
                    "score": score,
                    "metadata": metadata,
                    "id": hit.get('_id', '')
                })
        return matches
    except Exception as e:
        print(f"检索失败: {e}")
        return []