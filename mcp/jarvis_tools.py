from fastmcp import FastMCP
import wikipedia
import os
import requests
import json
from pathlib import Path

mcp = FastMCP("Jarvis")

MEMORY_FILE = "jarvis_memory.json"


# ==========================
# MEMORY SYSTEM
# ==========================

def load_memory():
    if not Path(MEMORY_FILE).exists():
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# ==========================
# STATUS
# ==========================

@mcp.tool()
def robot_status() -> dict:
    """
    Get Jarvis status.
    """
    return {
        "success": True,
        "status": "Jarvis is online and fully operational."
    }


# ==========================
# WIKIPEDIA SEARCH
# ==========================

@mcp.tool()
def wikipedia_search(topic: str) -> dict:
    """
    Get factual information about a topic.
    """
    try:
        summary = wikipedia.summary(topic, sentences=3)

        return {
            "success": True,
            "result": summary
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ==========================
# WEB SEARCH
# ==========================

@mcp.tool()
def web_search(query: str) -> dict:
    """
    Search the internet for current information.
    """
    try:
        api_key = os.getenv("TAVILY_API_KEY")

        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": api_key,
                "query": query,
                "search_depth": "basic",
                "max_results": 3,
                "include_answer": True
            },
            timeout=20
        )

        data = response.json()

        answer = data.get("answer")

        if answer:
            return {
                "success": True,
                "result": answer
            }

        results = []

        for item in data.get("results", []):
            results.append(item.get("content", ""))

        return {
            "success": True,
            "result": " ".join(results)
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ==========================
# NEWS
# ==========================

@mcp.tool()
def latest_ai_news() -> dict:
    """
    Get latest AI news.
    """
    return web_search(
        "latest artificial intelligence news today"
    )


@mcp.tool()
def robotics_news() -> dict:
    """
    Get latest robotics and humanoid robot news.
    """
    return web_search(
        "latest robotics and humanoid robot news today"
    )


@mcp.tool()
def tech_news() -> dict:
    """
    Get latest technology news.
    """
    return web_search(
        "latest technology news today"
    )


# ==========================
# WEATHER
# ==========================

@mcp.tool()
def weather(city: str) -> dict:
    """
    Get weather information.
    """
    return web_search(
        f"current weather in {city}"
    )


# ==========================
# MEMORY
# ==========================

@mcp.tool()
def remember(key: str, value: str) -> dict:
    """
    Store information permanently.
    """
    memory = load_memory()

    memory[key] = value

    save_memory(memory)

    return {
        "success": True,
        "message": f"Remembered {key}"
    }


@mcp.tool()
def recall(key: str) -> dict:
    """
    Recall stored information.
    """
    memory = load_memory()

    if key not in memory:
        return {
            "success": False,
            "message": "Nothing remembered."
        }

    return {
        "success": True,
        "value": memory[key]
    }


# ==========================
# DAILY BRIEFING
# ==========================

@mcp.tool()
def daily_briefing(city: str = "Bangalore") -> dict:
    """
    Get daily briefing.
    """
    try:
        weather_info = weather(city)
        ai_info = latest_ai_news()
        robotics_info = robotics_news()

        briefing = f"""
Weather:
{weather_info.get('result', '')}

AI News:
{ai_info.get('result', '')}

Robotics News:
{robotics_info.get('result', '')}
"""

        return {
            "success": True,
            "result": briefing
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# ==========================
# PROJECT ASSISTANT
# ==========================

@mcp.tool()
def project_status() -> dict:
    """
    Get current project.
    """
    memory = load_memory()

    return {
        "success": True,
        "project": memory.get(
            "current_project",
            "No active project stored."
        )
    }


@mcp.tool()
def save_project_idea(idea: str) -> dict:
    """
    Save a project idea.
    """
    memory = load_memory()

    ideas = memory.get("project_ideas", [])

    ideas.append(idea)

    memory["project_ideas"] = ideas

    save_memory(memory)

    return {
        "success": True,
        "message": "Project idea saved."
    }


@mcp.tool()
def get_project_ideas() -> dict:
    """
    Retrieve saved project ideas.
    """
    memory = load_memory()

    return {
        "success": True,
        "ideas": memory.get("project_ideas", [])
    }


@mcp.tool()
def suggest_project_improvement(project: str) -> dict:
    """
    Suggest improvements for a project.
    """
    return web_search(
        f"best improvements and ideas for {project}"
    )


@mcp.tool()
def troubleshooting_help(problem: str) -> dict:
    """
    Troubleshooting assistant.
    """
    return web_search(
        f"solution for {problem}"
    )


# ==========================
# START SERVER
# ==========================

if __name__ == "__main__":
    print("Starting Jarvis MCP Server...")
    mcp.run(transport="stdio")
