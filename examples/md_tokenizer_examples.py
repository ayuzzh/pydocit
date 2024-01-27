from pydocit.md import Lexer

md = """
#Not a header
# Header 1
## Header 2
### Header 3
#### Header 4
##### Header 5
###### Header 6

** Bold ** ** Again Bold **
* Italics * * Again Italics *

** Bold * Italic in Bold * Bold **
* Italic ** Bold in Italics ** Italics *

| Col 1 | Col 2 | Col 3 |
-------------------------
| R1C1 | R1C2 | R1C3 |
| R2C1 | R2C2 | R3C3 |

Python code
```
def example():
    pass
```
Above is the Python Code in code block

This is text with `single line code`
This is text with **bold** and *italics*

[link text](https://www.google.com)
![alt text](/res/image.png text)
[![alt text of image link](/res/link_image.png text)](https://wikipedia.com)

- Unordered List Item 1
- Unordered List Item 2
- Unordered List Item 3

1. Ordered List Item 1
2. Ordered List Item 2
3. Ordered List Item 3
"""

lexer = Lexer(md)

for i in lexer.tokenize():
    print(repr(i))
