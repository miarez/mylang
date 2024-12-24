; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

@"true" = constant i1 1
@"false" = constant i1 0
define i8* @"main"()
{
main_entry:
  %".2" = alloca [3 x i32]
  %".3" = getelementptr [3 x i32], [3 x i32]* %".2", i32 0, i32 0
  store i32 1, i32* %".3"
  %".5" = getelementptr [3 x i32], [3 x i32]* %".2", i32 0, i32 1
  store i32 2, i32* %".5"
  %".7" = getelementptr [3 x i32], [3 x i32]* %".2", i32 0, i32 2
  store i32 3, i32* %".7"
  %".9" = alloca [3 x i32]
  %".10" = load [3 x i32], [3 x i32]* %".2"
  store [3 x i32] %".10", [3 x i32]* %".9"
  %"int_str_buf" = alloca i8, i32 32
  %".12" = call i32 (i8*, i8*, ...) @"sprintf"(i8* %"int_str_buf", i8* bitcast ([3 x i8]* @"int_fmt" to i8*), i32 123)
  %".13" = call i32 @"puts"(i8* %"int_str_buf")
  %"float_str_buf" = alloca i8, i32 64
  %".14" = fpext float 0x405ed999a0000000 to double
  %".15" = call i32 (i8*, i8*, ...) @"sprintf"(i8* %"float_str_buf", i8* bitcast ([5 x i8]* @"float_fmt" to i8*), double %".14")
  %".16" = call i32 @"puts"(i8* %"float_str_buf")
  %".17" = call i32 @"puts"(i8* bitcast ([6 x i8]* @".str_7" to i8*))
  ret i8* bitcast ([8 x i8]* @".str_8" to i8*)
}

@"int_fmt" = private global [3 x i8] c"%d\00"
declare i32 @"sprintf"(i8* %".1", i8* %".2", ...)

declare i32 @"puts"(i8* %".1")

@"float_fmt" = private global [5 x i8] c"%.2f\00"
@".str_7" = private constant [6 x i8] c"hello\00"
@".str_8" = private constant [8 x i8] c"success\00"