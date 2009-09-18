# -*- coding: utf-8 -*-
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