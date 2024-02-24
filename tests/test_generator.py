"""
Test cases for MDGenerator class.
"""
import os
import shutil
import hashlib

import pytest
from generator.md_generator import MDGenerator

TEST_ROSTER = "test-roster.txt"
TEST_MD = "../person.md"
TEMP_MD = "template_copy.md"
TEMP_ROSTER = "roster_copy.md"
TEST_CONTENT_FILE = "test-content.txt"
TEST_CONTENT = []
TEST_GENERATOR = TEST_GENERATOR = MDGenerator(
    TEMP_MD, TEMP_ROSTER, os.getcwd() + "/person-files/")


@pytest.fixture(autouse=True)
def run_around_tests():
    """
    Wraps around each test.
    """
    # Before each test
    shutil.copyfile(TEST_MD, TEMP_MD)
    shutil.copyfile(TEST_ROSTER, TEMP_ROSTER)
    with open(TEST_CONTENT_FILE, "r", encoding="utf-8") as file:
        TEST_CONTENT.extend(file.readlines())
    yield

    # After each test
    os.remove(TEMP_MD)
    os.remove(TEMP_ROSTER)
    TEST_CONTENT.clear()


def compute_hash(file: str) -> str:
    """
    Return the md5 hash of the contents of the file as a hex string.
    """
    with open(file, "rb") as file:
        data = file.read()
        return hashlib.md5(data).hexdigest()


BASE_TEMPLATE_HASH = compute_hash(TEST_MD)


def compute_num_lines(file: str) -> int:
    """
    Return the number of lines in the file.
    """
    with open(file, "r", encoding="utf-8") as file:
        return len(file.readlines())


def test_insert_section() -> None:
    """
    Test insert_section.
    """
    # Get a count of the number of lines in the file
    num_lines = compute_num_lines(TEMP_MD)
    new_section = "New Section"
    successor = "KPIs"
    TEST_GENERATOR.insert_section(new_section, successor, TEMP_MD)
    # Check that the new section was inserted
    with open(TEMP_MD, "r", encoding="utf-8") as file:
        lines = file.readlines()
        # Verify that there is a line that starts with "## New Section"
        # and the line following it starts with "## KPIs"
        i = 0
        while i < len(lines) and not lines[i].startswith("## New Section"):
            i = i + 1
        assert lines[i].startswith("## New Section")
        assert lines[i + 1].startswith("## KPIs")
    # Check that the number of lines in the file has increased by 1
    assert compute_num_lines(TEMP_MD) == num_lines + 1


def test_remove_section() -> None:
    """
    Test remove_section.
    """
    # Get a count of the number of lines in the file
    num_lines = compute_num_lines(TEMP_MD)
    # Remove the "KPIs" section
    TEST_GENERATOR.remove_section("KPIs", TEMP_MD)
    # Check that the new section was removed
    with open(TEMP_MD, "r", encoding="utf-8") as file:
        lines = file.readlines()
        assert "KPIs" not in lines
    # Check that the number of lines in the file has decreased by 1
    assert compute_num_lines(TEMP_MD) == num_lines - 1


def test_insert_section_empty_successor() -> None:
    """
    Test insert_section with no successor.
    """
    # Get a count of the number of lines in the file
    num_lines = compute_num_lines(TEMP_MD)
    # Create a new section
    new_section = "New Section"
    # The new section should be inserted as the first section after name line
    successor = ""
    # Insert the new section
    TEST_GENERATOR.insert_section(new_section, successor, TEMP_MD)
    # Check that the new section was inserted as the first line of the file
    with open(TEMP_MD, "r", encoding="utf-8") as file:
        lines = file.readlines()
        assert "## New Section\n" == lines[0]
    # Check that the number of lines in the file has increased by 1
    assert compute_num_lines(TEMP_MD) == num_lines + 1


def test_insert_section_successor_not_found() -> None:
    """
    Test insert_section with a successor that is not found.
    Verify that section is added to the end.
    """
    # Get a count of the number of lines in the file
    num_lines = compute_num_lines(TEMP_MD)
    # Create a new section
    new_section = "New Section"
    # The new section should be appended to the end of the file
    successor = "Not Found"
    # Insert the new section
    TEST_GENERATOR.insert_section(new_section, successor, TEMP_MD)
    # Check that the new section was appended
    with open(TEMP_MD, "r", encoding="utf-8") as file:
        lines = file.readlines()
        assert "## New Section\n" == lines[-2]
    # Check that the number of lines in the file has increased by 1
    assert compute_num_lines(TEMP_MD) == num_lines + 1


