# -*- coding: utf-8 -*-
#pygmentHighliters - third party pygments lexers.

#Copyright (C) 2009 Marcin Biernat <biern.m@gmail.com>

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

__all__ = ['CucumberLexer']

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


class CucumberLexer(RegexLexer):
    name = "Cucumber"
    aliases = ["cucumber"]
    filenames = ["*.feature"]
    miemetypes = ['cucumber']

    KEYWORDS = ["Feature:", "Scenario:", "Scenario +Outline:", "Examples:", "Background:", "When", "Then", "And", "But", "Given"]

    tokens = {
        'root': [
            ("^ *({0})(?=\s)".format("|".join(KEYWORDS)), Keyword),
            ("(?P<q>[\"'])(\\\\(?P=q)|.)*?(?P=q)", String),
            ("\\|", Operator),
            (".", Text),
        ],
    }
