import pytest
from attendance_eligibility import attendance_percent, exam_eligibility, attendance_warning

# Code (line) coverage: every statement in attendance_eligibility.py runs at least once.


# ---------- attendance_percent ----------
def test_plain_percent():
    assert attendance_percent(30, 40, 0) == 75


def test_invalid_total_raises():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(10, 0, 0)


def test_invalid_attended_raises():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(-1, 40, 0)


def test_medical_leave_capped_at_five():
    # 30 + min(10, 5) = 35 -> 35*100//40 = 87
    assert attendance_percent(30, 40, 10) == 87


def test_credited_capped_at_total():
    # 38 + 5 = 43 > 40 -> capped to 40 -> 100
    assert attendance_percent(38, 40, 5) == 100


# ---------- exam_eligibility ----------
def test_eligible():
    assert exam_eligibility(80, False, True) == "eligible"


def test_fees_pending():
    assert exam_eligibility(90, True, False) == "fees pending"


def test_eligible_with_condonation():
    assert exam_eligibility(70, True, True) == "eligible"


def test_condonation_required():
    assert exam_eligibility(70, False, True) == "condonation required"


def test_detained():
    assert exam_eligibility(50, True, True) == "detained"


# ---------- attendance_warning ----------
def test_no_warning():
    assert attendance_warning(90, 5) is None


def test_critical_warning():
    assert attendance_warning(60, 6) == "critical"


def test_final_notice():
    assert attendance_warning(60, 2) == "final notice"


def test_reminder():
    assert attendance_warning(80, 3) == "reminder"
