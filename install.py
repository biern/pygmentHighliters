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

import sys
import os
import shutil

print("""
This script will attempt to install additional lexers for pygments library.
Note that it probably will require administrator rights for that, depending on your pygments installation.
--------------------------------
Starting process...
""")

try:
    import pygments
except ImportError:
    print("  Failed to import pygments library.")

lexers = []
if len(sys.argv) > 1:
    lexers.extend(sys.argv[1:])
else:
    print("  No filenames specified, guessing them from working dir")
    lexers = [f for f in os.listdir('.') if f.lower().endswith("lexer.py")]
    
if not lexers:
    print("  No files found, exiting!")
    
print("  Will attempt to install following files: {0}".format(", ".join(lexers)))
print("  Guessing installation dirs...")
lexers_dir = os.path.join(os.path.dirname(pygments.__file__), "lexers")
if raw_input("  Attempting to copy files to \"{0}\". Procced? (Y/n)".format(lexers_dir)) == "n":
    print("exiting")
    exit()

for file in lexers:
    copy_path = os.path.join(lexers_dir, file)
    if os.path.exists(copy_path):
        if raw_input("  File \"{0}\" already exists. Overwrite? (Y/n)".format(copy_path)) == "n":
            print("   skipping")
            continue
        
    print("    copying \"{0}\" to \"{1}\"...".format(file, copy_path))
    shutil.copy(file, copy_path)

print("Copying finished!")
print("Running _mapping.py...\n")
os.system("cd {0} && python _mapping.py".format(lexers_dir))
print("Done!")