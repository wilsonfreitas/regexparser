import re
from types import MethodType

from typing import List, Any, Callable


class TextParser:
    """
    TextParser class

    Builds parsers based on regular expressions.
    The regular expression, used to match the text pattern, is specified in the
    method's __doc__ attribute.
    The name of these *parser methods* must start with `parser`.

    The parser class inherits TextParser and implements the parser methods
    defining the regular expression in the method's __doc__.

    The parser method has two arguments, the first is the given text that is
    parsed and the second is one instance of the re.Match class.
    The regular expression attributes can be accessed in this argument.
    The parser method is called once the regular expression returns a valid
    Match object.

    If one regular expression matches the given text, the method associated
    to that regular expression is executed, the given text is parsed according to its
    implementation and the parsed value is returned.
    Otherwise, the passed text is returned without changes.

    Examples
    --------
    Creat a class to parse integers.

    >>> class IntParser(TextParser):
    >>>     def parseInteger(self, text, match):
    >>>         r'^-?\\s*\\d+$'
    >>>         return eval(text)

    Instanciate and call the parse method to convert the given text.

    >>> parser = IntParser()
    >>> parser.parse('1')
    1
    >>> parser.parse('a')
    'a'
    """
    def __init__(self):
        self.parsers = self.__createMethodAnalyzers()
        
    def __createMethodAnalyzers(self) -> List:
        pairs = []
        for methodName in dir(self):
            method = getattr(self, methodName)
            if methodName.startswith('parse') and type(method) is MethodType and method.__doc__:
                pairs.append(buildparser(method.__doc__, method))
        return pairs
    
    def parse(self, text: str) -> Any:
        for parser in self.parsers:
            val = parser(text)
            if val != text:
                return val
        return self.parseText(text)
    
    def parseText(self, text: str) -> str:
        return text


class BooleanParser(TextParser):
    """
    BooleanParser class

    Convert "TRUE" or "FALSE" (with any case combination) to boolean objects.

    Examples
    --------
    >>> parser.parse('True')
    True
    >>> parser.parse('FALSE')
    False
    """
    def parseBoolean(self, text: str, match: re.Match) -> bool:
        r'^[Tt][Rr][Uu][eE]|[Ff][Aa][Ll][Ss][Ee]$'
        return eval(text.lower().capitalize())


class NumberParser(TextParser):
    """
    NumberParser class

    Convert text with numbers to int and float objects.

    Examples
    --------
    >>> parser.parse('1')
    1
    >>> parser.parse('- 1.1')
    -1.1
    >>> parser.parse('1,000.1')
    1000.1
    """
    def parseInteger(self, text: str, match: re.Match) -> int:
        r'^-?\s*\d+$'
        return eval(text)
    
    def parse_number_decimal(self, text: str, match: re.Match) -> float:
        r'^-?\s*\d+\.\d+?$'
        return eval(text)
    
    def parse_number_with_thousands(self, text: str, match: re.Match) -> float:
        r'^-?\s*(\d+[,])+\d+[\.]\d+?$'
        text = text.replace(',', '')
        return eval(text)


class PortugueseRulesParser(TextParser):
    """
    PortugueseRulesParser class

    Convert text to float and boolean according to Brazilian Portuguese conventions.

    Examples
    --------
    >>> parser.parse('1,1')
    1,1
    >>> parser.parse('- 1.000,1')
    -1000.1
    >>> parser.parse('Sim')
    True
    >>> parser.parse('Não')
    False
    """
    def parseBoolean_ptBR(self, text: str, match: re.Match) -> bool:
        r'^(sim|Sim|SIM|n.o|N.o|N.O)$'
        return text[0].lower() == 's'

    def parseBoolean_ptBR2(self, text: str, match: re.Match) -> bool:
        r'^(verdadeiro|VERDADEIRO|falso|FALSO|V|F|v|f)$'
        return text[0].lower() == 'v'

    def parse_number_with_thousands_ptBR(self, text: str, match: re.Match) -> float:
        r'^-?\s*(\d+\.)+\d+,\d+?$'
        text = text.replace('.', '')
        text = text.replace(',', '.')
        return eval(text)

    def parse_number_decimal_ptBR(self, text: str, match: re.Match) -> float:
        r'^-?\s*\d+,\d+?$'
        text = text.replace(',', '.')
        return eval(text)


def textparse(text: str, regex: str, func: Callable[[str, re.Match], Any]) -> Any:
    """
    Parses the argument text with the function func once it matches the 
    regular expression regex.

    Parameters
    ----------
    text: str
        Given text to be parsed.
    regex: str
        Regular expression to match the desired pattern.
    func: function
        Function that parses the given text once it matches the regular expression.

    Returns
    -------
    Any
        Returns the parsed object as result of the parsing.

    Examples
    --------
    >>> textparser.textparse('TRUe', r'^[Tt][Rr][Uu][eE]|[Ff][Aa][Ll][Ss][Ee]$', lambda t, m: eval(t.lower().capitalize()))
    True
    >>> textparser.textparse('1,1', r'^-?\\s*\\d+[\\.,]\\d+?$', lambda t, m: eval(t.replace(',', '.')))
    1.1
    """
    parser = buildparser(regex, func)
    return parser(text)


def buildparser(regex: str, func: Callable[[str, re.Match], Any]) -> Callable[[str], Any]:
    """
    Builds a parser that parses a given text according to regex and func.

    Parameters
    ----------
    regex: str
        Regular expression to match the desired pattern.
    func: function
        Function that parses the given text once it matches the regular expression.

    Returns
    -------
    Callable[[str]]
        Returns a callable object that receives the text to be parsed and returns
        the result of the parsing.

    Examples
    --------
    >>> num_parser = textparser.buildparser(r'^-?\\s*\\d+[\\.,]\\d+?$', lambda t, m: eval(t.replace(',', '.')))
    >>> num_parser('1.1')
    1.1
    """
    _regex = re.compile(regex)
    def _func(text):
        match = _regex.match(text)
        return func(text, match) if match else text
    return _func


class GenericParser(NumberParser, BooleanParser):
    pass
