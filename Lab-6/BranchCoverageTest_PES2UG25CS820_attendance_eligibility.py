import pytest
from attendance_eligibility import attendance_percent, exam_eligibility, attendance_warning

# Branch coverage: every decision evaluates to both True and False,
# plus boundary values on each comparison.


# ---------- attendance_percent ----------
# if total_classes <= 0
def test_total_zero_raises():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(0, 0, 0)


def test_total_negative_raises():
    with pytest.raises(ValueError, match="invalid total"):
        attendance_percent(0, -5, 0)


# if attended < 0 or attended > total_classes
def test_attended_negative_raises():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(-1, 40, 0)


def test_attended_above_total_raises():
    with pytest.raises(ValueError, match="invalid attended count"):
        attendance_percent(41, 40, 0)


def test_attended_zero_valid():
    assert attendance_percent(0, 40, 0) == 0


def test_attended_equals_total_valid():
    assert attendance_percent(40, 40, 0) == 100


# if medical_leave_days > 5  (True / False / boundary)
def test_leave_above_cap():
    assert attendance_percent(30, 40, 6) == 87      # capped to 5 -> 35/40


def test_leave_at_cap():
    assert attendance_percent(30, 40, 5) == 87      # not capped, still 5


def test_leave_below_cap():
    assert attendance_percent(30, 40, 2) == 80      # 32/40


# if credited > total_classes  (True / False / boundary)
def test_credited_exceeds_total():
    assert attendance_percent(38, 40, 5) == 100     # 43 -> 40


def test_credited_equals_total():
    assert attendance_percent(35, 40, 5) == 100     # exactly 40, not capped


def test_credited_below_total():
    assert attendance_percent(30, 40, 0) == 75


def test_integer_division_floors():
    assert attendance_percent(2, 3, 0) == 66        # 66.67 -> 66


# ---------- exam_eligibility ----------
# if not fees_paid
def test_fees_pending_overrides_good_attendance():
    assert exam_eligibility(100, True, False) == "fees pending"


def test_fees_pending_with_low_attendance():
    assert exam_eligibility(10, False, False) == "fees pending"


# if percent >= 75
def test_eligible_above_75():
    assert exam_eligibility(80, False, True) == "eligible"


def test_eligible_at_75_boundary():
    assert exam_eligibility(75, False, True) == "eligible"


# elif percent >= 65 -> if has_condonation (True / False)
def test_74_with_condonation():
    assert exam_eligibility(74, True, True) == "eligible"


def test_74_without_condonation():
    assert exam_eligibility(74, False, True) == "condonation required"


def test_65_boundary_with_condonation():
    assert exam_eligibility(65, True, True) == "eligible"


def test_65_boundary_without_condonation():
    assert exam_eligibility(65, False, True) == "condonation required"


# percent < 65 -> detained (condonation does not help)
def test_64_detained_even_with_condonation():
    assert exam_eligibility(64, True, True) == "detained"


def test_detained_without_condonation():
    assert exam_eligibility(30, False, True) == "detained"


# ---------- attendance_warning ----------
# if percent >= 85
def test_no_warning_above_85():
    assert attendance_warning(95, 1) is None


def test_no_warning_at_85_boundary():
    assert attendance_warning(85, 10) is None


# percent < 85 and >= 75 -> reminder
def test_reminder_at_84():
    assert attendance_warning(84, 5) == "reminder"


def test_reminder_at_75_boundary():
    assert attendance_warning(75, 2) == "reminder"


# if percent < 75 -> if weeks_left > 4 (True / False / boundary)
def test_critical_many_weeks_left():
    assert attendance_warning(74, 5) == "critical"


def test_final_notice_at_4_weeks_boundary():
    assert attendance_warning(74, 4) == "final notice"


def test_final_notice_few_weeks_left():
    assert attendance_warning(50, 0) == "final notice"


# ---------- integration: percent -> eligibility -> warning ----------
@pytest.mark.parametrize(
    "attended, total, leave, condonation, fees, exp_elig, exp_warn",
    [
        (36, 40, 0, False, True, "eligible", None),                   # 90%
        (30, 40, 0, False, True, "eligible", "reminder"),             # 75%
        (26, 40, 2, False, True, "condonation required", "final notice"),  # 70%
        (26, 40, 2, True, True, "eligible", "final notice"),          # 70% + condonation
        (20, 40, 0, True, True, "detained", "final notice"),          # 50%
        (36, 40, 0, True, False, "fees pending", None),               # fees unpaid
    ],
)
def test_end_to_end(attended, total, leave, condonation, fees, exp_elig, exp_warn):
    pct = attendance_percent(attended, total, leave)
    assert exam_eligibility(pct, condonation, fees) == exp_elig
    assert attendance_warning(pct, 3) == exp_warn
