QUESTION_LIMIT = 4
HINTS_LIMIT = 2
CORRECTION_FUZZ_RATIO = 85
MESSAGE_TIMEOUT = 15


WRONG_ANS_RESPONSE = (
    "No one answered correctly!", "Better luck next time"
)
WINNER_RESPONSE = (
    "Congratulations {winners_mention} :tada: "
    "{winner_word} have won this quiz game with a grand total of {highest_points} points!"
)


CATEGORIES = {
    "general" : "Test your general knowledge",
    "wikipedia" : "Guess the title of random wikipedia passages.",
    "math" : "Test your knowledge on maths",
    "science" : "Test your scientific knowledge",
    "retro" : "Questions related to retro gaming."
}
RULES = (
    "No cheating and have fun!",
    "Points for each question reduces by 25 after 10s or after a hint. Total time is 30s per question"
)


RANDOM_WIKI_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"
TRIVIA_QUIZ_ICON = (
    "https://raw.githubusercontent.com/python-discord/branding/main/icons/trivia_quiz/trivia-quiz-dist.png"
)