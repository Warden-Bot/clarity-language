// Comprehensive test of Clarity language features

// Test variable declarations
let immutable_val = 42;
var mutable_val = 10;
mutable_val = mutable_val + 5;  // Now mutable_val = 15

// Test arithmetic
let result = (immutable_val + mutable_val) * 2;
println("Calculated result: ", result);

// Test conditional
if result > 100 {
    println("Result is greater than 100");
} else {
    println("Result is not greater than 100");
}

// Test boolean operations
let bool_test = (result > 50) && (immutable_val < 100);
println("Boolean test result: ", bool_test);

// Test function definition and call
fn square(x: Int) -> Int {
    return x * x;
}

let squared = square(5);
println("5 squared is: ", squared);

// Test more complex conditional
let abs_val = if result < 0 { -result } else { result };
println("Absolute value of result: ", abs_val);

// Test while loop
var counter = 0;
while counter < 5 {
    println("Counter: ", counter);
    counter = counter + 1;
}

// Test string operations (conceptual - actual implementation depends on string handling)
println("Comprehensive test completed successfully!");