#!/usr/bin/env python3

import pytest
from hypothesis import given
from datetime import timedelta
from hypothesis.strategies import timedeltas, from_regex, sampled_from

import taskw

# ag "def " taskw.py:
# 14:def _default(name, default="", arg_type=str):
# 21:def strbool(s):
# --- need mockup of system variables
# 57:def shorten(string, maxlen=maxlen):
# --- done
# 67:def get_taskw_json(filter_string):
# --- need .task mockup
# 73:def sort_taskw_info(taskw_json):
# --- need json output fixture
# 85:def get_taskw_info(taskw_filter="+ACTIVE"):
# --- skipping
# 90:def export_pending():
# 97:def get_timew_bytes(dom_string):
# --- need mockup of timew output
# 105:def decode_timew_bytes(in_bytes):
# --- need timew output fixture (bytes)
# 110:def get_timew_string(dom_string):
# 115:def get_timew_active():
# 119:def export_timew_description():
# --- skipping
# 124:def pad_time(s):
# --- done
# 128:def extract_time(delimiter, input_string):
# --- can do
# 133:def translate_timew_string(timew_in_str):
# --- done
# 139:def main():
# --- skipping


@pytest.fixture
def maxlen():
    return 35


# TODO: tidy up TestShorten
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


class TestPadTime:
    @given(from_regex(r"^[0-5]?[0-9]$", fullmatch=True))
    def test_match_as_numbers(self, digits):
        padded_time = taskw.pad_time(digits)
        assert int(padded_time) == int(digits)

    @given(from_regex(r"^[0-5]?[0-9]$", fullmatch=True))
    def test_length(self, digits):
        padded_time = taskw.pad_time(digits)
        assert len(padded_time) == 2


class TestExtractTime:
    @given(
        td=timedeltas(timedelta(seconds=1), timedelta(hours=12)),
        t_str=sampled_from(["H", "M", "S"]),
    )
    def test_match_as_numbers(self, td, t_str):
        hrs, remainder = divmod(td, timedelta(seconds=3600))
        mins, seconds = divmod(remainder, timedelta(seconds=60))
        time_dict = {"H": hrs, "M": mins, "S": seconds.seconds}
        input_string = f"PT{hrs}H{mins}M{seconds.seconds}S"
        output_string = time_dict[t_str]
        result = taskw.extract_time(t_str, input_string)
        assert int(result) == int(output_string)


class TestTranslateTimewString:
    @given(timedeltas(timedelta(seconds=1), timedelta(hours=12)))
    def test_translate_timew_string(self, td):
        hrs, remainder = divmod(td, timedelta(seconds=3600))
        mins, seconds = divmod(remainder, timedelta(seconds=60))
        input_string = f"PT{hrs}H{mins}M{seconds.seconds}S"
        output_string = f"{hrs:0>2d}:{mins:0>2d}"
        result = taskw.translate_timew_string(input_string)
        assert result == output_string
