import random

def PasswordGenerator(n_lower=7, n_upper=1, n_numbers=1, n_symbols=1):

    lower = 'abcdefghijklmnopqrstuvwxyz'
    upper = lower.upper()
    numbers = '0123456789'
    symbols = '[]{}()*/_-%#'
    whole = ''
    i_max = max(n_lower, n_upper, n_numbers, n_symbols)

    for i in range(i_max):

        if n_lower > 0:
            whole = whole + random.choice(lower)
            n_lower -= 1
        if n_upper > 0:
            whole = whole + random.choice(upper)
            n_upper -= 1
        if n_numbers > 0:
            whole = whole + random.choice(numbers)
            n_numbers -= 1
        if n_symbols > 0:
            whole = whole + random.choice(symbols)
            n_symbols -= 1

    password = ''.join(random.sample(whole, len(whole)))

    return password
