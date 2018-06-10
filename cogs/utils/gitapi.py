"""
Git(Hub|Lab) API utils
"""


def gl_build(endpoint, instance):
    return f'https://{instance}/{endpoint}'


def gh_build(endpoint):
    return f'https://api.github.com/{endpoint}'
