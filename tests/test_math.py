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

import unittest

from fuzztastic.utils.math import avg, div


class TestDiv(unittest.TestCase):
    def test_div_basic(self) -> None:
        # Arrange
        numerator = 10
        denominator = 2

        # Act
        result = div(numerator, denominator)

        # Assert
        self.assertEqual(result, 5.0)

    def test_div_zero_numerator(self) -> None:
        # Arrange
        numerator = 0
        denominator = 5

        # Act
        result = div(numerator, denominator)

        # Assert
        self.assertEqual(result, 0.0)

    def test_div_zero_denominator(self) -> None:
        # Arrange
        numerator = 10
        denominator = 0

        # Act
        result = div(numerator, denominator)

        # Assert
        self.assertEqual(result, 0.0)

    def test_div_zero_denominator_custom_default(self) -> None:
        # Arrange
        numerator = 10
        denominator = 0
        default = -1.0

        # Act
        result = div(numerator, denominator, default)

        # Assert
        self.assertEqual(result, -1.0)

    def test_div_float_numbers(self) -> None:
        # Arrange
        numerator = 7.5
        denominator = 2.5

        # Act
        result = div(numerator, denominator)

        # Assert
        self.assertEqual(result, 3.0)

    def test_div_negative_numerator(self) -> None:
        # Arrange
        numerator = -10
        denominator = 2

        # Act
        result = div(numerator, denominator)

        # Assert
        self.assertEqual(result, -5.0)

    def test_div_negative_denominator(self) -> None:
        # Arrange
        numerator = 10
        denominator = -2

        # Act
        result = div(numerator, denominator)

        # Assert
        self.assertEqual(result, -5.0)

    def test_div_negative_numbers(self) -> None:
        # Arrange
        numerator = -10
        denominator = -2

        # Act
        result = div(numerator, denominator)

        # Assert
        self.assertEqual(result, 5.0)


class TestAvg(unittest.TestCase):
    def test_avg_basic(self) -> None:
        # Arrange
        values = [1, 2, 3, 4, 5]

        # Act
        result = avg(values)

        # Assert
        self.assertEqual(result, 3.0)

    def test_avg_empty_list(self) -> None:
        # Arrange
        values: list = []

        # Act
        result = avg(values)

        # Assert
        self.assertEqual(result, 0.0)

    def test_avg_single_element(self) -> None:
        # Arrange
        values = [42]

        # Act
        result = avg(values)

        # Assert
        self.assertEqual(result, 42.0)

    def test_avg_float_numbers(self) -> None:
        # Arrange
        values = [1.5, 2.5, 3.5]

        # Act
        result = avg(values)

        # Assert
        self.assertAlmostEqual(result, 2.5)

    def test_avg_negative_numbers(self) -> None:
        # Arrange
        values = [-2, -4, -6]

        # Act
        result = avg(values)

        # Assert
        self.assertEqual(result, -4.0)

    def test_avg_mixed_numbers(self) -> None:
        # Arrange
        values = [-10, 0, 10]

        # Act
        result = avg(values)

        # Assert
        self.assertEqual(result, 0.0)

    def test_avg_all_zeros(self) -> None:
        # Arrange
        values = [0, 0, 0]

        # Act
        result = avg(values)

        # Assert
        self.assertEqual(result, 0.0)
