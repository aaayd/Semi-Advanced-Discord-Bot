from discord import Embed

def embed_error(message):
    return Embed(
        description=f":x: {message}", 
        color=0xFF0000
    )


class MissingArgument(Exception):
    def __init__(self, missing_argument, command_description, message="Missing keyword: ", ):
        self.missing_argument = f"`{missing_argument}`"
        self.command_description = f"`{command_description}`"

        self.missing_argument += f"\nCommand Usage: {self.command_description}"
        self.message = message + self.missing_argument

    def __str__(self):
        return self.message