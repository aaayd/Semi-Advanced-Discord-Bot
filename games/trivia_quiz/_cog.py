import json
import logging
import random
import typing as t

from discord.ext import commands, tasks
from aiohttp import AsyncResolver, ClientSession, TCPConnector
import socket

from main import ROOT, client
from games.trivia_quiz import _constants
from games.trivia_quiz import _helpers
from games.trivia_quiz._game import Game

logger = logging.getLogger(__name__)

try:
    with open(ROOT + "games\\trivia_quiz\\utils\\trivia_quiz.json", encoding="utf8") as json_data:
        QUESTIONS = json.load(json_data)
except:
    with open(ROOT + "games/trivia_quiz/utils/trivia_quiz.json", encoding="utf8") as json_data:
        QUESTIONS = json.load(json_data)




class TriviaQuiz(commands.Cog):
    """A cog for all quiz commands."""

    def __init__(self, bot: client) -> None:
        self.bot = bot
        # Dict to store questions got through wikipedia API
        self.wiki_questions: t.List = []
        self.games: t.Dict = {}
        self.HTTP_SESSION = ClientSession(
            connector=TCPConnector(resolver=AsyncResolver(), family=socket.AF_INET6)
        )


        self.get_wiki_questions.start()

    @tasks.loop(hours=1.0)
    async def get_wiki_questions(self) -> None:
        """Get 10 random questions from wikipedia and format them like the questions in resources/."""
        self.wiki_questions = []
        # trivia_quiz.json follows a pattern, every new category starts with the next century.
        start_id = 201

        while len(self.wiki_questions) != 10:
            async with self.HTTP_SESSION.get(url=_constants.RANDOM_WIKI_URL) as r:
                if r.status != 200:
                    continue

                raw_data = await r.json()

                if not all(c.isalnum() for c in raw_data["title"]):
                    # If the title contains non alphabet/numerical(s) then
                    # don't append it to the question and move on to the next.
                    # Eg. "Knight's night tour" would be skipped.
                    continue

                formatted_data = {
                    "id": start_id,
                    "question": f"Guess the title of the Wikipedia article."
                                f"\n\n"
                                # Sometimes the wikipedia title is given in the extract,
                                # giving away the answers, to remove then, they are replaced
                                # with '[redacted]'.
                                f"{raw_data['extract'].replace(raw_data['title'], '[redacted]')}",
                    "answer": raw_data["title"],
                    "info": raw_data["extract"]
                }
                start_id += 1
                self.wiki_questions.append(formatted_data)

    @commands.group(name="quiz", aliases=["trivia"], invoke_without_command=True)
    async def quiz_game(self, ctx: commands.Context, category: str = None) -> None:
        """
        Start a quiz!
        Questions for the quiz can be selected from the following categories:
        - general : Test your general knowledge. (default)
        - wikipedia : Test your wikipedia knowledge
        """
        # If a game is already running in the channel
        if ctx.channel.id in self.games:
            game = self.games[ctx.channel.id]
            if not game.over:
                await ctx.send(
                    f"Game is already running..."
                    f"do `?quiz stop`"
                )
                return

        # If the inputted category is None, then randomly choose one.
        if category is None:
            category = random.choice(list(_constants.CATEGORIES))

        category = category.lower()

        if category in ("wikipedia", "wiki"):
            questions = self.wiki_questions.copy()
        elif category in _constants.CATEGORIES:
            questions = QUESTIONS[category]
        else:
            # Send embed showing available categories if inputted category is invalid.
            embed = _helpers.category_embed()
            await ctx.send(embed=embed)
            return

        game = Game(self.bot, ctx, questions, category)
        self.games[ctx.channel.id] = game

        await game.play()

    @quiz_game.command(name="stop")
    async def stop_quiz(self, ctx: commands.Context) -> None:
        """
        Stop a quiz game if its running in the channel.
        """
        game = self.games[ctx.channel.id]
        if not game.over:
            if (
                    game.game_owner == ctx.author.id
            ):
                await ctx.send("Quiz stopped.")
                await _helpers.declare_winner(ctx.channel, game.player_scores)
                game.over = True
            else:
                await ctx.send(f"{ctx.author.mention}, you are not authorised to stop this game :ghost:!")
        else:
            await ctx.send("No quiz running.")

    @quiz_game.command(name="leaderboard")
    async def leaderboard(self, ctx: commands.Context) -> None:
        """View everyone's score for this bot session."""
        leaderboard = {}

        for game in self.games.values():
            for player, points in game.player_scores.items():
                if player in leaderboard:
                    leaderboard[player] += points
                else:
                    leaderboard[player] = points

        await _helpers.send_score(ctx.channel, leaderboard)


def setup(bot: client) -> None:
    """Load the cog."""
    bot.add_cog(TriviaQuiz(bot))
