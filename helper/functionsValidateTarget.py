def validate_target_donor(target_amount):
    """
    Memvalidasi target donor agar tidak bernilai negatif.

    Parameters:
    target_amount (int): Nilai target donor.

    Returns:
    int: Nilai target donor yang valid (>= 0).
    """
    if target_amount < 0:
        raise ValueError("Target donor tidak bisa bernilai negatif.")
    return target_amount