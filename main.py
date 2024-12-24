from src.lexer.Lexer import Lexer
from src.parser.Parser import Parser
from src.compiler.Compiler import Compiler
from src.ast.Program import Program
import json
import time

from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float, c_char_p

LEXER_DEBUG: bool = False 
PARSER_DEBUG: bool = True
COMPILER_DEBUG: bool = True

RUN_CODE = True

with open("tests/lists.line", "r") as f:
    code:str = f.read()

print(code)

if LEXER_DEBUG:
    print("============= LEXER DEBUG ================= ")
    debug_lex = Lexer(source=code)
    while debug_lex.current_char is not None:
        print(debug_lex.next_token())

lexer: Lexer = Lexer(source=code)
parser: Parser = Parser(lexer=lexer)

program: Program = parser.parse_program()
if len(parser.errors) > 0:
    for err in parser.errors:
        print(err)
    exit(1)

if PARSER_DEBUG:
    print("============= PARSER DEBUG ================= ")

    with open("debug/ast.json", "w") as f:
        json.dump(program.json(), f, indent=4)
    print("Wrote AST To debug/AST.json")
    
compiler: Compiler = Compiler()
compiler.compile(node=program)

module: ir.Module = compiler.module
# target architecture
module.triple = llvm.get_default_triple()

if COMPILER_DEBUG:
    print("============= COMPILER_DEBUG DEBUG ================= ")
    with open("debug/ir.ll", "w") as f:
        f.write(str(module))
    print("Wrote module To debug/ir.ll")

if RUN_CODE:
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    try:
        llvm_ir_parsed = llvm.parse_assembly(str(module))
        llvm_ir_parsed.verify()
    except Exception as e:
        print(e)
        raise

    target_machine = llvm.Target.from_default_triple().create_target_machine()

    engine = llvm.create_mcjit_compiler(llvm_ir_parsed, target_machine)
    engine.finalize_object()

    # entry = engine.get_function_address('main') # access point function
    # cfunction = CFUNCTYPE(c_int)(entry)
    # start_time = time.time()
    # result = cfunction() 
    # end_time = time.time()
    # print(f"\n\n Program Returned : {result} \n === Executed In {round(end_time-start_time*1000, 6)} ms. ===")

    entry = engine.get_function_address('main')
    cfunction = CFUNCTYPE(c_char_p)(entry)
    start_time = time.time()
    result_ptr = cfunction()
    end_time = time.time()
    print(result_ptr.decode('utf-8')) 



