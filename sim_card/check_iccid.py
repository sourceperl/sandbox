""" Control SIM card number

Each SIM is internationally identified by its integrated circuit card identifier (ICCID). 
Nowadays ICCID numbers are also used to identify eSIM profiles, not only physical SIM cards. 
ICCIDs are stored in the SIM cards and are also engraved or printed on the SIM card body during a process 
called personalisation.

The number can be up to 19 digits long, including a single check digit calculated using the Luhn algorithm.
The purpose of this code is to validate an ICCID using this algorithm.
"""


def is_valid_iccid(iccid_str: str) -> bool:
    """Checks the validity of a number using the Luhn algorithm (https://en.wikipedia.org/wiki/Luhn_algorithm)."""

    # clean str
    iccid_str = iccid_str.replace(' ', '')
    if not iccid_str.isdigit():
        return False

    digits = [int(d) for d in iccid_str]
    total_sum = 0
    num_digits = len(digits)

    # iterate through digits from right to left
    double_next = False

    for i in range(num_digits - 1, -1, -1):
        digit = digits[i]

        if double_next:
            doubled_digit = digit * 2
            if doubled_digit > 9:
                total_sum += (doubled_digit - 9)  # or doubled_digit // 10 + doubled_digit % 10
            else:
                total_sum += doubled_digit
        else:
            total_sum += digit

        # invert flag for the next digit
        double_next = not double_next

    # check if the total sum is a multiple of 10
    return total_sum % 10 == 0


if __name__ == '__main__':
    # an example of ICCID validation
    valid_iccid = '1234 5678 9012 8'
    print(f'ICCID "{valid_iccid}" is ok : {is_valid_iccid(valid_iccid)}')
