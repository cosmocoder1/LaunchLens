"""Defines a centralized logger configuration for the MissionAnalyzer project.

This module provides a shared `LOGGER` instance for consistent, readable
console output across all scripts and modules. The logger is pre-configured
with formatting and a stream handler, and is ready for immediate use.

Usage:
    from core.logging import LOGGER
    LOGGER.info("Your message here")

Log format:
    [LEVEL] Your message
"""

import logging

# Create and configure logger
LOGGER = logging.getLogger("MissionControl")
LOGGER.setLevel(logging.INFO)

# Stream handler with custom formatting
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)

# Attach the handler (only once)
if not LOGGER.handlers:
    LOGGER.addHandler(handler)
