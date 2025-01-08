## Language Features v0.1

v0.1 aims to provide all the basic functionality of a language such as:

- [x] lexer
- [x] ast
- [x] parser
- [x] interpreter

The goal is to create a turing-complete-esque language that we can begin to use & benchmark

### Must Haves:

- [ ] Nested block statements
  - `<block> :: = <statement> | {  [<block>]*  }`
- [x] OOP Based src directory layout
- [ ] ELI5-esque comments
- [x] string type
- [x] list type
- [ ] loop/enumeration
- [x] builtin functions functionality
- [ ] Type System (vectors, frames, etc)

### Nice To Haves:

- [ ] string variable interpolation
- [ ] Virtual console
- [ ] Error Handling
- [ ] datemath syntax (now-2w+1h/s)
- [ ] Negation
- [ ] elseif
- [ ] Interpreter Functionality
- [ ] Automatic Semicolon Insertion (ASI)

### v0.1 Builtins:

- [ ] IO
  - [x] print, printf
- [ ] String
    - [x] interpolation (sprintf)
- [ ] Mathematics and Arithmetic
  - [ ] Basic Arithmetic:
    - [ ] add
    - [ ] subtract
    - [ ] multiply
    - [ ] divide
  - [ ] Advanced Math:
    - [ ] pow
    - [ ] sqrt
    - [ ] log
    - [ ] exp

## Features v0.2

v0.2 will aim to standardize the syntax and how you interact with the language

- [ ] llvm IR compiler
- [ ] vectorized execution
- [ ] Dynamic Main Wrapping
- [ ] Incremental Compilation
- [ ] Rich Main Function return types (structured return objects)
- [ ] optional semicolon
- [ ] Pipping
- [ ] Currying / Partial Application
- [ ] BNR Representation
- [ ] OOP

- List Comprehension
  - ` [p.value for p in parameters]`

## Features v0.3

- [ ] concurrency
- [ ] asynchronousity / event loops

## MISC TO DO:

- [ ] function/variable name collision?

---

## Full BuiltIns List

## - [ ] Mathematics and Arithmetic

### - [ ] Basic Arithmetic

- [ ] `add`: Adds two numbers.
- [ ] `subtract`: Subtracts the second number from the first.
- [ ] `multiply`: Multiplies two numbers.
- [ ] `divide`: Divides the first number by the second.

### - [ ] Advanced Math

- [ ] `pow`: Raises a number to the power of another.
- [ ] `sqrt`: Calculates the square root of a number.
- [ ] `log`: Computes the natural logarithm of a number.
- [ ] `exp`: Calculates `e` raised to the power of a number.

---

## - [ ] String Operations

### - [ ] Case Conversion

- [ ] `toUpperCase`: Converts a string to uppercase.
- [ ] `toLowerCase`: Converts a string to lowercase.

### - [ ] Trimming

- [ ] `trim`: Removes whitespace from both ends of a string.
- [ ] `ltrim`: Removes whitespace from the start of a string.
- [ ] `rtrim`: Removes whitespace from the end of a string.

### - [ ] Substring Extraction

- [ ] `substr`: Extracts a substring given a start position and length.
- [ ] `substring`: Extracts a substring between two positions.
- [ ] `slice`: Extracts a section of a string.

### - [ ] Searching

- [ ] `indexOf`: Finds the position of a substring in a string.
- [ ] `contains`: Checks if a string contains a substring.
- [ ] `startsWith`: Checks if a string starts with a given substring.
- [ ] `endsWith`: Checks if a string ends with a given substring.

### - [ ] Joining/Splitting

- [ ] `join`: Joins an array of strings into a single string.
- [ ] `split`: Splits a string into an array of substrings.
- [ ] `concat`: Concatenates multiple strings into one.

---

## - [ ] Input/Output (I/O)

### - [ ] Console

- [ ] `print`: Outputs a value to the console.
- [ ] `readInput`: Reads input from the user.

### - [ ] File Operations

- [ ] `readFile`: Reads a file and returns its contents.
- [ ] `writeFile`: Writes data to a file.
- [ ] `appendFile`: Appends data to an existing file.
- [ ] `deleteFile`: Deletes a file from the system.

---

## - [ ] Data Structures

### - [ ] Array Operations

- [ ] `map`: Applies a function to each element in an array.
- [ ] `filter`: Returns elements that satisfy a condition.
- [ ] `reduce`: Reduces an array to a single value using a function.
- [ ] `sort`: Sorts an array.
- [ ] `reverse`: Reverses the order of elements in an array.

### - [ ] Map Operations

- [ ] `get`: Retrieves a value by key.
- [ ] `set`: Associates a value with a key.
- [ ] `keys`: Returns all keys in the map.
- [ ] `values`: Returns all values in the map.

### - [ ] Set Operations

