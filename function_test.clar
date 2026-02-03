// Test using functions to avoid top-level statement issues
fn calculate() -> Int {
    let x = 42;
    var y = 15;
    let result = (x + y) * 2;
    println("Result: ", result);
    
    if result > 100 {
        println("Greater than 100");
    } else {
        println("Not greater than 100");
    }
    
    var counter = 0;
    while counter < 3 {
        println("Count: ", counter);
        counter = counter + 1;
    }
    
    return result;
}

let final_result = calculate();
println("Final result: ", final_result);