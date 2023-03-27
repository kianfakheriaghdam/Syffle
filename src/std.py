from functools import reduce, partial
from itertools import accumulate

import sys, os

# BUILT-INS
std = {
    'abs'       : abs       ,
    'accumulate': accumulate,
    'all'       : all       ,
    'any'       : any       ,
    'ascii'     : ascii     ,
    'bin'       : bin       ,
    'chr'       : chr       ,
    'enumerate' : enumerate ,
    'exit'      : sys.exit  ,
    'filter'    : filter    ,
    'format'    : format    ,
    'hash'      : hash      ,
    'hex'       : hex       ,
    'iter'      : iter      ,
    'input'     : input     ,
    'len'       : len       ,
    'max'       : max       ,
    'min'       : min       ,
    'map'       : map       ,
    'next'      : next      ,
    'oct'       : oct       ,
    'ord'       : ord       ,
    'partial'   : partial   ,
    'print'     : print     ,
    'range'     : range     ,
    'round'     : round     ,
    'reduce'    : reduce    ,
    'reversed'  : reversed  ,
    'sorted'    : sorted    ,
    'type'      : type      ,
    'zip'       : zip       ,

    'take': lambda n, lst: lst[:n],
    'drop': lambda n, lst: lst[n:],

    'clear': lambda: os.system('cls') if sys.platform == 'win32' else os.system('clear')
}

def read(o):
    with open(o, 'r') as f:
        return f.read()

def write(o, a, w=True):
    m = 'w' if w else 'a'
    
    with open(o, m) as f:
        f.write(a)

# BUILT-IN METHODS
std.update({
    'split'   : lambda o, a: o.split    (a),
    'strip'   : lambda o, a: o.strip    (a),
    'rstrip'  : lambda o, a: o.rstrip   (a),
    'lstrip'  : lambda o, a: o.lstrip   (a),
    'join'    : lambda o, a: o.join     (a),
    'replace' : lambda o, a: o.replace  (a),
    'upper'   : lambda o   : o.upper    ( ),
    'lower'   : lambda o   : o.lower    ( ),
    'alnum?'  : lambda o   : o.isalnum  ( ),
    'alpha?'  : lambda o   : o.isalpha  ( ),
    'ascii?'  : lambda o   : o.isascii  ( ),
    'decimal?': lambda o   : o.isdecimal( ),
    'digit?'  : lambda o   : o.isdigit  ( ),
    'lower?'  : lambda o   : o.islower  ( ),
    'numeric?': lambda o   : o.isnumeric( ),
    'upper?'  : lambda o   : o.isupper  ( ),
    'index'   : lambda o, a: o.index    (a),
    'rindex'  : lambda o, a: o.rindex   (a),
    'count'   : lambda o, a: o.count    (a),
    'keys'    : lambda o, a: o.keys     ( ),
    'values'  : lambda o, a: o.values   ( ),
    'update'  : lambda o, a:  {**o,   **a} ,
    'copy'    : lambda o   :   o.copy()    ,
    'write'   : write                      ,
    'read'    : read
})

# BUILT-IN DATA TYPES
std.update({
    'int'  : int  ,
    'float': float,
    'str'  : str  ,
    'bool' : bool ,
    'true' : True ,
    'false': False,
    'none' : None ,

    'list' : lambda *args: list (args),
    'tuple': lambda *args: tuple(args),
    'set'  : lambda *args: set  (args),

    'list!' : list ,
    'tuple!': tuple,
    'set!'  : set  ,

    'dict' : lambda *args: dict(*args) if len(args) == 1 else {args[i]: args[i+1] for i in range(0, len(args), 2)},
    'dict!': dict,

    'bytes': bytes,
    'byte-array': bytearray
})

import operator

