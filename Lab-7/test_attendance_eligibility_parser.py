from hypothesis import given, strategies as st
from attendance_eligibility_parser import normalize_srn, attendance_from_ratio, attendance_from_register

@given(st.text() | st.none())
def test_normalize_srn_no_crash(s):
    try:
        result = normalize_srn(s)
        assert result is None or isinstance(result, str)
    except Exception as e:
        assert False, f"normalize_srn crashed with: {e!r} on input {s!r}"

@given(st.text() | st.none())
def test_attendance_from_ratio_no_crash(s):
    try:
        result = attendance_from_ratio(s)
        assert result is None or 0 <= result <= 100
    except Exception as e:
        assert False, f"attendance_from_ratio crashed with: {e!r} on input {s!r}"

@given(st.text() | st.none())
def test_attendance_from_register_no_crash(s):
    try:
        result = attendance_from_register(s)
        assert result is None or 0 <= result <= 100
    except Exception as e:
        assert False, f"attendance_from_register crashed with: {e!r} on input {s!r}"