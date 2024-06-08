# startup.py

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

# 2024 Amar Abane

# Description: This file is part of the AskBatfish project which interacts with
# Batfish using LLMs.


# Importing required libraries, setting up logging, and loading questions
import logging
import random  # noqa: F401
from typing import List, Optional  # noqa: F401

import pandas as pd
from IPython.display import display
from pandas.io.formats.style import Styler

from pybatfish.client.session import Session  # noqa: F401

# noinspection PyUnresolvedReferences
from pybatfish.datamodel import Edge, Interface  # noqa: F401
from pybatfish.datamodel.answer import TableAnswer
from pybatfish.datamodel.flow import HeaderConstraints, PathConstraints  # noqa: F401
from pybatfish.datamodel.route import BgpRoute  # noqa: F401
from pybatfish.util import get_html

# Configure all pybatfish loggers to use WARN level
logging.getLogger("pybatfish").setLevel(logging.WARN)

pd.set_option("display.max_colwidth", None)
pd.set_option("display.max_columns", None)
# Prevent rendering text between '$' as MathJax expressions
pd.set_option("display.html.use_mathjax", False)

# UUID for CSS styles used by pandas styler.
# Keeps our notebook HTML deterministic when displaying dataframes
_STYLE_UUID = "pybfstyle"


class MyStyler(Styler):
    """A custom styler for displaying DataFrames in HTML"""

    def __repr__(self):
        return repr(self.data)


def show(df):
    """
    Displays a dataframe as HTML table.

    Replaces newlines and double-spaces in the input with HTML markup, and
    left-aligns the text.
    """
    if isinstance(df, TableAnswer):
        df = df.frame()

    # workaround for Pandas bug in Python 2.7 for empty frames
    if not isinstance(df, pd.DataFrame) or df.size == 0:
        display(df)
        return
    display(
        MyStyler(df)
        .set_uuid(_STYLE_UUID)
        .format(get_html)
        .set_properties(**{"text-align": "left", "vertical-align": "top"})
    )
