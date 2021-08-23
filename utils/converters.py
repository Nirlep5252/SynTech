"""
These are the converters used to convert the user input to the correct type.
"""

from discord.ext.commands import Context, Converter
from utils.exceptions import ItemNotFound
from utils.constants import items
from utils.classes import Item


class ItemConverter(Converter):
    async def convert(self, ctx: Context, argument: str) -> Item:
        if argument.lower() in items:
            item_dict = items[argument.lower()]
            return Item(
                prize=item_dict["prize"],
                name=argument.lower(),
                description=item_dict["description"],
                emoji=item_dict["emoji"],
            )
        else:
            raise ItemNotFound(argument)
