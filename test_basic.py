#!/usr/bin/env python3

import pytest
import taskw


@pytest.fixture
def maxlen():
    return 35


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
        t = taskw.export_duration()
        assert t == "02:03"
