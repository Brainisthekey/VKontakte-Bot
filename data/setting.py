from data.config import PGUSER, PGPASSWORD, ip, DATABASEE
INTENTS = [
    {
        "name": 'Дата проведения',
        "tokens": ('когда', 'сколько', 'дата', 'дату'),
        "scenario": None,
        "answer": 'Конференция проводится 15-го апреля в 00:00'
    },
    {
        "name": 'Место провидения',
        "tokens": ('где', 'место', 'локация', 'адресс', 'метро'),
        "scenario": None,
        "answer": 'Конференция пройдёт в MicrosoftTems'
    },
    {
        "name": 'Регестрация',
        "tokens": ('регист', 'регестрация', 'добавь', 'добав'),
        "scenario": 'registration',
        "answer": None
    }
]

SCENARIO = {
    "registration": {
        "first_step": 'step1',
        "steps": {
            "step1": {
                "text": 'If you wand to register, enter your Name, your name will be visible for everyone',
                "failure_text": 'Your name must have a 3-30 length, and hyphen',
                "handler": 'handle_name',
                "next_step": 'step2'
            },
            "step2": {
                "text": 'Enter your email, we will send all information on email',
                "failure_text": 'Its not a valid adress',
                "handler": 'handle_email',
                "next_step": 'step3'
                },
            "step3": {
                "text": 'Thanks for registarion {name}! We will send an email on this adress {email} Your ticket is here!',
                "image": 'generate_ticket',
                "failure_text": None,
                "handler": None,
                "next_step": None
            }
        }
    }
}

DEFAULT_ANSWER = "I don't know what you want from me" \
                  "I can tell you when and where we will have a meating"

DB_CONFIG = dict(
    provider='postgres',
    user=PGUSER,
    password=PGPASSWORD,
    host=ip,
    #database=DATABASEE
)