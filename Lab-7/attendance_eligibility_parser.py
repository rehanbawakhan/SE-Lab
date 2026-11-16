MAX_DIGITS = 9  # far more classes than any course will hold; also blocks huge-int DoS


def _parse_count(part):
    """Returns a non-negative int for a plain ASCII digit string, else None."""
    part = part.strip()
    if not part or len(part) > MAX_DIGITS:
        return None
    # isascii() rejects Unicode digits like '١' or '²'; isdigit() rejects '+5', '-5', '1_0', '3.5'
    if not (part.isascii() and part.isdigit()):
        return None
    return int(part)


def normalize_srn(srn):
    """
    Trims and upper-cases a student registration number.
    Returns None if srn is not a string or is empty after cleaning.
    """
    if not isinstance(srn, str):
        return None
    cleaned = "".join(srn.split()).upper()  # removes all whitespace, not only ' '
    return cleaned or None


def attendance_from_ratio(text):
    """
    Converts 'ATTENDED/HELD' into a whole-number percentage (0-100).
    Returns None for anything that is not two whole numbers with
    HELD > 0 and ATTENDED <= HELD.
    """
    if not isinstance(text, str):
        return None
    parts = text.split('/')
    if len(parts) != 2:
        return None
    attended = _parse_count(parts[0])
    held = _parse_count(parts[1])
    if attended is None or held is None:
        return None
    if held == 0 or attended > held:
        return None
    return attended * 100 // held


def attendance_from_register(marks):
    """
    Works out the attendance percentage (0-100) from a string of P (present) and A (absent).
    Returns None if marks is not a string, is empty, or has any character other than P/A.
    """
    if not isinstance(marks, str):
        return None
    marks = "".join(marks.split()).upper()
    if not marks or any(ch not in "PA" for ch in marks):
        return None
    return marks.count('P') * 100 // len(marks)


def _show(label, result):
    print(label, result if result is not None else "Invalid input")


def main():
    print("==== Running normalize_srn ====")
    value = input("Enter an SRN (e.g. pes1ug23cs001): ")
    _show("Normalized SRN:", normalize_srn(value))

    print("\n==== Running attendance_from_ratio ====")
    value = input("Enter classes attended and held as ATTENDED/HELD (e.g. 30/40): ")
    _show("Attendance percent:", attendance_from_ratio(value))

    print("\n==== Running attendance_from_register ====")
    value = input("Enter the register as P/A marks (e.g. PPAPP): ")
    _show("Attendance percent:", attendance_from_register(value))


if __name__ == "__main__":
    main()