# BUILT-IN OPERATORS
std.update({
    '+' : lambda *args: operator.pos(args[0]) if len(args) == 1 else reduce(operator.add, args),
    '-' : lambda *args: operator.neg(args[0]) if len(args) == 1 else reduce(operator.sub, args),

    '*' : lambda *args: reduce(operator.mul     , args),
    '/' : lambda *args: reduce(operator.truediv , args),
    '%' : lambda *args: reduce(operator.mod     , args),
    '**': lambda *args: reduce(operator.pow     , args),
    '//': lambda *args: reduce(operator.floordiv, args),

    '=' : lambda *args: reduce(operator.eq, args),
    '!=': lambda *args: reduce(operator.ne, args),
    '<' : lambda *args: reduce(operator.lt, args),
    '>' : lambda *args: reduce(operator.gt, args),
    '<=': lambda *args: reduce(operator.le, args),
    '>=': lambda *args: reduce(operator.ge, args),

    '<<': lambda *args: reduce(operator.lshift, args),
    '>>': lambda *args: reduce(operator.rshift, args),

    '&': lambda *args: reduce(operator.and_, args),
    '|': lambda *args: reduce(operator.or_ , args),
    '^': lambda *args: reduce(operator.xor , args),
    '~': operator.inv,

    '@': lambda *args: reduce(operator.matmul, args),

    'and': lambda *args: reduce(lambda x, y: x and y, args),
    'or' : lambda *args: reduce(lambda x, y: x or  y, args),
    'not': operator.not_,

    'in?': lambda *args: reduce(operator.contains, args),
    'nth': lambda a, b: a[b],

    'del': lambda d, x: {k: v for k, v in d.items() if k != x},

    'inc': lambda x: x + 1,
    'dec': lambda x: x - 1
})

# PYTHON INTEGRATION
std.update({
    'py/.' : lambda o, *args: reduce(lambda x, y: getattr(x, y), args, o),
    'py/=' : setattr,

    'py/*' : lambda f, o: f(*o ),
    'py/**': lambda f, o: f(**o),
    'py/***': lambda f, o, k: f(*o, **k),

    'py/eval': eval,
    'py/exec': exec,

    'py/import': __import__
})

# SYSTEM INTEGRATION
std.update({
    'system': os.system,

    'system/args': sys.argv,

    'system/error': sys.stderr.write,
    'system/flush': sys.stdout.flush,
    
    'system/platform': sys.platform,
    'system/version' : '0.0.1',

    'system/cwd'  : os.getcwd,
    'system/cwd/=': os.chdir,

    'system/environ': os.environ,
    'system/list-dir': os.listdir,
})

import asyncio

# TODO - ASYNCHRONOUS INTEGRATION
std.update({
})

import threading
import queue, time

# THREADING INTEGRATION
std.update({
    'thread'       : lambda t, *args: threading.Thread(target=t, args=args), 
    'thread/daemon': lambda t, *args: threading.Thread(target=t, args=args, daemon=True),

    'thread/start': lambda t: t.start(),
    'thread/await': lambda t: t.join(),

    'thread/chan': queue.Queue,
    'thread/>!'  : lambda q, v: q.put(v),
    'thread/<!'  : lambda q: q.get(),

    'thread/sleep': time.sleep,
})

# MACRO INTEGRATION
std.update({
    'macro': []
})

class Mut:
    def __init__(self, value):
        self.value = value
    
    def set(self, value):
        self.value = value

    def get(self):
        return self.value

