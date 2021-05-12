import re

from generate_tiket import generate

re_pattern_name = re.compile(r'^[\w\-\s]{3,30}$')
re_pattern_email = re.compile(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b')

def handle_name(text, context):
    match = re.match(re_pattern_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False

def handle_email(text, context):
    match = re.findall(re_pattern_email, text)
    if len(match) > 0:
        context['email'] = match[0]
        return True
    else:
        return False

def generate_ticket(text, context):
    return generate(name=context['name'], email=context['email'])


