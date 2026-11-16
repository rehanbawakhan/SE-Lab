def attendance_percent(attended, total_classes, medical_leave_days):
    if total_classes <= 0:
        raise ValueError("invalid total")
    if attended < 0 or attended > total_classes:
        raise ValueError("invalid attended count")
    if medical_leave_days > 5:
        medical_leave_days = 5
    credited = attended + medical_leave_days
    if credited > total_classes:
        credited = total_classes
    return credited * 100 // total_classes


def exam_eligibility(percent, has_condonation, fees_paid):
    if not fees_paid:
        return "fees pending"
    if percent >= 75:
        return "eligible"
    elif percent >= 65:
        if has_condonation:
            return "eligible"
        return "condonation required"
    return "detained"


def attendance_warning(percent, weeks_left):
    if percent >= 85:
        return None
    if percent < 75:
        if weeks_left > 4:
            return "critical"
        return "final notice"
    return "reminder"