# MUT INTEGRATION
std.update({
    'mut': lambda v: Mut(v),
    
    'mut/!': lambda o: o.get(),
    'mut/=': lambda o, v: o.set(v),

    'mut/+=': lambda o, v: o.set(o.get() + v),
    'mut/-=': lambda o, v: o.set(o.get() - v),
    'mut/*=': lambda o, v: o.set(o.get() * v),
    'mut//=': lambda o, v: o.set(o.get() / v),
    'mut/%=': lambda o, v: o.set(o.get() % v),

    'mut/**=': lambda o, v: o.set(o.get() ** v),
    'mut///=': lambda o, v: o.set(o.get() // v),

    'mut/<<=': lambda o, v: o.set(o.get() << v),
    'mut/>>=': lambda o, v: o.set(o.get() >> v),
    'mut/&=' : lambda o, v: o.set(o.get() & v),
    'mut/|=' : lambda o, v: o.set(o.get() | v),
    'mut/^=' : lambda o, v: o.set(o.get() ^ v),

    'mut/++': lambda o: o.set(o.get() + 1),
    'mut/--': lambda o: o.set(o.get() - 1)
})

import requests

# NET INTEGRATION
std.update({
    'slurp': lambda w: requests.get(w).text
})

import json

# JSON INTEGRATION
std.update({
    'json/loads': json.loads,
    'json/dumps': json.dumps
})

import math

def is_prime(x):
    for i in range(2, x):
        if (x % i) == 0:
            return False
        
    return True

# MATH INTEGRATION
std.update({
    'math/floor': math.floor,
    'math/ceil' : math.ceil ,

    'math/factorial': math.factorial,

    'math/pi'     : math.pi     ,
    'math/radians': math.radians,
    'math/degrees': math.degrees,

    'math/gcd': math.gcd,
    'math/lcm': lambda x, y: (x * y) / math.gcd(x, y),

    'math/sqrt': math.sqrt,
    'math/cbrt': lambda x: x ** (1/3),

    'math/log'  : math.log  ,
    'math/log2' : math.log2 ,
    'math/log10': math.log10,
    'math/log1p': math.log1p,
    'math/exp'  : math.exp  ,
    'math/e'    : math.e    ,

    'math/sin'  : math.sin  ,
    'math/sinh' : math.sinh ,
    'math/asin' : math.asin ,
    'math/asinh': math.asinh,
    'math/cos'  : math.cos  ,
    'math/cosh' : math.cosh ,
    'math/acos' : math.acos ,
    'math/acosh': math.acosh,
    'math/tan'  : math.tan  ,
    'math/tanh' : math.tanh ,
    'math/atan' : math.atan ,
    'math/atanh': math.atanh,

    'math/tau': math.tau,

    'math/nan' : math.nan  ,
    'math/inf' : math.inf  ,
    'math/nan?': math.isnan,
    'math/inf?': math.inf  ,

    'math/even?' : lambda x: x % 2 == 0,
    'math/odd?'  : lambda x: x % 2 == 1,
    'math/prime?': is_prime
})

import decimal

# DECIMAL INTEGRATION
std.update({
    'decimal': decimal.Decimal,

    'decimal/exp'  : lambda o: o.exp  (),
    'decimal/ln'   : lambda o: o.ln   (),
    'decimal/log10': lambda o: o.log10(),

    'decimal/sqrt': lambda o: o.sqrt(),

    'decimal/max': lambda o, v: o.max(v),
    'decimal/min': lambda o, v: o.min(v),

    'decimal/&': lambda o, v: o.logical_and(v),
    'decimal/|': lambda o, v: o.logical_or (v),
    'decimal/^': lambda o, v: o.logical_xor(v),

    'decimal/~': lambda o: o.logical_invert()
})

# COMPLEX INTEGRATION
std.update({
    'complex': complex,

    'complex/real': lambda o: o.real,
    'complex/imag': lambda o: o.imag,
})

import datetime, jdatetime
from pytz import timezone

# DATE INTEGRATION
std.update({
    'date': datetime.datetime,

    'date/now'  : lambda t=None:  datetime.datetime.now(t),
    'date/j-now': lambda t=None: jdatetime.datetime.now(t),

    'date/time-zone' : timezone,
    'date/time-delta': datetime.timedelta,

    'date/strftime': lambda o, v: o.strftime(v),
    'date/strptime': lambda o, v: o.strptime(v)
})

import pickle

# PICKLE INTEGRATION
std.update({
    'pickle/loads': pickle.loads,
    'pickle/dumps': pickle.dumps
})
