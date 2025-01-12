; ModuleID = "main"
target triple = "x86_64-pc-windows-msvc"
target datalayout = ""

@"true" = constant i1 1
@"false" = constant i1 0
define i8* @"main"()
{
main_entry:
  %"mylist" = alloca [3 x i32]
  %".2" = getelementptr [3 x i32], [3 x i32]* %"mylist", i32 0, i32 0
  store i32 1, i32* %".2"
  %".4" = getelementptr [3 x i32], [3 x i32]* %"mylist", i32 0, i32 1
  store i32 2, i32* %".4"
  %".6" = getelementptr [3 x i32], [3 x i32]* %"mylist", i32 0, i32 2
  store i32 3, i32* %".6"
  %".8" = alloca [3 x i32]*
  store [3 x i32]* %"mylist", [3 x i32]** %".8"
  %".10" = load [3 x i32]*, [3 x i32]** %".8"
  %"arrtmp" = alloca [256 x i8]
  %"offset" = alloca i64
  store i64 0, i64* %"offset"
  %"buf_i8ptr" = getelementptr [256 x i8], [256 x i8]* %"arrtmp", i64 0, i64 0
  %"old_offset" = load i64, i64* %"offset"
  %"dest_ptr" = getelementptr i8, i8* %"buf_i8ptr", i64 %"old_offset"
  %".12" = call i32 (i8*, i8*, ...) @"sprintf"(i8* %"dest_ptr", i8* bitcast ([3 x i8]* @".str_5" to i8*), i8* bitcast ([2 x i8]* @".str_3" to i8*))
  %".13" = add i64 %"old_offset", 1
  store i64 %".13", i64* %"offset"
  %"elem_ptr_0" = getelementptr [3 x i32], [3 x i32]* %".10", i64 0, i32 0
  %"elem_val_0" = load i32, i32* %"elem_ptr_0"
  %"inttmp" = alloca [12 x i8]
  %"buf_i8ptr.1" = getelementptr [12 x i8], [12 x i8]* %"inttmp", i64 0, i64 0
  %".15" = call i32 (i8*, i8*, ...) @"sprintf"(i8* %"buf_i8ptr.1", i8* bitcast ([3 x i8]* @".str_6" to i8*), i32 %"elem_val_0")
  %"old_offset.1" = load i64, i64* %"offset"
  %"dest_ptr.1" = getelementptr i8, i8* %"buf_i8ptr", i64 %"old_offset.1"
  %".16" = call i32 (i8*, i8*, ...) @"sprintf"(i8* %"dest_ptr.1", i8* bitcast ([3 x i8]* @".str_7" to i8*), i8* %"buf_i8ptr.1")
  %"cstr_len" = call i64 @"strlen"(i8* %"buf_i8ptr.1")
  %".17" = add i64 %"old_offset.1", %"cstr_len"
  store i64 %".17", i64* %"offset"
  %"elem_ptr_1" = getelementptr [3 x i32], [3 x i32]* %".10", i64 0, i32 1
  %"elem_val_1" = load i32, i32* %"elem_ptr_1"
  %"old_offset.2" = load i64, i64* %"offset"
  %"dest_ptr.2" = getelementptr i8, i8* %"buf_i8ptr", i64 %"old_offset.2"
  %".19" = call i32 (i8*, i8*, ...) @"sprintf"(i8* %"dest_ptr.2", i8* bitcast ([3 x i8]* @".str_10" to i8*), i8* bitcast ([3 x i8]* @".str_9" to i8*))
  %".20" = add i64 %"old_offset.2", 2
  store i64 %".20", i64* %"offset"
  %"inttmp.1" = alloca [12 x i8]
  %"buf_i8ptr.2" = getelementptr [12 x i8], [12 x i8]* %"inttmp.1", i64 0, i64 0
  %".22" = call i32 (i8*, i8*, ...) @"sprintf"(i8* %"buf_i8ptr.2", i8* bitcast ([3 x i8]* @".str_11" to i8*), i32 %"elem_val_1")
  %"old_offset.3" = load i64, i64* %"offset"
  %"dest_ptr.3" = getelementptr i8, i8* %"buf_i8ptr", i64 %"old_offset.3"
  %".23" = call i32 (i8*, i8*, ...) @"sprintf"(i8* %"dest_ptr.3", i8* bitcast ([3 x i8]* @".str_12" to i8*), i8* %"buf_i8ptr.2")
  %"cstr_len.1" = call i64 @"strlen"(i8* %"buf_i8ptr.2")
  %".24" = add i64 %"old_offset.3", %"cstr_len.1"
  store i64 %".24", i64* %"offset"
  %"elem_ptr_2" = getelementptr [3 x i32], [3 x i32]* %".10", i64 0, i32 2
  %"elem_val_2" = load i32, i32* %"elem_ptr_2"
  %"old_offset.4" = load i64, i64* %"offset"
  %"dest_ptr.4" = getelementptr i8, i8* %"buf_i8ptr", i64 %"old_offset.4"
  %".26" = call i32 (i8*, i8*, ...) @"sprintf"(i8* %"dest_ptr.4", i8* bitcast ([3 x i8]* @".str_14" to i8*), i8* bitcast ([3 x i8]* @".str_13" to i8*))
  %".27" = add i64 %"old_offset.4", 2
  store i64 %".27", i64* %"offset"
  %"inttmp.2" = alloca [12 x i8]
  %"buf_i8ptr.3" = getelementptr [12 x i8], [12 x i8]* %"inttmp.2", i64 0, i64 0
  %".29" = call i32 (i8*, i8*, ...) @"sprintf"(i8* %"buf_i8ptr.3", i8* bitcast ([3 x i8]* @".str_15" to i8*), i32 %"elem_val_2")
  %"old_offset.5" = load i64, i64* %"offset"
  %"dest_ptr.5" = getelementptr i8, i8* %"buf_i8ptr", i64 %"old_offset.5"
  %".30" = call i32 (i8*, i8*, ...) @"sprintf"(i8* %"dest_ptr.5", i8* bitcast ([3 x i8]* @".str_16" to i8*), i8* %"buf_i8ptr.3")
  %"cstr_len.2" = call i64 @"strlen"(i8* %"buf_i8ptr.3")
  %".31" = add i64 %"old_offset.5", %"cstr_len.2"
  store i64 %".31", i64* %"offset"
  %"old_offset.6" = load i64, i64* %"offset"
  %"dest_ptr.6" = getelementptr i8, i8* %"buf_i8ptr", i64 %"old_offset.6"
  %".33" = call i32 (i8*, i8*, ...) @"sprintf"(i8* %"dest_ptr.6", i8* bitcast ([3 x i8]* @".str_18" to i8*), i8* bitcast ([2 x i8]* @".str_17" to i8*))
  %".34" = add i64 %"old_offset.6", 1
  store i64 %".34", i64* %"offset"
  %".36" = alloca i8*
  store i8* %"buf_i8ptr", i8** %".36"
  %".38" = load i8*, i8** %".36"
  %".39" = call i32 @"puts"(i8* %".38")
  ret i8* bitcast ([8 x i8]* @".str_20" to i8*)
}

@".str_3" = internal constant [2 x i8] c"[\00"
declare i32 @"sprintf"(i8* %".1", i8* %".2", ...)

@".str_5" = internal constant [3 x i8] c"%s\00"
@".str_6" = internal constant [3 x i8] c"%d\00"
@".str_7" = internal constant [3 x i8] c"%s\00"
declare i64 @"strlen"(i8* %".1")

@".str_9" = internal constant [3 x i8] c", \00"
@".str_10" = internal constant [3 x i8] c"%s\00"
@".str_11" = internal constant [3 x i8] c"%d\00"
@".str_12" = internal constant [3 x i8] c"%s\00"
@".str_13" = internal constant [3 x i8] c", \00"
@".str_14" = internal constant [3 x i8] c"%s\00"
@".str_15" = internal constant [3 x i8] c"%d\00"
@".str_16" = internal constant [3 x i8] c"%s\00"
@".str_17" = internal constant [2 x i8] c"]\00"
@".str_18" = internal constant [3 x i8] c"%s\00"
declare i32 @"puts"(i8* %".1")

@".str_20" = private constant [8 x i8] c"success\00"