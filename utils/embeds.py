from discord import Embed
from config import ERROR_COLOR, MAIN_COLOR


def error_embed(title: str, description: str) -> Embed:
    return Embed(
        title=title,
        description=description,
        color=ERROR_COLOR
    )


def success_embed(title: str, description: str) -> Embed:
    return Embed(
        title=title,
        description=description,
        color=MAIN_COLOR
    )


def custom_embed(title: str, description: str) -> Embed:
    return Embed(
        title=title,
        description=description,
        color=MAIN_COLOR
    )
