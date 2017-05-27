PURPLE = '\033[95m'
CYAN = '\033[96m'
DARKCYAN = '\033[36m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'
END = '\033[0m'


def pretty_print(colors, text, cr=True):
    """
    Print text to stdout

    Arguments:
        colors (str[]): An array of colors (such as those defined above)
        text (str): The text to colorize
        cr (boolean : True): Whether to include carriage returns or not

    Returns:
        None
    """
    if type(colors) == list:
        pre = ''.join(colors)
    else:
        pre = colors

    if cr:
        print(pre + text + END)
    else:
        print(pre + text + END, end="")


def pretty_format(colors, text):
    """
    Performs nesting of text inside coloration terminals

    Arguments:
        colors (str[]): An array of colors (such as those defined above)
        text (str): The text to colorize

    Returns:
        str: Formatted string, nested in formatters
    """
    if type(colors) == list:
        pre = ''.join(colors)
    else:
        pre = colors
    return(pre + text + END)
