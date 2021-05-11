#!/usr/bin/env python3

import pytest
from hypothesis import given
from datetime import timedelta
from hypothesis.strategies import timedeltas

import taskw


@pytest.fixture
def maxlen():
    return 35


@given(timedeltas(timedelta(seconds=1), timedelta(hours=12)))
def test_duration(monkeypatch, td):
    hrs, remainder = divmod(td, timedelta(seconds=3600))
    mins, seconds = divmod(remainder, timedelta(seconds=60))

    def patch_time():
        return f"PT{hrs}H{mins}M{seconds.seconds}S"

    monkeypatch.setattr(taskw, "time_to_str", patch_time)
    t_exp = taskw.translate_timew_string()
    t_out = f"{hrs}:{mins}"
    assert t_exp == t_out


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


class TestExportDuration:
    def test_duration(self, monkeypatch):
        def patch_time(self):
            return "PT2H3M17S"

        monkeypatch.setattr(taskw, "timew_to_str", patch_time)
        t = taskw.translate_timew_string()
        assert t == "02:03"
