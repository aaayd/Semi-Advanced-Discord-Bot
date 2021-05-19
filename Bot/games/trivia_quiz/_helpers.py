import discord

from Bot.games.trivia_quiz import _constants

__all__ = (
    'category_embed',
    'declare_winner',
    'make_start_embed',
    'send_answer',
    'send_score'
)


def make_start_embed(category: str) -> discord.Embed:
    """Generate a starting/introduction embed for the quiz."""
    rules = "\n".join([f"`{index}`: {rule}" for index, rule in enumerate(_constants.RULES, start=1)])

    start_embed = discord.Embed(
        title="Quiz game Starting!!",
        description=(
            "Each game consists of 5 questions.\n"
            f"**Rules :**\n{rules}"
            f"\n **Category** : {category}"
        ),
        colour=discord.Colour.red()
    )
    start_embed.set_thumbnail(url=_constants.TRIVIA_QUIZ_ICON)

    return start_embed


async def send_score(channel: discord.TextChannel, player_data: dict) -> None:
    """A function which sends the score."""
    if len(player_data) == 0:
        await channel.send("No one has made it onto the leaderboard yet.")
        return

    embed = discord.Embed(
        title="Score Board",
        description="",
        colour=discord.Colour.blue()
    )
    embed.set_thumbnail(url=_constants.TRIVIA_QUIZ_ICON)

    sorted_dict = sorted(player_data.items(), key=lambda a: a[1], reverse=True)
    for item in sorted_dict:
        embed.description += f"{item[0]} : {item[1]}\n"

    await channel.send(embed=embed)


async def declare_winner(channel: discord.TextChannel, player_data: dict) -> None:
    """Announce the winner of the quiz in the game channel."""
    if player_data:
        highest_points = max(list(player_data.values()))
        no_of_winners = list(player_data.values()).count(highest_points)

        # Check if more than 1 player has highest points.
        if no_of_winners > 1:
            word = "You guys"
            winners = []
            points_copy = list(player_data.values()).copy()

            for _ in range(no_of_winners):
                index = points_copy.index(highest_points)
                winners.append(list(player_data)[index])
                points_copy[index] = 0

            winners_mention = " ".join(winner.mention for winner in winners)
        else:
            word = "You"
            author_index = list(player_data.values()).index(highest_points)
            winner = list(player_data)[author_index]
            winners_mention = winner.mention

        await channel.send(
            _constants.WINNER_RESPONSE.format(
                winners_mention=winners_mention,
                winner_word=word,
                highest_points=highest_points
            )
        )


def category_embed() -> discord.Embed:
    """Build an embed showing all available trivia categories."""
    embed = discord.Embed(
        title="The available question categories are:",
        description="",
        colour=discord.Colour.blue()
    )
    embed.set_footer(text="If a category is not chosen, a random one will be selected.")

    for cat, description in _constants.CATEGORIES.items():
        embed.description += f"**- {cat.capitalize()}**\n{description.capitalize()}\n"

    return embed


async def send_answer(channel: discord.TextChannel, question_dict: dict, done_question: list) -> None:
    """Send the correct answer of a question to the game channel."""
    answer = question_dict["answer"]
    info = question_dict["info"]
    embed = discord.Embed(
        title=f"The correct answer is **{answer}**\n",
        description="",
        color=discord.Colour.red()
    )

    if info != "":
        embed.description += f"**Information**\n{info}\n\n"

    embed.description += (
        f"Let's move to the next question."
        f"\nRemaining questions: {_constants.QUESTION_LIMIT - len(done_question)}"
    )
    await channel.send(embed=embed)