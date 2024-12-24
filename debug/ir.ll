; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

@"true" = constant i1 1
@"false" = constant i1 0
define i8* @"sayHello"(i8* %".1")
{
sayHello_entry:
  %".3" = alloca i8*
  store i8* %".1", i8** %".3"
  %".5" = load i8*, i8** %".3"
  ret i8* %".5"
}

define i8* @"main"()
{
main_entry:
  %".2" = call i8* @"sayHello"(i8* bitcast ([12 x i8]* @".str_4" to i8*))
  %".3" = alloca i8*
  store i8* %".2", i8** %".3"
  %".5" = call i32 @"puts"(i8* bitcast ([102 x i8]* @".str_5" to i8*))
  ret i8* bitcast ([11 x i8]* @".str_7" to i8*)
}

@".str_4" = private constant [12 x i8] c"hello world\00"
@".str_5" = private constant [102 x i8] c"hello world is a very long sentence and I want to make sure that it works of any lengths to be honest\00"
declare i32 @"puts"(i8* %".1")

@".str_7" = private constant [11 x i8] c"it worked!\00"