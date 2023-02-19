# regexparser

`regexparser` helps with the painful situation of having a bunch of small
parsing functions spread for all over the code.

Frequently I have to parse text into `float`, `int` and `date` objects.
The `regexparser.TextParser` class to isolates the parsing task,
it groups the parsing rules in a hierachy of classes that can be easily reused
in different projects.

### Install

    pip install regexparser

`pip` install from github:

	pip install git+https://github.com/wilsonfreitas/regexparser.git

### Using

Create a class that inherits `regexparser.TextParser` and write methods with names starting with `parse`.
These methods must accept 2 arguments after `self`.
These arguments are the `text` that will be parsed and the `re.Match` that is returned by applying the regular expression to the `text`.
The `parse*` methods are called only if its regular expression matches the given text and their regular expressions are set in the methods' doc string.

`regexparser` provides a compact way of applying transformation rules and that rules don't have to be spread out along the code.

The following code shows how to create text parsing rules for a tew text chunks in portuguese.

```python
class PortugueseRulesParser(TextParser):
    # transform Sim and Não into boolean True and False, ignoring case
    def parseBoolean_ptBR(self, text, match):
        r'^(sim|Sim|SIM|n.o|N.o|N.O)$'
        return text[0].lower() == 's'
    # transform Verdadeiro and Falso into boolean True and False, ignoring case
    def parseBoolean_ptBR2(self, text, match):
        r'^(verdadeiro|VERDADEIRO|falso|FALSO|V|F|v|f)$'
        return text[0].lower() == 'v'
    # parses a decimal number
    def parse_number_decimal_ptBR(self, text, match):
        r'^-?\s*\d+,\d+?$'
        text = text.replace(',', '.')
        return eval(text)
    # parses number with thousands
    def parse_number_with_thousands_ptBR(self, text, match):
        r'^-?\s*(\d+\.)+\d+,\d+?$'
        text = text.replace('.', '')
        text = text.replace(',', '.')
        return eval(text)

parser = PortugueseRulesParser()

assert parser.parse('1,1') == 1.1
assert parser.parse('-1,1') == -1.1
assert parser.parse('- 1,1') == -1.1
assert parser.parse('WÃ¡lson') == 'WÃ¡lson'
assert parser.parse('1.100,01') == 1100.01
```
