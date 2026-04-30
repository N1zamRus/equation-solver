class BigFloat():
    BASE_DIGITS = 5
    BASE = 10 ** BASE_DIGITS       

    def __init__(self, sign: int, blocks: list[int], exp10: int):
        self.sign = sign
        self.blocks = blocks
        self.exp10 = exp10

    def __repr__(self):
        return bigfloat_string(self)
    
    def __abs__(self):
        return BigFloat(sign=1, blocks=self.blocks, exp10=self.exp10)
    
    def __eq__(self, other):
        return compare(self, other) == 0

    def __ne__(self, other):
        return compare(self, other) != 0

    def __lt__(self, other):
        return compare(self, other) < 0

    def __le__(self, other):
        return compare(self, other) <= 0

    def __gt__(self, other):
        return compare(self, other) > 0

    def __ge__(self, other):
        return compare(self, other) >= 0
    
    def __neg__(self):
        return BigFloat(sign=-1*self.sign, blocks=self.blocks, exp10=self.exp10)
    

def get_blocks(cls: BigFloat):
    return cls.blocks

def get_sign(cls: BigFloat):
    return cls.sign

def get_exp10(cls: BigFloat):
    return cls.exp10

def get_BASE(cls = BigFloat):
    return cls.BASE

def get_BASE_DIGITS(cls = BigFloat):
    return cls.BASE_DIGITS

def is_zero(number: BigFloat):
    blocks = get_blocks(number)
    for val in blocks:
        if val != 0:
            return False
    return True

def get_mantiss(cls: BigFloat):
    if not cls.blocks:
        return "0"

    parts = [str(cls.blocks[-1])]

    for i in range(len(cls.blocks) - 2, -1, -1):
        parts.append(str(cls.blocks[i]).zfill(get_BASE_DIGITS()))

    return "".join(parts)

def create_BigFloat(num: str):
    sign = 1
    exp10 = 0

    if num[0] == "-":
        sign = -1
        num = num[1:]
    elif num[0] == "+":
        num = num[1:]   


    num = num.replace(",", ".")

    if "e" in num or "E" in num:
        if "e" in num:
            parts = num.split("e")
        else:
            parts = num.split("E")

        num = parts[0]
        exp10 += int(parts[1])

    if "." in num:
        dot_pos = num.find(".")
        digits_after_dot = len(num) - dot_pos - 1

        exp10 -= digits_after_dot
        num = num.replace(".", "")

    num = num.lstrip("0") or "0"


    blocks = slice_blocks(num)
    return normalize(BigFloat(sign, blocks, exp10))


def slice_blocks(mantissa: str):
    BASE_DIGITS = get_BASE_DIGITS()
    blocks = []

    for i in range(len(mantissa), 0, -BASE_DIGITS):
        start = max(0, i - BASE_DIGITS)
        block = mantissa[start:i]
        blocks.append(int(block))

    return blocks


def bigfloat_string(num: BigFloat):
    output_line = get_mantiss(num)
    num_sign = "-" if get_sign(num) == -1 and output_line != "0" else ""
    num_exp = get_exp10(num)

    if num_exp == 0:
        return num_sign + output_line
    if num_exp > 0:
        return num_sign + output_line + "0" * num_exp

    dot_pos = len(output_line) + num_exp
    if dot_pos > 0:
        return num_sign + output_line[:dot_pos] + "." + output_line[dot_pos:]
    else:
        return num_sign + "0." + "0" * (-dot_pos) + output_line
    

def normalize(num: BigFloat):
    sign = num.sign
    blocks = num.blocks.copy()
    exp10 = num.exp10

    while blocks and blocks[-1] == 0:
        blocks.pop()

    if not blocks:
        return BigFloat(1, [0], 0)

    mantissa = get_mantiss(BigFloat(sign, blocks, exp10))

    while exp10 < 0 and mantissa and mantissa[-1] == "0":
        mantissa = mantissa[:-1]
        exp10 += 1

    mantissa = mantissa.lstrip("0") or "0"

    if mantissa == "0":
        return BigFloat(1, [0], 0)

    blocks = slice_blocks(mantissa)

    return BigFloat(sign, blocks, exp10)

def make_carry(coeffs: list[int]):
    BASE = get_BASE()

    carry = 0
    blocks = []

    for x in coeffs:
        x = int(x) + carry

        blocks.append(x % BASE)
        carry = x // BASE

    while carry > 0:
        blocks.append(carry % BASE)
        carry //= BASE

    while len(blocks) > 1 and blocks[-1] == 0:
        blocks.pop()

    return blocks


def compare(self: BigFloat, other: BigFloat):
    a = normalize(self)
    b = normalize(other)

    if is_zero(a) and is_zero(b):
        return 0
    
    if a.sign != b.sign:
        return 1 if a.sign > b.sign else -1

    a, b = align(a, b)
    cmp_abs = compare_abs(a, b)

    if a.sign == 1:
        return cmp_abs
    else:
        return -cmp_abs

def align(a: BigFloat, b: BigFloat):
    min_exp = min(a.exp10, b.exp10)

    if a.exp10 > min_exp:
        a = shift_exp(a, a.exp10 - min_exp)

    if b.exp10 > min_exp:
        b = shift_exp(b, b.exp10 - min_exp)

    return a, b

def shift_exp(num: BigFloat, exp_diff: int):
    if exp_diff <= 0:
        return BigFloat(num.sign, num.blocks.copy(), num.exp10)
    
    BASE_DIGITS = get_BASE_DIGITS()
    BASE = get_BASE()

    block_shift = exp_diff // BASE_DIGITS
    digit_shift = exp_diff % BASE_DIGITS

    sign = get_sign(num)
    exponent = get_exp10(num)
    blocks = get_blocks(num).copy()

    if block_shift > 0:
        blocks = [0] * block_shift + blocks

    if digit_shift > 0:
        mul = 10 ** digit_shift
        carry = 0
        for i in range(len(blocks)):
            val = blocks[i] * mul + carry
            blocks[i] = val % BASE
            carry = val // BASE
        while carry > 0:
            blocks.append(carry % BASE)
            carry //= BASE

    exponent -= exp_diff

    return BigFloat(sign, blocks, exponent)

def compare_abs(a: BigFloat, b: BigFloat):
    a_blocks = del_zeros(get_blocks(a))
    b_blocks = del_zeros(get_blocks(b))

    if len(a_blocks) > len(b_blocks):
        return 1

    if len(a_blocks) < len(b_blocks):
        return -1

    for i in range(len(a_blocks) - 1, -1, -1):
        if a_blocks[i] > b_blocks[i]:
            return 1
        if a_blocks[i] < b_blocks[i]:
            return -1

    return 0

def del_zeros(blocks: list[int]):
    blocks = blocks.copy()

    while len(blocks) > 1 and blocks[-1] == 0:
        blocks.pop()

    return blocks