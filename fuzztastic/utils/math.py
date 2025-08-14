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

from collections.abc import Sequence


def div(numerator: int | float, denominator: int | float, default: float = 0.0) -> float:
    """Safely divide two numbers (returns 0 if the denominator is zero)."""
    return numerator / denominator if denominator != 0 else default


def avg(values: Sequence[int | float]) -> float:
    """Safely calculate the average of a list of numbers (returns 0 if the list is empty)."""
    return div(sum(values), len(values))
