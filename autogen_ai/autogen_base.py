from autogen import AssistantAgent, UserProxyAgent, ConversableAgent
import streamlit as st
import asyncio
import autogen_ai


class TrackableAssistantAgent(AssistantAgent):
    def _process_received_message(self, message, sender, silent):
        return super()._process_received_message(message, sender, silent)


class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        return super()._process_received_message(message, sender, silent)


if __name__ == '__main__':
    llm_config = {"model": "deepseek-chat", "api_key": '',
                  "base_url": "https://api.deepseek.com"}
    assistant = TrackableAssistantAgent(name="assistant", llm_config=llm_config)

    user_proxy = TrackableUserProxyAgent(
        name="User",
        code_execution_config=False,
        human_input_mode="TERMINATE",
        llm_config=llm_config
    )

    assistant.register_for_llm(name="user", description="A simple user info api")(autogen_ai.fetch_user_info)
    user_proxy.register_for_execution(name="user")(autogen_ai.fetch_user_info)

    llm_config = {"model": "deepseek-chat", "api_key": "",
                  "base_url": "https://api.deepseek.com"}

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    user_proxy.initiate_chat(recipient=assistant,
                             # 模型归纳
                             summary_method="reflection_with_llm",
                             message="美国的地理信息",
                             max_turns=3)
