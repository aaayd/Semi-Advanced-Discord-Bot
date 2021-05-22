from bot import client


def setup(client: client) -> None:
    """Set up the Trivia Questions Cog."""
    from ._cog import TriviaQuiz

    client.add_cog(TriviaQuiz(client))
