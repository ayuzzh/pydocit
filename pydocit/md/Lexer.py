import re


class Token:
    def __init__(self, value: str, start: int, end: int):
        self.val = value
        self.start = start
        self.end = end

    def __repr__(self):
        return f'{self.name}("{self.val}", {self.start}, {self.end})'

    def __str__(self):
        return f"{self.name}"


class Heading1(Token):
    re_pattern = re.compile(r"^# +(.+)", re.MULTILINE)
    name = "Heading1"


class Heading2(Token):
    re_pattern = re.compile(r"^#{2} +(.+)", re.MULTILINE)
    name = "Heading2"


class Heading3(Token):
    re_pattern = re.compile(r"^#{3} +(.+)", re.MULTILINE)
    name = "Heading3"


class Heading4(Token):
    re_pattern = re.compile(r"^#{4} +(.+)", re.MULTILINE)
    name = "Heading4"


class Heading5(Token):
    re_pattern = re.compile(r"^#{5} +(.+)", re.MULTILINE)
    name = "Heading5"


class Heading6(Token):
    re_pattern = re.compile(r"^#{6} +(.+)", re.MULTILINE)
    name = "Heading6"


class PlainText(Token):
    re_pattern = re.compile(r"^(?!(- )|(\d+\. ))(?P<text>.+)", re.MULTILINE)
    name = "PlainText"


class BoldText(Token):
    re_pattern = re.compile(
        r"(?<!\\)\*\*(.+?)(?!\\)\*(?!\\)\*", re.DOTALL | re.MULTILINE
    )
    name = "BoldText"


class ItalicText(Token):
    re_pattern = re.compile(
        r"(?<!\*)(?<!\\)\*(.+?)(?<!\\)\*(?!\*)", re.DOTALL | re.MULTILINE
    )
    name = "ItalicText"


class Link(Token):
    re_pattern = re.compile(
        r"(?<!!)(?<!\\)\[(?<!!)(?<!\\)(?P<text>.+?)(?<!\\)](?<!\\)\((?P<link>\S+)(?<!\\)\)"
    )

    def __init__(self, text, link, start, end):
        self.name = "Link"
        self.val = text
        self.link = link
        self.start = start
        self.end = end

        super().__init__(self.val, self.start, self.end)

    def __repr__(self):
        return f'{self.name}("{self.val}", "{self.link}", {self.start}, {self.end})'


class MultilineCode(Token):
    re_pattern = re.compile(r"^(?<!\\)`{3}(.+?)(?<!\\)`{3}", re.DOTALL | re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "MultilineCode"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.val, self.start, self.end)


class SingleLineCode(Token):
    re_pattern = re.compile(r"(?<!`)(?<!\\)`(?!`)(.+?)(?<!\\)`(?!`)")
    name = "SinglelineCode"


class TableHeader(Token):
    re_pattern = re.compile(r"^(?!\\)\| +(.+) +\| *\n(?<!\\)-{3,}$", re.MULTILINE)
    name = "TableHeader"


class TableRow(Token):
    re_pattern = re.compile(r"^(?<!\\)\| +(.+) +\| *", re.MULTILINE)
    name = "TableRow"


class UnorderedListItem(Token):
    re_pattern = re.compile(r"^[\t ]*-[\t ]+(.+)", re.MULTILINE)
    name = "UnorderedListItem"


class OrderedListItem(Token):
    re_pattern = re.compile(r"^[\t ]*\d+\.[\t ]+(.+)", re.MULTILINE)
    name = "OrderedListItem"


class Image(Token):
    re_pattern = re.compile(
        r"(?<!\\)!(?<!\\)\[(?P<alt>.+?)(?<!\\)](?<!\\)\((?P<link>\S+)[\t ]+(?P<text>.+?)(?<!\\)\)",
        re.MULTILINE,
    )

    def __init__(self, alt, link, text, start, end):
        self.name = "Image"

        self.alt = alt
        self.link = link
        self.text = text

        self.start = start
        self.end = end

        super().__init__(self.link, self.start, self.end)

    def __repr__(self):
        return f'{self.name}("{self.alt}", "{self.link}", {self.text}, {self.start}, {self.end})'


class NewLine(Token):
    re_pattern = re.compile(r"^\n", re.MULTILINE)

    def __init__(self, pos):
        self.name = "NewLine"
        self.start = pos
        self.end = pos

        super().__init__("\n", self.start, self.end)

    def __repr__(self):
        return f"{self.name}({self.start})"


