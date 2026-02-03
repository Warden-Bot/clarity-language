// Sample Clarity program demonstrating various language features

// Function to calculate factorial
fn factorial(n: Int) -> Int {
    if n <= 1 {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

// Function to check if a number is prime
fn is_prime(n: Int) -> Bool {
    if n <= 1 {
        return false;
    }
    if n == 2 {
        return true;
    }
    if n % 2 == 0 {
        return false;
    }
    
    let limit = sqrt(n);  // Assume sqrt is a built-in function
    let i = 3;
    while i <= limit {
        if n % i == 0 {
            return false;
        }
        i = i + 2;
    }
    return true;
}

// Function to calculate Fibonacci numbers
fn fibonacci(n: Int) -> Int {
    if n <= 1 {
        return n;
    }
    return fibonacci(n - 1) + fibonacci(n - 2);
}

// Main function demonstrating the language features
fn main() {
    // Variable declarations
    let num = 5;
    var result = factorial(num);
    const MAX_ITERATIONS = 10;
    
    // Print the result
    println("Factorial of ", num, " is ", result);
    
    // Test primality
    if is_prime(result) {
        println(result, " is a prime number");
    } else {
        println(result, " is not a prime number");
    }
    
    // Loop demonstration
    let fib_index = 0;
    while fib_index < MAX_ITERATIONS {
        let fib_num = fibonacci(fib_index);
        println("Fibonacci(", fib_index, ") = ", fib_num);
        fib_index = fib_index + 1;
    }
    
    // Conditional expression
    let larger = if result > 100 { result } else { 100 };
    println("The larger value is ", larger);
    
    return 0;
}