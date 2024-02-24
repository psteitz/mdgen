
"""
Creates markdown files for people in people.txt.
"""
import os
from typing import List


class MDGenerator:
    """
    A class to generate markdown files.
    """

    def __init__(self, template: str, roster: str, path: str) -> None:
        self.template = template
        self.roster = roster
        self.path = path

    def make_files(self) -> None:
        """
        Create people markdown files for the people in people.txt.
        """
        # Open the roster file and read the lines into a list of strings
        with open(self.roster, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Iterate over the lines creating person files
        for line in lines:
            if line != "\n":
                name = line.strip()
                self.make_file(name)

    def make_file(self, name: str) -> None:
        """
        Create a person markdown file with the given name. 
        Use TEMPLATE as the template.  Save the file to the given path.
        Make sure that a line with the person's name exists in ROSTER.  
        If not, add it.  The file name should be name_x.md where x is the next available number.
        Name is the person's name with spaces replaced by underscores.

        Args:
            name: The name of the person.
            path: The path to save the file.
        """
        # Create a new md file with the given name with spaces replaced by underscores.
        # Save the file to the given path.
        with open(self.path + name.replace(" ", "_").replace(",", "") + ".md", "w", encoding="utf-8") as f:
            # Now open the person.md file and read the lines int a list of strings
            with open(self.template, "r", encoding="utf-8") as f2:
                lines = f2.readlines()
            # Put the person's name, title and org into the top level header
            lines[0] = "# " + name + "\n"
            # Write the new contents to the new file
            f.writelines(lines)
            # Close the file
        # Add the person to the ROSTER if they are not already there
        with open(self.roster, "r", encoding="utf-8") as f:
            lines = f.readlines()
        person_exists = False
        for line in lines:
            if name in line:
                person_exists = True
                break
        if not person_exists:
            with open(self.roster, "a", encoding="utf-8") as f:
                f.write(name + "\n")

    def is_section_header(self, line: str) -> bool:
        """
        Return True if line is a section header, False otherwise.
        """
        return line.startswith("##") and not line.startswith("###")

    def insert_section(self, new_section: str, successor: str, md_file) -> None:
        """
        Update md_file by inserting new_section before the first occurrence of successor.
        If successor does not exist, new_section will be appended to the end of the file;
        unless successor is an empty string, in which case new_section will be inserted
        at the beginning of the file.
        """
        # Open the md_file and read the lines into a list of strings
        with open(md_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Find the index of the first occurrence of successor
        index = 0
        successor_exists = False
        for index, line in enumerate(lines):
            if line.startswith("## " + successor):
                successor_exists = True
                break
        if successor_exists:
            # Insert new_section before the index
            lines.insert(index, "## " + new_section.strip() + "\n")
        else:
            # If successor does not exist, append new_section to the end of the file
            lines.insert(index, "## " + new_section.strip() + "\n")
        # Write the new contents to the file
        with open(md_file, "w", encoding="utf-8") as f:
            f.writelines(lines)

    def update_section(self, section: str, new_lines: List[str], md_file: os.path) -> None:
        """
        Update md_file by replacing the content of section with new_lines.
        If the section does not exist, create it at the end of the file and add the content.
        The content of the section is all lines between the section header and the next section header.

        Args:
            section: The section to update.
            new_lines: The new content for the section.
            md_file: The file to update.
        """
        # Open the md_file and read the lines into a list of strings
        with open(md_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Find the index of the section header
        index = 0
        section_exists = False
        for index, line in enumerate(lines):
            if line.startswith("## " + section):
                section_exists = True
                break
        if section_exists:
            # Replace the content of the section with new_content
            index += 1
            section_content_index = index
            while index < len(lines) and not self.is_section_header(lines[index]):
                lines.pop(index)
                index += 1
            # Insert new_lines at index
            lines[section_content_index:section_content_index] = new_lines
        else:
            # If section does not exist, append section and new_content to the end of the file
            lines.append("## " + section + "\n")
            lines.extend(new_lines)
        # Write the new contents to the file
        with open(md_file, "w", encoding="utf-8") as f:
            f.writelines(lines)

    def add_to_section(self, section: str, new_lines: List[str], md_file: os.path) -> None:
        """
        Add new_lines to the end of the section.
        If the section does not exist, create it at the end of the file with new_lines as content.
        """
        # Open the md_file and read the lines into a list of strings
        with open(md_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Find the index of the first occurrence of section
        index = 0
        section_exists = False
        for index, line in enumerate(lines):
            if section in line:
                section_exists = True
                break
        if section_exists:
            # Find the index of the next section
            next_index = index + 1
            while next_index < len(lines) and not self.is_section_header(lines[next_index]):
                next_index += 1
            # Insert new_content before the next section
            if next_index == len(lines):
                lines.append(new_lines)
            else:
                lines.insert(next_index, new_lines)
        else:
            # If section does not exist, append section and new_content to the end of the file
            lines.append("# " + section)
            lines.append(new_lines)
        # Write the new contents to the file
        with open(md_file, "w", encoding="utf-8") as f:
            f.writelines(lines)

    def remove_section(self, section: str, md_file: os.path) -> None:
        """
        Remove a section.
        No-op if the
        """
        # Open the md_file and read the lines into a list of strings
        with open(md_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # Find the index of the first occurrence of section
        index = 0
        section_exists = False
        for index, line in enumerate(lines):
            if section in line:
                section_exists = True
                break
        if section_exists:
            # Remove the line at the index
            lines.pop(index)
            # Remove all lines between the index and the next section
            while index < len(lines) and not self.is_section_header(lines[index]):
                lines.pop(index)
            # Write the new contents to the file
            with open(md_file, "w", encoding="utf-8") as f:
                f.writelines(lines)

    def global_insert_section(self, new_section: str, successor: str) -> None:
        """
        Execute insert_section for all md files in directory.
        Then update TEMPLATE to include the new section.
        """
        for filename in os.listdir(self.path):
            if filename.endswith(".md"):
                self.insert_section(new_section, successor,
                                    self.path + filename)
        # Update TEMPLATE
        self.insert_section(new_section, successor, self.template)

    def global_remove_section(self, section: str) -> None:
        """
        Execute remove_section for all md files in directory.
        Then update TEMPLATE to remove the section.
        """
        for filename in os.listdir(self.path):
            if filename.endswith(".md"):
                self.remove_section(section, self.path + filename)
        # Update TEMPLATE
        self.remove_section(section, self.template)
