import re

def replace_quoted(s, old, new):
    pattern = r'(?<!\\)(?:"(?:\\.|[^\\"])*?){}((?:\\.|[^\\"])*)"'.format(re.escape(old))
    return re.sub(pattern, lambda m: m.group().replace(old, new), s)

def replace_unquoted(s, old, new):
    pattern = f'(?<!\\\\)(?:"(?:\\\\.|[^\\\\"])*")|({re.escape(old)})'
    def repl(match):
        return new if match.group(1) else match.group(0)
    return re.sub(pattern, repl, s)

def split_unquoted(s):
    pattern = r'"(?:\\.|[^\\"])*"|\S+'
    return re.findall(pattern, s)

def uncomment(s):
    pattern = r'"(?:\\.|[^\\"])*"|;[^\n]*'
    uncommented = re.sub(pattern, lambda m: m.group(0) if m.group(0)[0] == '"' else '', s)
    return uncommented.strip()

# LISP TO PYTHON
def read(expr):
    expr = uncomment(expr)

    expr = replace_unquoted(expr, '\\', '\\\\')

    expr = replace_unquoted(expr, '(', '( ')
    expr = replace_unquoted(expr, ')', ' )')

    expr = split_unquoted(expr)
    expr = [i if i in ('(', ')') else (f"'{i}'" if i[0] == '"' else (f'"{i}"' if "'" in i else f"'{i}'")) for i in expr]

    expr = ','.join(expr)
    expr = replace_unquoted(expr, '(,', '(')
    
    try:
        expr = eval(expr)
    except:
        raise Exception('couldn\'t read expression - maybe missing parenthesis?')
    
    if len(expr) == 1:
        if isinstance(expr[0], str) and expr[0].startswith('"') and expr[0].endswith('"'):
            expr = expr[0]
        elif isinstance(expr[0], str) and expr[0].replace('.', '', 1).isdigit():
            expr = expr[0]

    return expr
