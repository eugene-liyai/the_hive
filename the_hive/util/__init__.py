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
import random
import string
from threading import Thread


_EMAIL_PATTERN = r"([\w\-\.]+@(\w[\w\-]+\.)+[\w\-]+)"
_NUMBERS_PATTERN = r"^[0-9]+$"
_WHITE_SPACE = r"[ \t]"


def generate_random_password_string():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))


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


def check_if_job_should_be_marked_as_paid(parent, job_item_update):
    if parent is None:
        return False
    if len(parent.job_detail) == 0:
        return False
    for job_item in parent.job_detail:
        if job_item.paid is False and job_item.job_details_id != job_item_update:
            return False
        return True


def is_job_duration_item_invalid(parent, duration):
    if parent is None:
        return True
    job_duration = parent.duration
    computed_duration = 0
    for job_items in parent.job_detail:
        computed_duration = job_items.duration + computed_duration

    if computed_duration + duration > job_duration:
        return True
    return False


def is_job_duration_invalid(parent, duration, item_id):
    if parent is None:
        return True
    job_duration = parent.duration
    computed_duration = 0
    for job_item in parent.job_detail:
        if job_item.job_details_id != item_id:
            computed_duration = job_item.duration + computed_duration

    if computed_duration + duration > job_duration:
        return True
    return False


def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target=f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
