# Syffle
Syffle is a LISP dialect, highly compatible with Python that is going to receive proper documentation & icon one day.

# Installation
make sure that you have the latest Python & PIP installed. install the `requests`, `jdatetime` & `pytz` PIP packages.

then clone this repository & either use `python3 src/main.py` or `python src/main.py` based on your operating system.

it will open the interpreter, if no command-line argument is provided. it expects a file.syf as its argument. `--version` is also permitted.

# Basics
the language is made out of atoms & function calls. unlike some LISP dialects like Clojure, there is no other special syntax & it's just simple LISP.

## Atoms
### Integers
these are numbers, without decimal points, such as `1`, `2`, `0`, `-3` & ... 
### Floats
these are numbers with decimal places, without good precision. (arithmetic operations may not be entirely correct) these are numbers, such as `1.2`, `.2`, `1.`, `-3.4` & ... 
### Strings
a string is a list of characters, enclosed in double quotes. (`"`) for example `"Hello, world!"`.
#### Escape Sequences
some characters cannot be presented in a string, hence escape sequences are used, which are characters with a back slash (`\`) to indicate those characters. the following is a list of these characters.
* `\'` single quotes
* `\"` double quotes
* `\n` new line
* `\t` tab
* `\r` return feed
* `\b` back space
* `\\` back slash

## Function Calls
LISP dialects use the Polish Notation, which instead of `f(arg1, arg2, arg3, ...)`, `(f arg1 arg2 arg3 ...)` is used. these concludes even operators, which are just functions. for example `(+ 1 2)`, `(* (- 2 1) 3)` & ...

### Naming Identifiers
LISP dialects use `kebab-case`. unlike other languages, LISP dialects don't have any restrictions on names, due to the simplicity of the syntax. Syffle extends this freedom more, by making the already simple syntax, more simple. hence names with `` ` ``, `~`, `[]`, `{}` & `'` are allowed.

## Comments
single line comments are allowed by `;`.

# Special Functions
the whole language is based around function calls. special functions are actually macros that make using the language possible.
```racket
(define x 10)
x ; 10
```
```clojure
(let (x 10 y x)
    (print x) ; 10
    (+ x y))  ; 20
```
```clojure
(do
    (print "Hello, world!") ; Hello, world!
    10)                     ; 10
```
```clojure
(if (even? 4)
    "yes"
    "no") ; "yes"
```
```clojure
(when true
    (print "yes") ; yes
    "no")         ; "no"
```
```clojure
(cond
    true  1
    false 2
    true  3
    true  4)
```
```clojure
(for i (range 1 6)
    (print i)) ; 1 2 3 4 5

(while true
    (print "yes")  ; yes
    (print "no" )) ; no
                   ; yes
                   ; ...
```
```racket
((lambda (x y)
    (print x)     ; 1
    (+ x y)) 1 2) ; 3
```
```clojure
((lambda* (x args) (+ x (reduce + args))) 1 2 3) ; 6
```
```clojure
(fun func (x y) ; fun* is used for variadic
    (print x)
    (print y))

(func 2 2) ; 2
           ; 2
```
```clojure
(try (/ 1 0) - 0) ; 0
```
```clojure
(try (raise "error!") error error) ; "error!"
```
```clojure
(assert (= 1 1) "1")
(assert false   "2") ; error - 2
```
*lib.syf*
```racket
(define x 10)
```
*main.syf*
```clojure
(require lib)
lib/x ; 10

(require lib l)
l/x ; 10

(require lib *)
x ; 10
```
```clojure
(=>> (list 1 2 3) ; <<= is used for replacing the first arguments
    (map inc)
    (filter math/even?)
    (list!)) ; [2, 4]
```

# Macros
macros, meta-programming, code that writes code & ... but how does it work?

`` macro/` `` will stop evaluation, except for pieces that use `macro/~`.
```racket
(define x 10)
(macro/` (list 1 2 3 (macro/~ x))) ; ('list', '1', '2', '3', 10)
```
`macro` & `macro*` are just like `fun` & `fun*`, except how they will mark their function as a macro. when a function is marked as a macro, the arguments won't get evaluated & it must always return unevaluated code. the unevaluated code is then evaluated.

`macro/~@` will evaluated a list of unevaluated c & apply it to a function, when used inside `` macro/` ``.