class Lexer:
    """
    Convert MD content into tokens

    The tokenizing occurs in order
    1. Multiline_Code
    2. Singleline_Code
    3. Heading1
    4. Heading2
    5. Heading3
    6. Heading4
    7. Heading5
    8. Heading6
    9. Table header
    10. Table Row
    11. Bold_Text
    12. Italic_Text
    13. Image
    14. Link
    15. Plain_Text
    """

    def __init__(self, feed):
        self.feed = feed

        self.tokens = []
        self.ignore = []

        self.table_header_start_index = []
        self.rows = []
        self.multiline_code = []

    def tokenize(self):
        # tokenize_singleline_code is tokenized before headings
        # so that singleline code can be included in headings
        if self.tokens:
            return self.tokens

        self.tokenize_multiline_code()
        self.tokenize_singleline_code()

        self.tokenize_h1()
        self.tokenize_h2()
        self.tokenize_h3()
        self.tokenize_h4()
        self.tokenize_h5()
        self.tokenize_h6()

        self.tokenize_table_header()
        self.tokenize_table_row()

        self.tokenize_unordered_list()
        self.tokenize_ordered_list()

        self.tokenize_bold_text()
        self.tokenize_italic_text()

        self.tokenize_images()
        self.tokenize_links()

        self.tokenize_newline()

        self.tokenize_text()

        return self.tokens

    def tokenize_multiline_code(self):
        for match in MultilineCode.re_pattern.finditer(self.feed):
            tok = MultilineCode(match.group(1), match.start(), match.end())
            self.add_tok(tok)

            self.ignore.append((match.start(), match.end()))
            self.multiline_code.append((match.start(), match.end()))

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

    def tokenize_table_header(self):
        for match in TableHeader.re_pattern.finditer(self.feed):
            if not self.check_if_in_ignore(TableHeader, match.start(), match.end()):
                self.add_tok(TableHeader(match.group(1), match.start(), match.end()))
                self.table_header_start_index.append(match.start())

    def tokenize_table_row(self):
        for match in TableRow.re_pattern.finditer(self.feed):
            if not self.check_if_in_ignore(TableRow, match.start(), match.end()):
                if not match.start() in self.table_header_start_index:
                    self.add_tok(TableRow(match.group(1), match.start(), match.end()))
                    self.rows.append(match.start())

    def tokenize_unordered_list(self):
        for match in UnorderedListItem.re_pattern.finditer(self.feed):
            if not self.check_if_in_ignore(
                UnorderedListItem, match.start(), match.end()
            ):
                self.add_tok(
                    UnorderedListItem(match.group(1), match.start(), match.end())
                )

    def tokenize_ordered_list(self):
        for match in OrderedListItem.re_pattern.finditer(self.feed):
            if not self.check_if_in_ignore(OrderedListItem, match.start(), match.end()):
                self.add_tok(
                    OrderedListItem(match.group(1), match.start(), match.end())
                )

    def tokenize_images(self):
        for match in Image.re_pattern.finditer(self.feed):
            if not self.check_if_in_ignore(Image, match.start(), match.end()):
                self.add_tok(
                    Image(
                        match.group("alt"),
                        match.group("link"),
                        match.group("text"),
                        match.start(),
                        match.end(),
                    )
                )

    def tokenize_newline(self):
        for match in NewLine.re_pattern.finditer(self.feed):
            if not self.check_if_in_ignore("NewLine", match.start(), match.end()):
                self.add_tok(NewLine(match.start()))

    def tokenize_text(self):
        ignore = self.table_header_start_index + self.rows + [m[0] for m in self.ignore]

        for match in PlainText.re_pattern.finditer(self.feed):
            if match.start() not in ignore:
                if not self.check_if_in_mlc_ignore(match.start(), match.end()):
                    if not re.match(r"^-{3,}$", match.group("text")):
                        self.add_tok(
                            PlainText(match.group("text"), match.start(), match.end())
                        )

    def check_if_in_ignore(self, tok_type, start, end):
        for s, e in self.ignore:
            if start > s and e > end:
                if tok_type in ["BoldText", "ItalicText"]:
                    return False
                return True
        return False

    def check_if_in_mlc_ignore(self, start, end):
        return any(s <= start < e and s < end <= e for s, e in self.ignore)

    def add_tok(self, tok):
        for index, value in enumerate(self.tokens):
            if not tok.start > value.start:
                self.tokens.insert(index, tok)
                return
        self.tokens.append(tok)
