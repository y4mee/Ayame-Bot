#!/usr/bin/env python3
"""
Simple script to run the bot from root directory.
Usage: python run_bot.py
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import and run main
from backend.main import *

if __name__ == "__main__":
    import asyncio
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("👋 Bot shutting down gracefully...")
