; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

@"true" = constant i1 1
@"false" = constant i1 0
define i32 @"add"(i32 %".1", i32 %".2")
{
add_entry:
  %".4" = alloca i32
  store i32 %".1", i32* %".4"
  %".6" = alloca i32
  store i32 %".2", i32* %".6"
  %".8" = load i32, i32* %".4"
  %".9" = load i32, i32* %".6"
  %".10" = add i32 %".8", %".9"
  ret i32 %".10"
}

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
  %".2" = call i8* @"sayHello"(i8* bitcast ([12 x i8]* @".str_5" to i8*))
  %".3" = alloca i8*
  store i8* %".2", i8** %".3"
  %".5" = call i32 @"add"(i32 10, i32 10)
  %".6" = alloca i32
  store i32 %".5", i32* %".6"
  %".8" = load i8*, i8** %".3"
  ret i8* %".8"
}

@".str_5" = private constant [12 x i8] c"hello world\00"