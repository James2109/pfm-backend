import json
from typing import Annotated, List

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

from src.models.messages import MessageFrom
from src.repositories import PlayerRepository, PlanRepository
from src.core.config import settings

import yaml
from pathlib import Path


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# --- Tool factories (need repo instances at runtime) ---

def create_tools(player_repo: PlayerRepository, plan_repo: PlanRepository, user_id: str):

    # @tool
    # async def search_player(name: str) -> str:
    #     """Search for a football player by name. Returns player stats including position, age, goals, assists, club, etc."""
    #     players = await player_repo.get_by_name(name)
    #     if not players:
    #         return "No players found."
    #     return json.dumps(players, default=str)

    # @tool
    # async def get_user_plans() -> str:
    #     """Get all training and nutrition plans for the current user."""
    #     plans = await plan_repo.get_by_user_id(user_id)
    #     if not plans:
    #         return "No plans found for this user."
    #     return json.dumps(plans, default=str)

    # return [search_player, get_user_plans]
    return []


class AgentService:
    def __init__(self, model: str = "gemini-3-flash-preview"):
        self.model_name = model
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        path = settings.PROMPTS_DIR / "agent_prompt.yaml"
        with open(path, "r") as f:
            return yaml.safe_load(f)["system_prompt"]

    def _build_graph(self, tools: list) -> StateGraph:
        llm = ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=settings.GEMINI_API_KEY,
        )
        llm_with_tools = llm.bind_tools(tools) if tools else llm

        async def chatbot(state: AgentState):
            return {"messages": [await llm_with_tools.ainvoke(state["messages"])]}

        graph = StateGraph(AgentState)
        graph.add_node("chatbot", chatbot)
        graph.add_edge(START, "chatbot")

        if tools:
            graph.add_node("tools", ToolNode(tools=tools))
            graph.add_conditional_edges("chatbot", tools_condition)
            graph.add_edge("tools", "chatbot")
        else:
            graph.add_edge("chatbot", END)

        return graph.compile()

    def _build_history(self, messages: list) -> list:
        """Convert DB messages to LangChain message format."""
        history = [SystemMessage(content=self.system_prompt)]
        for msg in messages:
            if msg["message_from"] == MessageFrom.HUMAN.value:
                history.append(HumanMessage(content=msg["message"]))
            else:
                history.append(AIMessage(content=msg["message"]))
        return history

    async def chat(
        self,
        user_message: str,
        conversation_history: list,
        player_repo: PlayerRepository,
        plan_repo: PlanRepository,
        user_id: str,
    ) -> str:
        """Run the agent: send message, handle tool calls automatically, return final response."""
        tools = create_tools(player_repo, plan_repo, user_id)
        graph = self._build_graph(tools)

        messages = self._build_history(conversation_history)
        messages.append(HumanMessage(content=user_message))

        result = await graph.ainvoke({"messages": messages})

        # Last message is the final AI response
        content = result["messages"][-1].content
        if isinstance(content, list):
            return "".join(part.get("text", "") for part in content if isinstance(part, dict))
        return content
