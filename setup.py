#!/usr/bin/env python

from distutils.core import setup

setup(name="textparser",
      version="0.1.0",
      py_modules=['textparser'],
      author='Wilson Freitas',
      author_email='wilson.freitas@gmail.com',
      description='Simple parser for small chuncks of text',
      url='https://github.com/wilsonfreitas/textparser',
      license='MIT',
      keywords='text, parser, text parser, parsing',
      long_description='''\
Frequently I have to parse text into float, int and date, for just a few examples.
I've written that class to isolate the parsing task, instead of getting it spreaded all over the code.
This is a fairly simple class which helped me very much.

Simply create a class inheriting TextParser define the parsing rules as the following and in the end call the method parse.

Examples::

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

''',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Operating System :: OS Independent"
    ],
)