- [ ] `union`: Combines two sets.
- [ ] `intersection`: Finds common elements between two sets.
- [ ] `difference`: Finds elements in one set but not the other.

---

## - [ ] Date and Time

### - [ ] Basic Operations

- [ ] `now`: Returns the current date and time.
- [ ] `today`: Returns the current date.

### - [ ] Formatting

- [ ] `formatDate`: Formats a date using a specified format.
- [ ] `toISOString`: Converts a date to an ISO 8601 string.

### - [ ] Arithmetic

- [ ] `addDays`: Adds a number of days to a date.
- [ ] `subtractDays`: Subtracts a number of days from a date.
- [ ] `differenceInDays`: Calculates the difference in days between two dates.

---

## - [ ] Operating System

### - [ ] Environment

- [ ] `getEnv`: Retrieves the value of an environment variable.
- [ ] `setEnv`: Sets the value of an environment variable.

### - [ ] Process Management

- [ ] `exit`: Terminates the current process.
- [ ] `exec`: Executes a system command.
- [ ] `spawn`: Starts a new process.

---

## - [ ] Math/Linear Algebra

### - [ ] Vector Operations

- [ ] `dot`: Computes the dot product of two vectors.
- [ ] `cross`: Computes the cross product of two vectors.
- [ ] `add`: Adds two vectors element-wise.
- [ ] `subtract`: Subtracts two vectors element-wise.

### - [ ] Matrix Operations

- [ ] `transpose`: Transposes a matrix.
- [ ] `multiply`: Multiplies two matrices.
- [ ] `inverse`: Calculates the inverse of a matrix.

---

## - [ ] System and Debugging

### - [ ] Debugging

- [ ] `assert`: Validates a condition and raises an error if false.
- [ ] `log`: Outputs a debug message.
- [ ] `debug`: Starts a debugging session.

### - [ ] Introspection

- [ ] `typeOf`: Returns the type of a value.
- [ ] `sizeOf`: Returns the size of a value in memory.

---

## - [ ] Utility Functions

### - [ ] Random

- [ ] `random`: Generates a random float between 0 and 1.
- [ ] `randInt`: Generates a random integer within a range.
- [ ] `seed`: Seeds the random number generator.

### - [ ] UUID

- [ ] `uuid`: Generates a unique identifier.

---

## - [ ] Type Conversion

### - [ ] Conversion Functions

- [ ] `toString`: Converts a value to a string.
- [ ] `toInt`: Converts a value to an integer.
- [ ] `toFloat`: Converts a value to a float.
- [ ] `toBool`: Converts a value to a boolean.

---

## - [ ] Error Handling

### - [ ] Error Functions

- [ ] `tryCatch`: Executes code and catches any exceptions.
- [ ] `throw`: Raises a user-defined error.
- [ ] `assert`: Ensures a condition is true; raises an error otherwise.

## OLD Brainstorming Document

# My Dream Language

## R Influence

### Auto complete on dataframe colums

typing
`df. `

would autocomplete different column names within the df

### Implicit Output / Immediate Evaluation

automatically evaluate and display the result of any expression entered

### Block (cursor and highlight) Execution

Run code selectively by placing the cursor or highlighting it

### Data First & Piping

```r
filter(df, cyl == 6)
# can be piped instead
df | filter(cyl == 6)
```

### Variadic Functions

can accept a variable number of arguments

```
function filter(df, ...)
```

### Rank Polymorphism / Type-Driven Dispatch

automatically adapt the function's behavior based on the structure of the input data, making operations seamless across scalars, vectors, dataframes, or other structures.

### Multiple Dispatch

Function behavior depends on the types of all arguments

```
add int int -> int (adds to integers together)
add str str -> str (concats two strings together)
```

### Vectorized Operations / Array Programming

allows you to perform operations on entire arrays without loops.

### Non-Standard Evaluation (NSE)

`filter(mtcars, cyl == 6)`

### R styled dataframe slicing

`df[, -1]`

## Lucene Influence

### Date Math

Operations like now-1d/W

## APL Influence

## Haskell/Ramda.js Influence

### Higher Order functions

### Functions as first class citizens

### Automatic Function Currying

## Type System

## OOP Paradigm

### Nested classes

## Comments:

```
-- this is a valid comment
# this is a valid comment
// this is a valid comment

/*
this is a block comment
*/
```

## MISC

### Automatic Return of last expression from expression/function

```
clean_table = df -> io (
    filter(df, ctr <= 100) |
    table
)

```

```
-- on the sales column, do the percent of total of the sales column
df.sales_vol_share = df.sales.percent_of_total()

-- alternatively, you can do of another column like:
df.sales_vol_share = df.sales.percent_of_total(net_sales)

```

df['moving_avg'] = df['sales'].rolling(window=3).mean()
df['rank'] = df['sales'].rank(ascending=False)
