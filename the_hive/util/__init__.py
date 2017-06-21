# -*- coding:utf-8 -*-
"""
File      : util package
Date      : April, 2017
Author    : eugene liyai
Desc      : Gives utility activities.
"""

# ============================================================================
# necessary imports
# ============================================================================
import re


_EMAIL_PATTERN = r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)"
_NUMBERS_PATTERN = r"^[0-9]+$"
_WHITE_SPACE = r"[ \t]"


def has_white_space(value):
    regex = _WHITE_SPACE
    if re.search(regex, value):
        return True
    return False


def is_numbers_only(value):
    regex = _NUMBERS_PATTERN
    if has_white_space(value):
        return False
    if re.search(regex, value):
        return True
    return False


def is_email_valid(value):
    regex = _EMAIL_PATTERN
    if re.match(regex, value):
        return True
    return False


