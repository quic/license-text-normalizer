# Copyright (c) 2020, Qualcomm Innovation Center, Inc. All rights reserved.
# SPDX-License-Identifier: BSD-3-Clause

import csv
import os

import pytest

from license_text_normalizer import normalize_license_text


@pytest.fixture
def fixtures():
    pathname = os.path.join(os.path.dirname(__file__), "fixtures.csv")
    return _load_fixtures(pathname)


def _load_fixtures(pathname):
    with open(pathname, "r") as f:
        contents = csv.reader(f)
        next(contents)  # skip header row
        return [(row[0], row[1]) for row in contents]


def test_validate_fixtures_files(fixtures):
    assert len(fixtures) == 32


def test_normalize_license_text(fixtures):
    for raw, normalized in fixtures:
        assert normalize_license_text(raw) == normalized
