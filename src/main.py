import sys
sys.setrecursionlimit(2147483647)

from evaluate import evaluate
from read import read

from evaluate import script

red    = '\u001b[1;31m'
green  = '\u001b[1;32m'
yellow = '\u001b[1;33m'
reset  = '\u001b[0m'

# BOOTSTRAP
from evaluate import bootstrap
bootstrap()

# READ, EVALUATE, PRINT & LOOP
if sys.platform != 'win32':
    import readline

def repl():
    while True:
        try:
            prompt = input(f'{yellow}!{reset} ')
            if prompt.strip() == '': continue

            result = evaluate(read(prompt))

            if result != None:
                print(f'{green}{result}{reset}')

        except KeyboardInterrupt:
            sys.exit()

        except EOFError:
            sys.exit()

        except Exception as e:
            print(f'{red}error - {str(e).lower()}{reset}')

if __name__ == '__main__':
    
    if len(sys.argv) == 1:
        print(f'{yellow}Syffle 0.0.1 - Kian Fakheri Aghdam')
        print(f'(exit)')
        repl()

    else:
        if sys.argv[1] == '--version':
            print('Syffle 0.0.1 - Kian Fakheri Aghdam')
        else:
            script(sys.argv[1], sys.argv[1].split('.')[0])
