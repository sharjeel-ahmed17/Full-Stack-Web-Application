#!/usr/bin/env python3
"""
MCP Server Startup Script

This script provides a convenient way to start the MCP server for task management tools.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.mcp.server import main

if __name__ == "__main__":
    print("Starting MCP Task Management Server...")
    main()