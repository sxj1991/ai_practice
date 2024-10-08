from autogen import AssistantAgent, UserProxyAgent, ConversableAgent
import streamlit as st
import asyncio
import autogen_ai


class TrackableAssistantAgent(AssistantAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)


class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)


if __name__ == '__main__':
    llm_config = {"model": "deepseek-chat", "api_key": '',
                  "base_url": "https://api.deepseek.com"}
    assistant = TrackableAssistantAgent(name="assistant", llm_config=llm_config)

    user_proxy = TrackableUserProxyAgent(
        name="User",
        code_execution_config=False,
        human_input_mode="NEVER",
        llm_config=llm_config
    )

    assistant.register_for_llm(name="user", description="A simple user info api")(autogen_ai.fetch_user_info)
    user_proxy.register_for_execution(name="user")(autogen_ai.fetch_user_info)

    with st.sidebar:
        st.header("OpenAI Configuration")
        st.selectbox("Model", ['deepseek-chat'], index=0)
        st.text_input("API Key", type="password")

    with st.container():
        st.header("Multi-turn Chat with Assistant")
        user_input = st.chat_input("问点什么...")

        if user_input:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            if "chat_initiated" not in st.session_state:
                st.session_state.chat_initiated = False

            if not st.session_state.chat_initiated:
                async def initiate_chat():
                    # 开启多轮对话，直到满足 max_turns
                    result = await user_proxy.a_initiate_chat(
                        recipient=assistant,
                        summary_method="reflection_with_llm",
                        message=user_input,
                        max_turns=3
                    )
                    # 显示对话结果
                    if result:
                        st.markdown(f"**Assistant:** {result.summary}")


                # 运行异步函数
                loop.run_until_complete(initiate_chat())

                loop.close()

                st.session_state.chat_initiated = True
            elif user_input == 'exit':
                st.stop()
