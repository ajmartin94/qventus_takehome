"""Domain core: the agent's decisions as pure functions over Pydantic models.

Imports nothing outside itself. Hospital rules arrive as data (`policy.py`); the
current time is passed in, never read.
"""
