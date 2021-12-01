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
    for r in range(1, n_rows + 1):
        for c in range(1, n_cols + 1):
            if c + 1 == n_cols + 1:
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
