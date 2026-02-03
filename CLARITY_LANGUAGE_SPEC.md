# Clarity Language Specification

## Overview
Clarity is a modern, general-purpose programming language designed for safety, readability, and performance. It combines the simplicity of Python with the safety guarantees of Rust, making it ideal for both learning and production use.

## Core Principles
1. **Safety by design** - Prevent common programming errors at compile time
2. **Readability first** - Clean syntax that's easy to understand
3. **Performance without sacrifice** - Efficient execution without complexity

## Syntax Guide

### Basic Structure
```clar
// Hello World in Clarity
fn main() {
    println("Hello, World!")
}
```

### Variables and Constants
```clar
// Immutable variable (like Rust's `let`)
let name = "Clarity";
let count: Int = 42;

// Mutable variable (like Rust's `mut`)
var counter = 0;
counter = counter + 1;

// Constants
const PI = 3.14159;
const MAX_SIZE: Int = 1000;
```

### Data Types
- `Int` - Signed integers
- `Float` - Floating point numbers
- `Bool` - Boolean values (`true`, `false`)
- `String` - Text strings
- `Array[T]` - Arrays of type T
- `Map[K,V]` - Maps from keys of type K to values of type V
- `Option[T]` - Optional values (Some(T) or None)
- `Result[T,E]` - Result values (Ok(T) or Err(E))

### Functions
```clar
// Function with parameters and return type
fn add(a: Int, b: Int) -> Int {
    return a + b;
}

// Function without return value (returns unit type)
fn greet(name: String) {
    println("Hello, ", name, "!");
}

// Recursive function
fn factorial(n: Int) -> Int {
    if n <= 1 {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
```

### Control Flow

#### Conditionals
```clar
if condition {
    // do something
} else if other_condition {
    // do something else
} else {
    // otherwise
}

// Expression form (returns a value)
let result = if x > 0 { x } else { -x };
```

#### Loops
```clar
// While loop
while condition {
    // do something
}

// For loop (iterates over collections)
for item in collection {
    // do something with item
}
```

#### Match Expressions
```clar
match value {
    pattern1 => result1,
    pattern2 => result2,
    _ => default_result  // wildcard pattern
}
```

### Operators

#### Arithmetic
- `+` - Addition
- `-` - Subtraction
- `*` - Multiplication
- `/` - Division
- `%` - Modulo

#### Comparison
- `==` - Equal to
- `!=` - Not equal to
- `<` - Less than
- `>` - Greater than
- `<=` - Less than or equal to
- `>=` - Greater than or equal to

#### Logical
- `&&` - Logical AND
- `||` - Logical OR
- `!` - Logical NOT

## Memory Management
Clarity uses a simplified ownership system inspired by Rust but easier to learn:
- Each value has a single owner
- When the owner goes out of scope, the value is dropped
- References must not outlive the value they refer to
- No garbage collection required

## Standard Library
The Clarity standard library includes:
- Basic I/O functions (`println`, `print`, `read_line`)
- Collection types (`Array`, `Map`, `Set`)
- Utility functions for mathematics, string manipulation, etc.
- Error handling utilities

## Error Handling
Clarity uses Result and Option types for error handling:
```clar
// Function that might fail
fn divide(a: Int, b: Int) -> Result[Int, String] {
    if b == 0 {
        return Err("Division by zero");
    } else {
        return Ok(a / b);
    }
}

// Using the result
match divide(10, 2) {
    Ok(value) => println("Result: ", value),
    Err(error) => println("Error: ", error)
}
```

## Concurrency
Clarity supports lightweight concurrency with async/await:
```clar
async fn fetch_data(url: String) -> String {
    // asynchronous operation
}

fn main() {
    let task = async fetch_data("http://example.com");
    let result = await task;
}
```

## Advantages of Clarity
1. **Safety**: Prevents memory errors and common bugs at compile time
2. **Performance**: Compiles to efficient machine code
3. **Readability**: Clear, expressive syntax
4. **Approachability**: Designed to be easy to learn
5. **Modern**: Includes contemporary features like pattern matching and async/await