from string import Template


def matrix_formatter(symbol: str, n_rows: int, n_cols: int):
    """A formatter for efficiently generating
    LaTeX matrices that contains `symbol`

    Args:
        symbol (str): The symbol
        n_rows (int): Number of rows
        n_cols (int): Number of columns
    """
    SUBSCRIPT = '_'
    t = Template('$symbol$subscript{$r$c} $delimiter')
    for r in range(n_rows):
        for c in range(n_cols):
            if c + 1 == n_cols:
                delimiter = r'\\'
            else:
                delimiter = '& '
            print(
                t.substitute(
                    symbol=symbol,
                    subscript=SUBSCRIPT,
                    r=r,
                    c=c,
                    delimiter=delimiter
                ),
                end=''
            )
        print()


def auto_subscripter():
    pass
