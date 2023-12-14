from django import template
import re

register = template.Library()


@register.filter(name='censor_text')
def censor_text(input_text):
    if not isinstance(input_text, str):
        raise TypeError("Input must be a string")

    censored_words = ["обучение", "грубое_слово", "неприличное"]

    for word in censored_words:
        pattern = re.compile(r'\b' + re.escape(word) + r'\b', re.IGNORECASE)
        input_text = pattern.sub(word[0] + '*' * len(word), input_text)

    return input_text
