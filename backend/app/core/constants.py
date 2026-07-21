"""
Application-wide constants.

This module contains reusable constants shared across
the application to avoid magic numbers and duplicated values.
"""

# Database String Lengths
NAME_MAX_LENGTH = 100
SLUG_MAX_LENGTH = 120
DESCRIPTION_MAX_LENGTH = 5000
SKU_MAX_LENGTH = 100
COLORWAY_MAX_LENGTH = 255
IMAGE_KEY_MAX_LENGTH = 255

# Pagination
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100