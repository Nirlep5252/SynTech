"""
These are the custom exceptions that I raise in the project.
"""

from discord.ext.commands import BadArgument


class ItemNotFound(BadArgument):
    def __init__(self, item):
        self.item = item


class NoMoney(BadArgument):
    def __init__(self, current: int, required: int):
        self.current = current
        self.required = required
