# backend/utils/ocr.py
import os
import base64
import io
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

# 从环境变量读取 AccessKey
ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")

def ocr_from_image_base64(image_base64: str) -> str:
    """使用阿里云OCR SDK识别图片base64"""
    from alibabacloud_ocr_api20210707.client import Client
    from alibabacloud_ocr_api20210707.models import RecognizeGeneralRequest
    from alibabacloud_tea_openapi.models import Config
    from alibabacloud_tea_util.models import RuntimeOptions

    # 创建客户端配置
    config = Config(
        access_key_id=ACCESS_KEY_ID,
        access_key_secret=ACCESS_KEY_SECRET,
        endpoint='ocr-api.cn-hangzhou.aliyuncs.com'
    )
    client = Client(config)

    # 构建请求
    request = RecognizeGeneralRequest()
    request.body = base64.b64decode(image_base64)

    # 调用接口
    response = client.recognize_general_with_options(request, RuntimeOptions())

    # 解析返回结果
    result = response.body.to_map()
    data = result.get('Data', '')
    
    # 从 JSON 中提取文字（根据阿里云返回结构）
    import json
    if isinstance(data, str):
        data = json.loads(data)
    
    text_parts = []
    if 'content' in data:
        return data['content']
    
    # 遍历文字块
    for block in data.get('prism_wordsInfo', []):
        text_parts.append(block.get('word', ''))
    
    return '\n'.join(text_parts)

def ocr_from_file(file_bytes: bytes, filename: str) -> str:
    """根据文件类型调用OCR"""
    ext = filename.split('.')[-1].lower()
    
    if ext in ['jpg', 'jpeg', 'png']:
        return ocr_from_image_base64(base64.b64encode(file_bytes).decode())
        
    elif ext == 'pdf':
        from pdf2image import convert_from_bytes
        images = convert_from_bytes(file_bytes)
        full_text = []
        for i, img in enumerate(images):
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode()
            page_text = ocr_from_image_base64(img_base64)
            full_text.append(f"第{i+1}页:\n{page_text}")
        return "\n".join(full_text)
        
    elif ext == 'txt':
        return file_bytes.decode('utf-8')
        
    else:
        raise ValueError(f"不支持的文件类型: {ext}")