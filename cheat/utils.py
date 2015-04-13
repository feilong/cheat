from __future__ import print_function
import os
import sys


def colorize(sheet_content):
    """ Colorizes cheatsheet content if so configured """

    # only colorize if so configured
    if not 'CHEATCOLORS' in os.environ:
        return sheet_content

    # the language to colorize in
    first_line = sheet_content.splitlines()[0]
    if 'python' in first_line:
        lang = 'python'
    else:
        lang = 'bash'

    try:
        from pygments import highlight
        if lang == 'bash':
            from pygments.lexers import BashLexer
            lexer = BashLexer
        elif lang == 'python':
            from pygments.lexers import PythonLexer
            lexer = PythonLexer
        from pygments.formatters import TerminalFormatter

    # if pygments can't load, just return the uncolorized text
    except ImportError:
        return sheet_content

    except Exception:
        return sheet_content

    return highlight(sheet_content, lexer(), TerminalFormatter())


def die(message):
    """ Prints a message to stderr and then terminates """
    warn(message)
    exit(1)


def editor():
    """ Determines the user's preferred editor """
    if 'EDITOR' not in os.environ:
        die(
            'In order to create/edit a cheatsheet you must set your EDITOR '
            'environment variable to your editor\'s path.'
        )

    elif os.environ['EDITOR'] == "":
        die(
          'Your EDITOR environment variable is set to an empty string. It must '
          'be set to your editor\'s path.'
        )

    else:
        return os.environ['EDITOR']


def prompt_yes_or_no(question):
    """ Prompts the user with a yes-or-no question """
    # Support Python 2 and 3 input
    # Default to Python 2's input()
    get_input = raw_input
 
    # If this is Python 3, use input()
    if sys.version_info[:2] >= (3, 0):
        get_input = input

    print(question)
    return get_input('[y/n] ') == 'y'


def warn(message):
    """ Prints a message to stderr """
    print((message), file=sys.stderr)
