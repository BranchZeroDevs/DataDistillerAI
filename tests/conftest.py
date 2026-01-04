"""Test configuration and fixtures."""

import os
from pathlib import Path


# Test data directory
TEST_DATA_DIR = Path(__file__).parent / "test_data"


def setup_test_data():
    """Create test data directory and files."""
    TEST_DATA_DIR.mkdir(exist_ok=True)
    
    # Create sample text file
    sample_file = TEST_DATA_DIR / "sample.txt"
    with open(sample_file, 'w') as f:
        f.write("Sample document for testing.\n")
        f.write("It contains multiple paragraphs.\n")
        f.write("\n")
        f.write("This is the second paragraph with more content.")


if __name__ == "__main__":
    setup_test_data()
