## textparser

Frequently I have to parse text into `float`, `int` and `date`, for just a few examples.
I've written that class to isolate the parsing task, instead of getting it spreaded all over the code.
This is a fairly simple class which helps me keeping my code clean.

Simply create a class inheriting TextParser define the parsing rules as the following and in the end call the method parse.

Examples:

```python
class PortugueseRulesParser(TextParser):
    def parseBoolean_ptBR(self, text, match):
        r'^(sim|Sim|SIM|n.o|N.o|N.O)$'
        return text[0].lower() == 's'
    def parseBoolean_ptBR2(self, text, match):
        r'^(verdadeiro|VERDADEIRO|falso|FALSO|V|F|v|f)$'
        return text[0].lower() == 'v'
    def parse_number_with_thousands_ptBR(self, text, match):
        r'^-?\s*(\d+\.)+\d+,\d+?$'
        text = text.replace('.', '')
        text = text.replace(',', '.')
        return eval(text)
    def parse_number_decimal_ptBR(self, text, match):
        r'^-?\s*\d+,\d+?$'
        text = text.replace(',', '.')
        return eval(text)
parser = PortugueseRulesParser()
assert parser.parse('1,1') == 1.1
assert parser.parse('-1,1') == -1.1
assert parser.parse('- 1,1') == -1.1
assert parser.parse('WÃ¡lson') == 'WÃ¡lson'
assert parser.parse('1.100,01') == 1100.01
```

I copied the idea of using a regular expression in `__doc__` from [PLY](http://www.dabeaz.com/ply/).


## Install

`pip` install from github with the following command.

	pip install git+https://github.com/wilsonfreitas/textparser.git

