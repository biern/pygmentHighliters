# -*- coding: utf-8 -*-
#pygmentHighliters - third party pygments lexers.

#Copyright (C) 2009 Marcin Biernat <biern.m.com>

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU Affero General Public License as
#published by the Free Software Foundation, either version 3 of the
#License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU Affero General Public License for more details.

#You should have received a copy of the GNU Affero General Public License
#along with this program. If not, see <http://www.gnu.org/licenses/>.

__all__ = ['SassLexer']

import re
try:
    set
except NameError:
    from sets import Set as set

from pygments.lexer import Lexer, DelegatingLexer, RegexLexer, bygroups, \
     include, using, this
from pygments.token import Error, Punctuation, \
     Text, Comment, Operator, Keyword, Name, String, Number, Other, Token
from pygments.util import html_doctype_matches, looks_like_xml


class SassLexer(RegexLexer):
    name = "Sass"
    aliases = ["sass"]
    filenames = ["*.sass"]
    miemetypes = ['sass']

    tokens = {
        'root': [
            include('comments'),
            include('variables'),
            include('punctuation'),
            ("(^)(=)((\w|\\-)*?)$", bygroups(Text, Keyword, Name.Class)),
            ("(^)(\\+)((\w|\\-)*?)$", bygroups(Text, Keyword, Name.Class)),
            ("@for(?= )" , Keyword, 'forloop'),
            #NOTE: accepts anything starting with '@' as keyword
            ("@\w+(?=\s)", Keyword, 'computations'),
            ("^ *&", Keyword),
            ("^ *\w+", Name.Tag),
            ("#.*?(?=[^(\w|\\-)])", String),
            ("\.(\w|\\-)+", Name.Class),
            ("^ *:[\w\-]+", Name.Attribute, 'computations'),
            ("=(?= *?)", Operator, 'computations'),
            (".", Text),
        ],
        ## INLINES ##
        'punctuation':[
            ("\\(", Punctuation, "b1"),
            ("\\[", Punctuation, "b2"),
            ("\\{", Punctuation, "b3"),
        ],
        'comments':[
            #Multiline
            ("(?sm)^(?P<i> *?)/\*.*?^(?!(?P=i)(  |$))", Comment.Multiline),
            #Single line
            (" *?//.*$", Comment),
        ],
        #Like single line comment but pops state stack and does not match newline
        'pop-comment':[
            (" *?//.*(?=$)", Comment, "#pop"),
        ],
        'variables':[
            ("!\w+", Name.Variable),
        ],
        'values':[
            # number with units
            ("(\d+)(px|em|%)(?=\s)", bygroups(Number, Keyword)),
            # sole number
            ("(\d+\.\d+)(?![\d])", Number),
            ("(\d+)(?![\d])", Number),
            # hex
            ("#[0-9a-fA-F]{6}(?=\s)", Number.Hex),
            # string
            ("(?P<q>[\"'])(\\\\(?P=q)|.)*?(?P=q)", String),
        ],
        ## SEMI-INLINE ##
        'computations':[
            ("[a-zA-Z_]\w* *\\(", Name.Function, "function"),
            include('punctuation'),
            include('variables'),
            include('values'),
            include('pop-comment'),
            ("[\\-\\+\\*/]", Operator),
            ("$", Text, "#pop"),
            (".", Text),
        ],
        ## STATES ##
        'b1':[
            include('computations'),
            ('\\)', Punctuation, "#pop"),
        ],
        'b2':[
            include('computations'),
            ('\\]', Punctuation, "#pop"),
        ],
        'b3':[
            include('computations'),
            ('\\}', Punctuation, "#pop"),
        ],
        'function':[
            (',', Punctuation),
            ("\\)", Name.Function, "#pop"),
            include("computations"),
        ],
        'forloop':[
            (" +from(?= +)", Keyword),
            (" +to(?= +)", Keyword),
            include("computations"),
        ],
    }
