import re


class Token:
    def __init__(self, name: str, value: str, start: int, end: int):
        self.name = name
        self.val = value
        self.start = start
        self.end = end

    def __repr__(self):
        return f'{self.name}("{self.val}", {self.start}, {self.end})'

    def __str__(self):
        return f"{self.name}"


class Heading1(Token):
    re_pattern = re.compile(r"^# +(.+)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "Heading1"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class Heading2(Token):
    re_pattern = re.compile(r"^#{2} +(.+)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "Heading2"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class Heading3(Token):
    re_pattern = re.compile(r"^#{3} +(.+)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "Heading3"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class Heading4(Token):
    re_pattern = re.compile(r"^#{4} +(.+)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "Heading4"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class Heading5(Token):
    re_pattern = re.compile(r"^#{5} +(.+)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "Heading5"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class Heading6(Token):
    re_pattern = re.compile(r"^#{6} +(.+)", re.MULTILINE)

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
    re_pattern = re.compile(r"\*\*(.+?)\*\*", re.DOTALL | re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "BoldText"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class ItalicText(Token):
    re_pattern = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")

    def __init__(self, value, start, end):
        self.name = "ItalicText"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class Link(Token):
    re_pattern = re.compile(r"\[(?P<text>.+?)]\((?P<link>.+?)\)")

    def __init__(self, text, link, start, end):
        self.name = "Link"
        self.val = text
        self.link = link
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)

    def __repr__(self):
        return f'{self.name}("{self.val}", "{self.link}", {self.start}, {self.end})'


class MultilineCode(Token):
    re_pattern = re.compile(r"^`{3}(.+?)`{3}", re.DOTALL | re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "MultilineCode"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class SingleLineCode(Token):
    re_pattern = re.compile(r"(?<!`)`(?!`)(.+?)(?<!`)`(?!`)")

    def __init__(self, value, start, end):
        self.name = "SinglelineCode"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class Lexer:
    """
    This class parses the md markup text and converts in into
    a simple tree which can be used to converted into html or pdf
    according to the requirement.

    The parsing occurs in order
    1. Multiline_Code
    2. Singleline_Code
    3. Heading1
    4. Heading2
    5. Heading3
    6. Heading4
    7. Heading5
    8. Heading6
    9. Bold_Text -> Undergoes parsing to check if contains any Links or Italic_Text
    10. Italic_Text -> Undergoes parsing to check if contains any Links
    11. Link
    12. Plain_Text -> Undergoes parsing to check if contains any Links

    ### TODO
    - Lists
    - Tables
    - Images
    """

    def __init__(self, feed):
        self.feed = feed
        self.tokens = []
        self.ignore = []

    def tokenize(self):
        self.tokenize_multiline_code()
        self.tokenize_singleline_code()
        self.tokenize_h1()
        self.tokenize_h2()
        self.tokenize_h3()
        self.tokenize_h4()
        self.tokenize_h5()
        self.tokenize_h6()
        self.tokenize_bold_text()
        self.tokenize_italic_text()
        self.tokenize_links()

        return self.tokens

    def tokenize_multiline_code(self):
        for match in MultilineCode.re_pattern.finditer(self.feed):
            tok = MultilineCode(match.group(1), match.start(), match.end())
            self.add_tok(tok)

            self.ignore.append((match.start(), match.end()))

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

    def tokenize_bold_text(self):
        for match in BoldText.re_pattern.finditer(self.feed):
            if not self.check_if_in_ignore(BoldText, match.start(), match.end()):
                self.add_tok(BoldText(match.group(1), match.start(), match.end()))

    def tokenize_italic_text(self):
        for match in ItalicText.re_pattern.finditer(self.feed):
            if not self.check_if_in_ignore(ItalicText, match.start(), match.end()):
                self.add_tok(ItalicText(match.group(1), match.start(), match.end()))

    def tokenize_links(self):
        for match in Link.re_pattern.finditer(self.feed):
            if not self.check_if_in_ignore(Link, match.start(), match.end()):
                self.add_tok(
                    Link(
                        match.group(1),
                        match.group(2),
                        match.start(),
                        match.end(),
                    )
                )

    def tokenize_singleline_code(self):
        for match in SingleLineCode.re_pattern.finditer(self.feed):
            if not self.check_if_in_ignore(SingleLineCode, match.start(), match.end()):
                self.add_tok(SingleLineCode(match.group(1), match.start(), match.end()))

    def check_if_in_ignore(self, tok_type, start, end):
        for s, e in self.ignore:
            if start > s and e > end:
                if tok_type in ["BoldText", "ItalicText"]:
                    return False
                return True
        return False

    def add_tok(self, tok):
        for index, value in enumerate(self.tokens):
            if not tok.start > value.start:
                self.tokens.insert(index, tok)
                return
        self.tokens.append(tok)
