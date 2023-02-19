
import regexparser


def test_boolean_parser():
    parser = regexparser.BooleanParser()
    assert parser.parse('true')


def test_numeric_parser():
    parser = regexparser.NumberParser()
    assert parser.parse('1.1') == 1.1
    assert parser.parse('11') == 11
    assert parser.parse('1,100.01') == 1100.01


def test_portuguese_parser():
    parser = regexparser.PortugueseRulesParser()
    assert parser.parse('Verdadeiro')
    assert not parser.parse('FALSO')
    assert parser.parse('SIM')
    assert not parser.parse('Não')
    assert parser.parse('1,1') == 1.1
    assert parser.parse('-1,1') == -1.1
    assert parser.parse('- 1,1') == -1.1
    assert parser.parse('WÃ¡lson') == 'WÃ¡lson'
    assert parser.parse('1.100,01') == 1100.01


def test_textparser_function():
    assert regexparser.textparse('TRUe', r'^[Tt][Rr][Uu][eE]|[Ff][Aa][Ll][Ss][Ee]$', lambda t, m: eval(t.lower().capitalize()))
    assert regexparser.textparse('1,1', r'^-?\s*\d+[\.,]\d+?$', lambda t, m: eval(t.replace(',', '.'))) == 1.1
    num_parser = regexparser.buildparser(r'^-?\s*\d+[\.,]\d+?$', lambda t, m: eval(t.replace(',', '.')))
    assert num_parser('1,1') == 1.1