def test_remove_section_not_found() -> None:
    """
    Test remove_section with a section that is not found.
    This should be a no-op.  Check that file contents don't change.
    """
    # Get hash of the people.PEOPLE_PATH file
    # original_hash = hashlib.md5("example string").hexdigest()
    original_hash = compute_hash(TEMP_MD)
    # New section is not in default template
    new_section = "## New Section"
    # Call remove_section for the non-existent section
    TEST_GENERATOR.remove_section(new_section, TEMP_MD)
    # Check that the file was not modified
    after_hash = compute_hash(TEMP_MD)
    assert original_hash == after_hash


def test_update_existing_empty_section() -> None:
    """
    Test update_section.
    """
    # Get a count of the number of lines in the file
    num_lines = compute_num_lines(TEMP_MD)
    TEST_GENERATOR.update_section("KPIs", TEST_CONTENT, TEMP_MD)
    # Check that the number of lines in the file has increased by len(TEST_CONTENT)
    assert compute_num_lines(TEMP_MD) == num_lines + len(TEST_CONTENT)
    with open(TEMP_MD, "r", encoding="utf-8") as file:
        lines = file.readlines()
    # Verify that TEST_CONTENT appears immediately after "## KPIs"
    i = 0
    while i < len(lines) and not lines[i].startswith("## KPIs"):
        i = i + 1
    i = i + 1
    for line in TEST_CONTENT:
        assert lines[i] == line
        i = i + 1


def test_update_section_replace_existing_content() -> None:
    """
    Test update_section with an existing section.
    """
    num_lines = compute_num_lines(TEMP_MD)
    TEST_GENERATOR.update_section("Dev plan", TEST_CONTENT, TEMP_MD)
    with open(TEMP_MD, "r", encoding="utf-8") as file:
        lines = file.readlines()
        print(lines)
    # Check that the number of lines in the file has increased by len(TEST_CONTENT)
    assert compute_num_lines(TEMP_MD) == num_lines + len(TEST_CONTENT)
    # Now update again, with different content
    TEST_GENERATOR.update_section("Dev plan", ["Different Content"], TEMP_MD)
    # Now length should just be one more than original
    assert compute_num_lines(TEMP_MD) == num_lines + 1
    # Check that the new content was inserted
    with open(TEMP_MD, "r", encoding="utf-8") as file:
        lines = file.readlines()
        # Verify that there is a line that starts with "## Dev Plan"
        # and the line following it starts with "Different Content"
        i = 0
        while i < len(lines) and not lines[i].startswith("## Dev plan"):
            i = i + 1
        assert lines[i].startswith("## Dev plan")
        assert lines[i + 1].startswith("Different Content")


def test_update_section_replace_existing_content_last_section() -> None:
    """
    Test update last section that is not empty.
    """
    num_lines = compute_num_lines(TEMP_MD)
    # Update the "Alarms" section with TEST_CONTENT
    TEST_GENERATOR.update_section("Alarms", TEST_CONTENT, TEMP_MD)
    assert compute_num_lines(TEMP_MD) == num_lines + len(TEST_CONTENT)
    # Now update again, with different content
    TEST_GENERATOR.update_section("Alarms", ["Different Content"], TEMP_MD)
    # Now length should just be one more than original
    assert compute_num_lines(TEMP_MD) == num_lines + 1
    # Check that the new content was inserted
    with open(TEMP_MD, "r", encoding="utf-8") as file:
        lines = file.readlines()
        # Verify that there is a line that starts with "## Alarms"
        # and the line following it starts with "Different Content"
        i = 0
        while i < len(lines) and not lines[i].startswith("## Alarms"):
            i = i + 1
        assert lines[i].startswith("## Alarms")
        assert lines[i + 1].startswith("Different Content")


def test_update_non_existent_section() -> None:
    """
    Test update_section with a section that is not found.
    Verify that section is added to the end.
    """
    num_lines = compute_num_lines(TEMP_MD)
    # Update the "Not Found" section with TEST_CONTENT
    TEST_GENERATOR.update_section("Not Found", TEST_CONTENT, TEMP_MD)
    # Check that the number of lines in the file has increased by len(TEST_CONTENT)
    assert compute_num_lines(TEMP_MD) == num_lines + len(TEST_CONTENT) + 1
    # Check that the new content was inserted at the end of the file
    with open(TEMP_MD, "r", encoding="utf-8") as file:
        lines = file.readlines()
        # Verify that there is a line that starts with "## Not Found"
        # and the line following it starts with "Different Content"
        i = 0
        while i < len(lines) and not lines[i].startswith("## Not Found"):
            i = i + 1
        assert lines[i].startswith("## Not Found")
        assert lines[i + 1].startswith(TEST_CONTENT[0])
        assert lines[-1].startswith(TEST_CONTENT[-1])
