import asyncio

import requests
import streamlit as st
from autogen import ConversableAgent


class TrackableAgent(ConversableAgent):
    def _process_received_message(self, message, sender, silent):
        # 打印 agent 互相沟通的信息
        # with st.chat_message(sender.name):
        #     st.markdown(message)
        return super()._process_received_message(message, sender, silent)


def fetch_user_info(msg: str) -> str:
    """
    自定义函数
    Returns:

    """
    url = 'http://127.0.0.1:5000/get_user_data'
    params = {'msg': msg}

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")


def fetch_map_info(msg: str) -> str:
    """
    自定义函数
    Returns:

    """
    url = 'http://127.0.0.1:5000/get_map_data'
    params = {'msg': msg}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")


if __name__ == '__main__':
    with st.sidebar:
        st.header("OpenAI Configuration")
        st.selectbox("Model", ['deepseek-chat', 'deepseek'], index=1)
        st.text_input("API Key", type="password")

    with st.container():
        user_input = st.chat_input("问点什么...")
        if user_input:
            with st.chat_message('User'):
                st.markdown(user_input)

        llm_config = {"model": "deepseek-chat", "api_key": "",
                      "base_url": "https://api.deepseek.com"}
        assistant = TrackableAgent(
            name="Assistant",
            # 提示词
            system_message="你是一个AI助手，帮助人们提问时，准确回答人们需要的信息。"
                           "Return 'TERMINATE' when the task is done.",
            llm_config={"config_list": [llm_config]},
        )

        user_proxy = TrackableAgent(
            name="User",
            llm_config={"config_list": [llm_config]},
            # 提示词
            system_message="根据AI助手给予的信息回答问题。",
            # 停止条件
            is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
            # 不需要人类输入
            human_input_mode="NEVER",
        )
        # 注册agent tool
        assistant.register_for_llm(name="userInfo", description="A simple user info api")(fetch_user_info)
        assistant.register_for_llm(name="mapInfo", description="A simple country info api")(fetch_map_info)

        user_proxy.register_for_execution(name="userInfo")(fetch_user_info)
        user_proxy.register_for_execution(name="mapInfo")(fetch_map_info)

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


        async def initiate_chat():
            result = user_proxy.initiate_chat(recipient=assistant,
                                              # 模型归纳
                                              summary_method="reflection_with_llm",
                                              message=user_input,
                                              max_turns=3)
            # 归纳总结输出
            with st.chat_message('Assistant'):
                st.markdown(result.summary)


        # Run the asynchronous function within the event loop
        loop.run_until_complete(initiate_chat())
