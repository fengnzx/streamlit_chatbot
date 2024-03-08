import openai
import streamlit as st

# 定义一个函数，用于在侧边栏中输入OpenAI API Key和OpenAI API Base
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key",key="api_key",type="password")
    openai_api_base = st.text_input("OpenAI API Base",key="api_base")

# 设置标题
st.title("💬 Chatbot Demo")

# 如果会话状态中没有消息，则设置初始消息
if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "assistant", "content": "How can I help you?"}]

# 遍历消息，在聊天消息中显示
for msg in st.session_state['messages']:
    st.chat_message(msg['role']).write(msg['content'])

# 如果输入框中有提示，则获取OpenAI API Key和OpenAI API Base
if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please enter your OpenAI API key.")
        st.stop()
    if not openai_api_base:
        st.info("Please enter your OpenAI API base.")
        st.stop()
    openai.api_key = openai_api_key
    openai.api_base = openai_api_base

    # 将输入的提示添加到消息中
    st.session_state['messages'].append({"role": "user", "content": prompt})   
    st.chat_message("user").write(prompt)
    # 使用OpenAI API和消息创建聊天会话
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=st.session_state['messages'])
    # 获取响应中的消息
    msg = response['choices'][0]['message']
    # 将消息添加到消息中
    st.session_state['messages'].append(msg)
    st.chat_message("assistant").write(msg['content'])