# Copyright 2021-2025 Chair for Software & Systems Engineering, TUM
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import tempfile
import unittest
from pathlib import Path

from fuzztastic.utils.io import write_text


class TestWriteText(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.mkdtemp()
        self.temp_dir_path = Path(self.temp_dir)

    def tearDown(self) -> None:
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_write_text_basic(self) -> None:
        # Arrange
        file_path = self.temp_dir_path / "test.txt"
        text = "Hello, world!"

        # Act
        write_text(file_path, text)

        # Assert
        self.assertEqual(file_path.read_text(), text)

    def test_write_text_with_linebreak(self) -> None:
        # Arrange
        file_path = self.temp_dir_path / "test.txt"
        text = "Hello, world!"

        # Act
        write_text(file_path, text, linebreak=True)

        # Assert
        self.assertEqual(file_path.read_text(), text + os.linesep)

    def test_write_text_append(self) -> None:
        # Arrange
        file_path = self.temp_dir_path / "test.txt"
        text1 = "text 1"
        text2 = "text 2"

        # Act
        write_text(file_path, text1)
        write_text(file_path, text2, append=True)

        # Assert
        self.assertEqual(file_path.read_text(), text1 + text2)

    def test_write_text_append_with_linebreak(self) -> None:
        # Arrange
        file_path = self.temp_dir_path / "test.txt"
        text1 = "text 1"
        text2 = "text 2"

        expected = text1 + os.linesep + text2 + os.linesep

        # Act
        write_text(file_path, text1, linebreak=True)
        write_text(file_path, text2, linebreak=True, append=True)

        # Assert
        self.assertEqual(file_path.read_text(), expected)

    def test_write_text_overwrite(self) -> None:
        # Arrange
        file_path = self.temp_dir_path / "test.txt"
        text1 = "text 1"
        text2 = "text 2"

        # Act
        write_text(file_path, text1)
        write_text(file_path, text2)

        # Assert
        self.assertEqual(file_path.read_text(), text2)

    def test_write_text_multiline_content(self) -> None:
        # Arrange
        file_path = self.temp_dir_path / "test.txt"
        text = "Line 1" + os.linesep + "Line 2" + os.linesep + "Line 3"

        # Act
        write_text(file_path, text)

        # Assert
        self.assertEqual(file_path.read_text(), text)
