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
    re_pattern = re.compile(r"(?<!!)\[(?<!!)(?P<text>.+?)]\((?P<link>\S+)\)")

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


class TableHeader(Token):
    re_pattern = re.compile(r"^\| +(.+) +\| *\n-{3,}", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "TableHeader"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class TableRow(Token):
    re_pattern = re.compile(r"^\| +(.+) +\| *", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "TableRow"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class UnorderedListItem(Token):
    re_pattern = re.compile(r"^[\t ]*\*[\t ]+(.+)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "UnorderedListItem"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class OrderedListItem(Token):
    re_pattern = re.compile(r"^[\t ]*\d+\.[\t ]+(.+)", re.MULTILINE)

    def __init__(self, value, start, end):
        self.name = "OrderedListItem"
        self.val = value
        self.start = start
        self.end = end

        super().__init__(self.name, self.val, self.start, self.end)


class Image(Token):
    re_pattern = re.compile(
        r"!\[(?P<alt>.+?)]\((?P<link>\S+)[\t ]+(?P<text>.+?)\)", re.MULTILINE
    )

    def __init__(self, alt, link, text, start, end):
        self.name = "Image"

        self.alt = alt
        self.link = link
        self.text = text

        self.start = start
        self.end = end

        super().__init__(self.name, self.link, self.start, self.end)

    def __repr__(self):
        return f'{self.name}("{self.alt}", "{self.link}", {self.text}, {self.start}, {self.end})'


class ImageLink:
    re_pattern = re.compile(
        r"\[!\[(?P<alt>.+?)]\((?P<image_link>.+?)[\t ]+(?P<text>.+?)\)]\((?P<link>.+?)\)"
    )

    def __init__(self, alt, image_link, text, link, start, end):
        self.name = "ImageLink"

        self.alt = alt
        self.image_link = image_link
        self.link = link
        self.text = text

        self.start = start
        self.end = end

        super().__init__(self.name, self.link, self.start, self.end)

    def __repr__(self):
        return f'{self.name}("{self.alt}", "{self.image_link}", "{self.link}", {self.text}, {self.start}, {self.end})'


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
    9. Table header
    10. Table Row
    11. Bold_Text -> Undergoes parsing to check if contains any Links or Italic_Text
    12. Italic_Text -> Undergoes parsing to check if contains any Links
    13. Image
    14. Link
    15. Image_Links
    16. Plain_Text -> Undergoes parsing to check if contains any Links

    ### TODO
    - Images
    """

    def __init__(self, feed):
        self.original_feed = feed

        # It may be altered for preventing matching clashes
        self.feed = self.original_feed

        self.tokens = []
        self.ignore = []

        self.table_header_start_index = []

    def tokenize(self):
        # tokenize_singleline_code is tokenized before headings
        # so that singleline code can be included in headings
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
        self.tokenize_image_links()

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

    def tokenize_unordered_list(self):
        for match in UnorderedListItem.re_pattern.finditer(self.feed):
            if not self.check_if_in_ignore(
                UnorderedListItem, match.start(), match.end()
            ):
                self.add_tok(
                    UnorderedListItem(match.group(1), match.start(), match.end())
                )
                # For preventing the clash between italic matching
                # and unordered list matching
                self.alter_feed(match.start(), "-")

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

    def tokenize_image_links(self):
        for match in Image.re_pattern.finditer(self.feed):
            if not self.check_if_in_ignore(ImageLink, match.start(), match.end()):
                self.add_tok(
                    ImageLink(
                        match.group("alt"),
                        match.group("image_link"),
                        match.group("link"),
                        match.group("text"),
                        match.start(),
                        match.end(),
                    )
                )

    def check_if_in_ignore(self, tok_type, start, end):
        for s, e in self.ignore:
            if start > s and e > end:
                if tok_type in ["BoldText", "ItalicText"]:
                    return False
                return True
        return False

    def alter_feed(self, index, val):
        feed_list = list(self.feed)
        feed_list[index] = val
        self.feed = "".join(feed_list)

    def add_tok(self, tok):
        for index, value in enumerate(self.tokens):
            if not tok.start > value.start:
                self.tokens.insert(index, tok)
                return
        self.tokens.append(tok)
