from dashscope import Generation 
import os
from prompt import generate_prompt


# 设置 DashScope 的 API Key
DASHSCOPE_API_KEY = 'sk-xx'


def suggestions(text):
    prompt = generate_prompt(text)

    # 调用 Qwen 大模型
    response = Generation.call(
        model="qwen-turbo",  # Qwen 的轻量模型
        api_key=DASHSCOPE_API_KEY,
        messages=[
            {"role": "system", "content": "你是一个专业的中文写作润色助手，输出简洁的修改建议。"},
            {"role": "user", "content": prompt}
        ]
    )
    suggestions = response['output']['text']
    # 解析 JSON 格式的修改建议
    try:
        suggestions = eval(suggestions)  # 使用 eval 安全地解析 JSON 字符串
    except Exception as e:
        print("解析建议时出错:", e)
        suggestions = []
    return suggestions

if __name__ == "__main__":
    # 测试 suggestions 函数
    text = "这个产品可能有点问题，用户体验不是很好。"
    result = suggestions(text)
    print("修改建议:", result)