with the current knowledge, lets make a fork of the `while` & `for` macros. notice how you can make a recursive unevaluated code, but you can't make the macro itself recursive & how you can use identifiers.
```clojure
(macro* while' (c b) (macro/`
    (let (help (lambda ()
        (when (macro/~ c)
            (macro/~@ do b)
            (help))))
        (help))))

(macro* for' (i x b) (macro/`
    (list! (map
        (lambda ((macro/~ i)) (macro/~@ do b))
    (macro/~ x)))))
```
`macro/eval` is just like `py/eval`, but for Syffle code. you can also configure the bindings.
```clojure
(macro/eval "(+ x y)" "x" 10 "y" 20) ; 30
```

# Python Integration
`py/import` is used for importing Python default modules & PIP modules.
`py/.` gets attributes, while `py/=` sets attributes of a Python object.
`py/eval` & `py/exec` are `eval` & `exec` Python builtin functions.
`py/*` spreads a list into a function's arguments & executes the function. `py/**` does the same, but for dictionaries & `py/***` spreads a list & a dictionary.
```racket
(define tkinter (py/import "tkinter"))

(define tk (py/. tkinter "Tk"))

(define root (tk))
((py/. root "title") "Hello, world!")
((py/. root "geometry") "300x200")

((py/, root "mainloop"))
```

# Standard Library
`abs       ` `accumulate` `all       ` `any       ` `ascii     ` `bin       ` `chr       ` `enumerate ` `exit      ` `filter    ` `format    ` `hash      ` `hex       ` `iter      ` `input     ` `len       ` `max       ` `min       ` `map       ` `next      ` `oct       ` `ord       ` `partial   ` `print     ` `range     ` `round     ` `reduce    ` `reversed  ` `sorted    ` `type      ` `zip       `

`take` `drop` `inc` `dec` `slurp` `clear`

`split   ` `strip   ` `rstrip  ` `lstrip  ` `join    ` `replace ` `upper   ` `lower   ` `alnum?  ` `alpha?  ` `ascii?  ` `decimal?` `digit?  ` `lower?  ` `numeric?` `upper?  ` `index   ` `rindex  ` `count   ` `keys    ` `values  ` `update  ` `copy    ` `write   ` `read    `

`int` `float``str`  `bool` `true` `false` `none` `list` `tuple` `set` `list!` `tuple!` `set!` `dict` `dict!` `bytes` `byte-array`

`+` `-` `*` `/` `%` `**` `//` `=` `!=` `<` `<=` `>` `>=` `<<` `>>` `&` `|` `^` `~` `@` `and` `or` `not` `in?` `nth` `del`

`system` `system/args` `system/error` `system/flush` `system/platform` `system/version` `system/cwd` `system/cwd/=` `system/environ` `system/list-dir`

`thread` `thread/daemon` `thread/start` `thread/await` `thread/chan` `thread/>!` `thread/<!` `thread/sleep`

`mut` `mut/!` `mut/=` `mut/+=` `mut/-=` `mut/*=` `mut//=` `mut/%=` `mut/**=` `mut///=` `mut/<<=` `mut/>>=` `mut/&=` `mut/|=` `mut/^=` `mut/++` `mut/--`

`json/loads` `json/dumps`

`pickle/loads` `pickle/dumps`

`math/floor` `math/ceil` `math/factorial` `math/pi` `math/radians` `math/degrees` `math/gcd` `math/lcm` `math/sqrt` `math/cbrt` `math/log` `math/log2` `math/log10` `math/log1p` `math/exp` `math/e` `math/sin` `math/sinh` `math/asin` `math/asinh` `math/cos` `math/cosh` `math/acos` `math/acosh` `math/tan` `math/tanh` `math/atan` `math/atanh` `math/tau` `math/nan` `math/inf` `math/nan?` `math/inf?` `math/even?` `math/odd?` `math/prime?`

`decimal` `decimal/exp` `decimal/ln` `decimal/log10` `decimal/sqrt` `decimal/max` `decimal/min` `decimal/&` `decimal/|` `decimal/^` `decimal/~`

`complex` `complex/real` `complex/imag`

`date` `date/now` `date/j-now` `date/time-zone` `date/time-delta` `date/strftime` `date/strptime`
