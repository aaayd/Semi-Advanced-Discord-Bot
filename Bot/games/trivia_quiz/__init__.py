from bot import bot


def setup(bot: bot) -> None:
    """Set up the Trivia Questions Cog."""
    from ._cog import TriviaQuiz

    bot.add_cog(TriviaQuiz(bot))
