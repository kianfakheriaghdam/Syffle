from std import std
from read import read, uncomment

def eval_expr(*args):
    local = {args[1:][i]: args[1:][i+1] for i in range(0, len(args[1:]), 2)}
    return evaluate(read(args[0]), {**std, **local})

std.update({
    'macro/eval': eval_expr
})

def unquote(tup, f):
    if isinstance(tup, tuple) and len(tup) != 0:
        if tup[0] == 'macro/~':
            return f(tup[1])
        elif tup[0] == 'macro/~@':
            return (tup[1], *tuple(f(i) for i in tup[2:-1]), *f(tup[-1]))
        else:
            return tuple(unquote(x, f) for x in tup)
    else:
        return tup

def evaluate(expr, env=std):
    if isinstance(expr, tuple):
        # SPECIAL FUNCTIONS
        if expr[0] == 'define':
            env[expr[1]] = evaluate(expr[2], env)
    
        elif expr[0] == 'let':
            decls = []
            backs = {}
            for i in range(0, len(expr[1]), 2):
                if expr[1][i] in env.keys():
                    backs.update({expr[1][i]: env[expr[1][i]]})

                env[expr[1][i]] = evaluate(expr[1][i+1], env)
                decls += [expr[1][i]]

            result = [evaluate(i, env) for i in expr[2:]][-1]

            for key in decls:
                del env[key]

            env.update(backs)
            return result
    
        elif expr[0] == 'do':
            return [evaluate(i, env) for i in expr[1:]][-1]
    
        elif expr[0] == 'if':
            return evaluate(expr[2], env) if evaluate(expr[1], env) else evaluate(expr[3], env)
    
        elif expr[0] == 'cond':
            conds = ((evaluate(expr[1:][i], env), evaluate(expr[1:][i+1], env)) for i in range(0, len(expr[1:]), 2))
            for p, c in conds:
                if p: return c

        elif expr[0] == 'lambda':
            return lambda *args: evaluate(('do', *expr[2:]), {**env, **dict(zip(expr[1], args))})
        
        elif expr[0] == 'lambda*':
            return lambda *args: evaluate(('do', *expr[2:]), {**env, **dict(zip(expr[1][:-1], args[:len(expr[1])-1])), **{expr[1][-1]: args[len(expr[1])-1:]}})
    
        elif expr[0] == 'fun':
            env[expr[1]] = lambda *args: evaluate(('do', *expr[3:]), {**env, **dict(zip(expr[2], args))})

        elif expr[0] == 'fun*':
            env[expr[1]] = lambda *args: evaluate(('do', *expr[3:]), {**env, **dict(zip(expr[2][:-1], args[:len(expr[2])-1])), **{expr[2][-1]: args[len(expr[2])-1:]}})

        elif expr[0] == 'try':
            try:
                return evaluate(expr[1], env)
            except BaseException as e:
                return evaluate(expr[3], {**env, **{expr[2]: f'{e}'}})
        
        elif expr[0] == 'raise':
            raise Exception(evaluate(expr[1], env))

        elif expr[0] == 'require':
            if len(expr) == 2:
                env.update(script(expr[1] + '.syf', expr[1]))
            else:
                env.update(script(expr[1] + '.syf', expr[2]))

        elif expr[0] == '=>>':
            init = evaluate(expr[1], env)

            for lead in expr[2:]:
                func = evaluate(lead[0], env)
                args = [evaluate(arg, env) for arg in lead[1:]]
                
                init = func(*args, init)
            
            return init
        
        elif expr[0] == '<<=':
            init = evaluate(expr[1], env)
            
            for lead in expr[2:]:
                func = evaluate(lead[0], env)
                args = [evaluate(arg, env) for arg in lead[1:]]
                
                init = func(init, *args)
            
            return init
        
        elif expr[0] == 'assert':
            try:
                assert evaluate(expr[1], env)
            except:
                raise AssertionError(f"{evaluate(expr[2], env)}")

        # MACRO INTEGRATION
        elif expr[0] == 'macro':
            env['macro'] += [expr[1]]
            env[expr[1]] = lambda *args: evaluate(('do', *expr[3:]), {**env, **dict(zip(expr[2], args))})

        elif expr[0] == 'macro*':
            env['macro'] += [expr[1]]
            env[expr[1]] = lambda *args: evaluate(('do', *expr[3:]), {**env, **dict(zip(expr[2][:-1], args[:len(expr[2])-1])), **{expr[2][-1]: args[len(expr[2])-1:]}})

        elif expr[0] == 'macro/`':
            return unquote(expr[1], lambda i: evaluate(i, env))

        elif expr[0] in env['macro']:
            macro = evaluate(expr[0], env)
            args = expr[1:]

            return evaluate(macro(*args), env)

        # REGULAR FUNCTIONS
        else:
            func = evaluate(expr[0], env)
            args = [evaluate(arg, env) for arg in expr[1:]]

            return func(*args)
    
    # ATOMS
    elif isinstance(expr, str) and expr.startswith('"') and expr.endswith('"'):
        return expr[1:-1]
    
    elif isinstance(expr, str) and expr.replace('.', '', 1).isdigit():
        try:
            return int(expr)
        except:
            return float(expr)
    
    elif isinstance(expr, str) and expr in env.keys():
        return env[expr]
    
    else:
        if expr == None:
            raise Exception(f'couldn\'t evaluate macro, without unevaluated return')
        else:
            raise Exception(f'couldn\'t find value - {expr}')

# SPLIT BY LISP EXPRESSIONS
def split_balanced(text):
    expressions = []
    stack = []
    current_expression = ''

    for char in text:
        current_expression += char
    
        if char == '(':
            stack.append(char)
            
        elif char == ')':
            stack.pop()

            if not stack:
                expressions.append(current_expression)
                current_expression = ''
    
    return expressions

red   = '\u001b[1;31m'
reset = '\u001b[0m'

# EVALUATE FILES
def script(name, alias):
    local = std.copy()

    try:
        with open(name, 'r') as file:
            for index, expr in enumerate(split_balanced(uncomment(file.read()))):
                try:
                    evaluate(read(expr), local)
                except Exception as e:
                    print(f'{red}error - {name} : {index+1} - {str(e).lower()}{reset}')
    except FileNotFoundError:
        raise Exception(f'couldn\'t open file - {name}')

    updated_std = {key: value for key, value in local.items() if key in std and std[key] is not local[key]}
    updated_std = {key: value for key, value in std.items() if key not in updated_std}

    if alias == '*':
        return {key: value for key, value in local.items() if key not in updated_std}
    else:
        return {alias+'/'+key: value for key, value in local.items() if key not in updated_std}

# BOOTSTRAP
def bootstrap():
    source = """(macro* when (c b) (macro/`
    (if (macro/~ c)
        (macro/~@ do b)
        none)))

    (macro* for (i x b) (macro/`
        (list! (map
            (lambda ((macro/~ i)) (macro/~@ do b))
        (macro/~ x)))))

    (macro* while (c b) (macro/`
        (let (help (lambda ()
            (when (macro/~ c)
                (macro/~@ do b)
                (help))))
            (help))))

    ;; (macro if-let (b p c a) (macro/`
    ;;     (let ((macro/~ b) (macro/~ p))
    ;;         (if (macro/~ b)
    ;;             (macro/~ c)
    ;;             (macro/~ a)))))

    ;; (macro* when-let (b p c) (macro/`
    ;;     (let ((macro/~ b) (macro/~ p))
    ;;         (macro/~@ when p c))))"""

    for expr in split_balanced(uncomment(source)):
        evaluate(read(expr))
