"""
Reducing code complexity (sorta) by wrapping aiohttp GET
into a simple function.
"""
from cogs.common import user_agent
from aiohttp import ClientSession

def get_req(session: ClientSession, url: str):
    return session.get(url, headers=user_agent)