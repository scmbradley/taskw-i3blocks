#!/usr/bin/env python3

import pytest
from hypothesis import given
from datetime import timedelta
from hypothesis.strategies import timedeltas, text

import taskw


@pytest.fixture
def maxlen():
    return 35


class TestTimewTranslation:
    @given(timedeltas(timedelta(seconds=1), timedelta(hours=12)))
    def test_timew_translation(self, td):
        hrs, remainder = divmod(td, timedelta(seconds=3600))
        mins, seconds = divmod(remainder, timedelta(seconds=60))
        input_string = f"PT{hrs}H{mins}M{seconds.seconds}S"
        output_string = f"{hrs:0>2d}:{mins:0>2d}"
        result = taskw.translate_timew_string(input_string)
        assert result == output_string


class TestShorten:
    def test_shorten_default(self, maxlen):
        long_string = "This string is too long and should be shortened to etc and so on"
        shortened_string = "This string is too long and shou..."
        assert taskw.shorten(long_string) == shortened_string

    def test_shorten_non_default(self):
        long_string = "This string is too long and should be shortened to etc and so on"
        shortened_string = "This string is to..."
        assert taskw.shorten(long_string, maxlen=20) == shortened_string

    def test_shorten_no_action(self, maxlen):
        long_string = "Short"
        assert taskw.shorten(long_string) == long_string
