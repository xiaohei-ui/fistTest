import gradio as gr
import requests
import json
import base64

# 百度 AI 文本识别 API 的 URL 和您的 API 密钥
API_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
API_KEY = "4mZAFTrpgpr758IA7ukxz3lU"
SECRET_KEY = "62awNB24Yt9Xl3CuoEgNqAktyOPjWfku"

def baidu_ocr(image):
    """使用百度 AI 接口进行文本识别"""
    with open(image, 'rb') as f:
        img = f.read()
    img_base64 = base64.b64encode(img).decode()

    request_url = API_URL + "?access_token=" + get_access_token()
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    data = {
        'image': img_base64,
    }
    response = requests.post(request_url, data=data, headers=headers)
    if response:
        result = response.json()
        return json.dumps(result, ensure_ascii=False)  # 返回美化后的JSON结果
    else:
        return "Error: Unable to connect to Baidu OCR API"

def get_access_token():
    """获取百度 AI 的访问令牌"""
    auth_url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + API_KEY + "&client_secret=" + SECRET_KEY
    response = requests.get(auth_url)
    if response:
        json_res = response.json()
        return json_res['access_token']
    else:
        return "Error: Unable to get access token"

# 创建 Gradio 界面
iface = gr.Interface(
    fn=baidu_ocr,
    inputs=gr.Image(type="filepath"),
    outputs="text",
    title="百度 AI 文本识别",
    description="上传图片，使用百度 AI 进行文本识别。"
)

# 启动应用
iface.launch()