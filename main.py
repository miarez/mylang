from src.lexer.Lexer import Lexer
from src.parser.Parser import Parser
# from src.compiler.Compiler import Compiler
from src.ast.Program import Program
from src.interpreter.Interpreter import Interpreter
import json
import time

# from llvmlite import ir
# import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float, c_char_p

LEXER_DEBUG: bool = False 
RUN_CODE = True

with open("tests/block_statements.line", "r") as f:
    code:str = f.read()

print(f" Source Code: \n {code}")


print("--- RUNNING LEXER")    
lexer = Lexer(source=code)

if LEXER_DEBUG:
    print("============= LEXER DEBUG ================= ")    
    while lexer.current_char is not None:
        print(lexer.next_token())

print("--- RUNNING PARSER")    

parser: Parser = Parser(lexer=lexer)

program: Program = parser.parse_program()
if len(parser.errors) > 0:
    print("============= PARSER ERRORS FOUND ================= ")
    for err in parser.errors:
        print(err)
    exit(1)

with open("debug/ast.json", "w") as f:
    json.dump(program.json(), f, indent=4)
print("Wrote AST To debug/AST.json")


if RUN_CODE:
    interpreter = Interpreter()
    result = interpreter.interpret(program)
    print("Program result:", result)

# compiler: Compiler = Compiler()
# compiler.compile(node=program)

# module: ir.Module = compiler.module
# # target architecture
# module.triple = llvm.get_default_triple()

# if COMPILER_DEBUG:
#     print("============= COMPILER_DEBUG DEBUG ================= ")
#     with open("debug/ir.ll", "w") as f:
#         f.write(str(module))
#     print("Wrote module To debug/ir.ll")

# if RUN_CODE:
#     llvm.initialize()
#     llvm.initialize_native_target()
#     llvm.initialize_native_asmprinter()

#     try:
#         llvm_ir_parsed = llvm.parse_assembly(str(module))
#         llvm_ir_parsed.verify()
#     except Exception as e:
#         print(e)
#         raise

#     target_machine = llvm.Target.from_default_triple().create_target_machine()

#     engine = llvm.create_mcjit_compiler(llvm_ir_parsed, target_machine)
#     engine.finalize_object()

#     # entry = engine.get_function_address('main') # access point function
#     # cfunction = CFUNCTYPE(c_int)(entry)
#     # start_time = time.time()
#     # result = cfunction() 
#     # end_time = time.time()
#     # print(f"\n\n Program Returned : {result} \n === Executed In {round(end_time-start_time*1000, 6)} ms. ===")

#     entry = engine.get_function_address('main')
#     cfunction = CFUNCTYPE(c_char_p)(entry)
#     start_time = time.time()
#     result_ptr = cfunction()
#     end_time = time.time()
#     print(result_ptr.decode('utf-8')) 



