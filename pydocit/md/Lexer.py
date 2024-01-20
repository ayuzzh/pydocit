import re


class Token:
    def __init__(self, name: str, value: str, start: int, end: int):
        self.name = name
        self.val = value
        self.start = start
        self.end = end

    def __repr__(self):
        return f'{self.name}("{self.val}", {self.start}, {self.end})'


class Heading1(Token):
    re_pattern = re.compile(r"^(?:#)(?: )+(.+)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "Heading1"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class Heading2(Token):
    re_pattern = re.compile(r"^(?:#){2}(?: )+(.+)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "Heading2"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class Heading3(Token):
    re_pattern = re.compile(r"^(?:#){3}(?: )+(.+)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "Heading3"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class Heading4(Token):
    re_pattern = re.compile(r"^(?:#){4}(?: )+(.+)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "Heading4"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class Heading5(Token):
    re_pattern = re.compile(r"^(?:#){5}(?: )+(.+)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "Heading5"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class Heading6(Token):
    re_pattern = re.compile(r"^(?:#){6}(?: )+(.+)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "Heading6"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class PlainText(Token):
    def __init__(self, value, start, end):
        self.name = "PlainText"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class BoldText(Token):
    re_pattern = re.compile(r"(\*\*.+\*\*)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "BoldText"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class ItalicText(Token):
    re_pattern = re.compile(r"(?!\*)(\*.+\*)(?!\*)")

    def __init__(self, value, start, end):
        self.name = "ItalicText"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class MDParser:
    """
    This class parses the md markup text and converts in into
    a simple tree which can be used to converted into html or pdf
    according to the requirement.

    The parsing occurs in order
    1. Heading1
    2. Heading2
    3. Heading3
    4. Heading4
    5. Heading5
    6. Heading6
    7. Bold_Text -> Undergoes parsing to check if contains any Links or Italic_Text
    8. Italic_Text -> Undergoes parsing to check if contains any Links
    9. Plain_Text -> Undergoes parsing to check if contains any Links

    ### TODO
    - Lists
    - Tables
    - Links
    - Images
    - Bold text
    - Italic Text
    """

    def __init__(self, feed):
        self.feed = feed
        self.tokens = []
        self.ignore = []

    def tokenize(self):
        self.tokenize_h1()
        self.tokenize_h2()
        self.tokenize_h3()
        self.tokenize_h4()
        self.tokenize_h5()
        self.tokenize_h6()

        return self.tokens

    def tokenize_h1(self):
        for match in Heading1.re_pattern.finditer(self.feed):
            tok = Heading1(match.group(1), match.start(), match.end())
            self.add_tok(tok)

            self.ignore.append((match.start(), match.end()))

    def tokenize_h2(self):
        for match in Heading2.re_pattern.finditer(self.feed):
            tok = Heading2(match.group(1), match.start(), match.end())
            self.add_tok(tok)

            self.ignore.append((match.start(), match.end()))

    def tokenize_h3(self):
        for match in Heading3.re_pattern.finditer(self.feed):
            tok = Heading3(match.group(1), match.start(), match.end())
            self.add_tok(tok)

            self.ignore.append((match.start(), match.end()))

    def tokenize_h4(self):
        for match in Heading4.re_pattern.finditer(self.feed):
            tok = Heading4(match.group(1), match.start(), match.end())
            self.add_tok(tok)

            self.ignore.append((match.start(), match.end()))

    def tokenize_h5(self):
        for match in Heading5.re_pattern.finditer(self.feed):
            tok = Heading5(match.group(1), match.start(), match.end())
            self.add_tok(tok)

            self.ignore.append((match.start(), match.end()))

    def tokenize_h6(self):
        for match in Heading6.re_pattern.finditer(self.feed):
            tok = Heading6(match.group(1), match.start(), match.end())
            self.add_tok(tok)

            self.ignore.append((match.start(), match.end()))

    def add_tok(self, tok):
        for index, value in enumerate(self.tokens):
            if not tok.start > value.start:
                self.tokens.insert(index, tok)
                return
        self.tokens.append(tok)
