"""
Generates markdown files for things.
"""
import os
import sys
from generator.md_generator import MDGenerator

TEMPLATE = "person.md"
ROSTER = "people.txt"
FILES_PATH = os.getcwd() + "/people/"


def main():
    """
    Run the program.
    """
    print("Running file_generator.py")
    # Get command line arguments
    args = sys.argv
    # Create an MDGenerator with the template, roster, and path
    md_generator = MDGenerator(TEMPLATE, ROSTER, FILES_PATH)

    # If there are no arguments, create people in the current directory
    if len(args) == 1:
        md_generator.make_files()
    else:
        # The first argument can be "insert-section", "remove-section", or "add-person"
        command = args[1]
        if command == "insert-section":
            # The second argument is the new section to insert
            new_section = args[2]
            # The third argument is the successor section
            successor = args[3]
            md_generator.global_insert_section(new_section, successor)
        elif command == "remove-section":
            # The second argument is the section to remove
            section = args[2]
            md_generator.global_remove_section(section)
        elif command == "make-file":
            # The second argument is the name of the thing
            name = args[2]
            md_generator.make_file(name)
        else:
            print("Bad arguments.")


if __name__ == '__main__':
    main()
