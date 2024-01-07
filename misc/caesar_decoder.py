"""
Basic Caesar's decoder

Try to found the best wheel position for a french message target.
"""


# some const
wheel_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


# some function
def caesarize_letter(letter: str, offset: int) -> str:
    if letter in wheel_letters:
        idx = wheel_letters.index(letter)
        caesar_idx = (idx + offset) % len(wheel_letters)
        return wheel_letters[caesar_idx]
    else:
        return letter


def fr_ratio(text: str) -> float:
    # an higher ratio of 'e' to 'z' in text suggests it might be French
    # here max() avoid to divide by zero
    return text.count('E') / max(1, text.count('Z'))


if __name__ == '__main__':
    # the mystery message
    myst_msg = "B'ULUHUIJ UIJ BU FBKI XQKJ IECCUJ TK JYRUJ."

    # try to decode the message for each wheel positions
    d_wheel_pos = {}
    for wheel_offset in range(len(wheel_letters)):
        # with this caesar wheel try to decrypt message
        decrypt_msg = ''
        for myst_letter in myst_msg:
            decrypt_msg += caesarize_letter(myst_letter, offset=wheel_offset)
        wheel_position = wheel_letters[wheel_offset]
        d_wheel_pos[wheel_position] = dict(dec_msg=decrypt_msg, fr_ratio=fr_ratio(decrypt_msg))

    # sorted d_pos by french ratio order (highest first) with a limit to the first 3 best ratios
    d_wheel_pos = dict(sorted(d_wheel_pos.items(), key=lambda item: item[1]['fr_ratio'], reverse=True)[:3])

    # display the 3 best wheel positions
    for wheel_pos, result_d in d_wheel_pos.items():
        print(f"A -> {wheel_pos}: fr_ratio={result_d['fr_ratio']}: \"{result_d['dec_msg']}\"")
