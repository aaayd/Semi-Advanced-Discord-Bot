import asyncio
import random

import discord
from discord.ext.commands import Context
from fuzzywuzzy import fuzz

from main import client
from games.trivia_quiz import _constants
from games.trivia_quiz import _helpers


class Game:
    """Class that contains information and functions about Tic Tac Toe game."""

    def __init__(self, bot: client, ctx: Context, questions: dict, category: str):
        self.bot = bot
        self.ctx = ctx
        self.questions = questions
        self.category = category

        # A variable to store the game status: either running or not running.
        self.over = False
        # A variable to store the person's ID who started the quiz game in a channel.
        self.game_owner = ctx.author.id
        # # A variable to store all player's scores for a the trivia quiz session.
        self.player_scores = {}

    async def play(self) -> None:
        """Start and handle game."""
        # Start game if not running.
        if not self.over:
            self.game_owner = self.ctx.author.id
            start_embed = _helpers.make_start_embed(self.category)

            await self.ctx.send(embed=start_embed)  # send an embed with the rules
            await asyncio.sleep(1)

        # A variable to store the questions which have been sent to the user during the quiz.
        done_question = []
        # A variable to store the number of hints used in a quiz question.
        hint_no = 0
        # A variable to store the answer to a quiz question.
        answer = None

        while not self.over:
            # Exit quiz if number of questions for a round are already sent.
            if len(done_question) > _constants.QUESTION_LIMIT and hint_no == 0:
                await self.ctx.send("The round has ended.")
                await _helpers.declare_winner(self.ctx.channel, self.player_scores)
                self.over = True
                break

            # If no hint has been sent or any time alert. Basically if hint_no = 0  means it is a new question.
            if hint_no == 0:
                # Select a random question which has not been used yet.
                while True:
                    question_dict = random.choice(self.questions)
                    if question_dict["id"] not in done_question:
                        done_question.append(question_dict["id"])
                        break

                q = question_dict["question"]
                answer = question_dict["answer"]

                embed = discord.Embed(
                    title=f"Question #{len(done_question)}",
                    description=q,
                    colour=discord.Colour.gold()
                )
                await self.ctx.send(embed=embed)  # Send question embed.

            # A function to check whether user input is the correct answer(close to the right answer)
            def check(m: discord.Message) -> bool:
                return (
                    m.channel == self.ctx.channel
                    and fuzz.ratio(answer.lower(), m.content.lower()) > _constants.CORRECTION_FUZZ_RATIO
                )

            try:
                msg = await self.bot.wait_for('message', check=check, timeout=_constants.MESSAGE_TIMEOUT)
            except asyncio.TimeoutError:
                # In case of TimeoutError and the game has been stopped, then do nothing.
                if self.over:
                    break

                # if number of hints sent or time alerts sent is less than 2, then send one.
                if hint_no < _constants.HINTS_LIMIT:
                    hint_no += 1
                    if "hints" in question_dict:
                        hints = question_dict["hints"]
                        await self.ctx.send(f"**Hint #{hint_no + 1}\n**{hints[hint_no]}")
                    else:
                        # If hints are not available for the question, then send time alerts
                        await self.ctx.send(
                            f"{(_constants.HINTS_LIMIT * 10) - (hint_no * 10)}s left!"
                        )

                # All hints/time alerts have been sent (`_constants.HINTS_LIMIT`) and
                # the user has still not given a correct answer to the question.
                # Therefore the bot sends the answer and continues ahead.
                else:
                    if self.over:
                        break

                    response = random.choice(_constants.WRONG_ANS_RESPONSE)
                    await self.ctx.send(response)
                    await _helpers.send_answer(self.ctx.channel, question_dict, done_question)
                    await asyncio.sleep(1)

                    # init hint_no = 0 to reset the count.
                    hint_no = 0

                    await _helpers.send_score(self.ctx.channel, self.player_scores)
                    await asyncio.sleep(2)
            else:
                if self.over:
                    break

                # Each hint reduces the total score by 25 points.
                points = (_constants.HINTS_LIMIT + 1) * 25 - 25 * hint_no
                if msg.author in self.player_scores:
                    self.player_scores[msg.author] += points
                else:
                    self.player_scores[msg.author] = points

                # Also updating the overall scoreboard.
                if msg.author in self.player_scores:
                    self.player_scores[msg.author] += points
                else:
                    self.player_scores[msg.author] = points

                hint_no = 0

                await self.ctx.send(f"{msg.author.mention} got the correct answer :tada: {points} points!")
                await _helpers.send_answer(self.ctx.channel, question_dict, done_question)
                await _helpers.send_score(self.ctx.channel, self.player_scores)
                await asyncio.sleep(2)