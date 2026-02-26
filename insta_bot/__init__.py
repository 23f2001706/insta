"""
InstagramBot - Instagram DM Bot with Gemini AI

A simple, configurable bot for responding to Instagram DMs using Google Gemini AI.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

from .bot import InstagramBot
from .config import Config

__all__ = ["InstagramBot", "Config"]
