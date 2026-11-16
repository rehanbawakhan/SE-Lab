import pytest
from attendance_eligibility import attendance_percent, exam_eligibility, attendance_warning

#Example test cases:
def test_plain_percent():
    assert attendance_percent(30, 40, 0) == 75

def test_eligible():
    assert exam_eligibility(80, False, True) == "eligible"

#Write the rest of the test cases so that the code is 90- 100% covered.
