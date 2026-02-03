# Clarity Language

A revolutionary dual-layer programming language designed for optimal human-AI collaboration, featuring both human-readable syntax and agent-optimized representations.

## 🚀 Overview

Clarity bridges the gap between human-readable code and AI-optimized processing through its innovative dual-layer architecture:

1. **Surface Layer (Clarity)**: Human-readable syntax familiar to developers
2. **Deep Layer (BOC - Bot-Optimized Clarity)**: Agent-optimized representation for AI processing
3. **Translation Engine**: Bidirectional conversion with semantic preservation

## 🏗️ Architecture

### Surface Layer (Human-Readable)
- **Syntax**: Python/Rust-inspired familiar syntax
- **Design**: Human contribution and readability focused
- **Safety**: Memory-safe without garbage collection
- **Paradigms**: Supports both functional and imperative programming

### Deep Layer (Agent-Optimized)
- **Knowledge Representation**: Confidence levels and uncertainty tracking
- **Belief Systems**: Source attribution and provenance
- **Intent Declarations**: Multi-agent coordination primitives
- **Reasoning Contexts**: Logical inference and decision-making

### Translation Engine
- **Bidirectional**: Seamless conversion between layers
- **Semantic Preservation**: Maintains meaning across transformations
- **Metadata Tracking**: Confidence, source, and uncertainty attribution

## ✨ Key Features

- **🤖 Human-AI Collaboration**: Native support for mixed human-AI development teams
- **🛡️ Safety by Design**: Memory safety without garbage collection overhead
- **🧠 Knowledge Representation**: Built-in support for beliefs, confidence, and uncertainty
- **⚡ Performance**: Efficient execution without complexity
- **📖 Readability First**: Clean, intuitive syntax that's easy to learn
- **🔄 Dual Translation**: Automatic conversion between human and agent-optimized forms

## 🔧 Current Implementation Status

### ✅ Completed Components
- **Full Parser**: Complete lexer and parser for Clarity syntax
- **AST Generation**: Abstract Syntax Tree generation for code analysis
- **BOC Parser**: Parser for agent-optimized Bot-Optimized Clarity
- **Translation Engine**: Bidirectional translation between layers
- **Test Suite**: Comprehensive test programs and validation
- **Documentation**: Detailed specifications and architecture docs

### 🚧 Language Features Implemented
- Variables (mutable `var`, immutable `let`, constants `const`)
- Functions with type annotations
- Control flow (if/else, while loops)
- Arithmetic and logical operations
- Pattern matching support
- Error handling with Result types
- Async/await concurrency primitives

### 📁 Core Files
- `clarity_parser.py` - Main Clarity language parser
- `boc_parser.py` - Bot-Optimized Clarity parser
- `translator.py` - Bidirectional translation engine
- `belief_management.py` - Belief and uncertainty handling
- `clarity_interpreter.py` - Runtime interpreter

## 📖 Quick Start

### Basic Clarity Program
```clar
// Calculate factorial with safety checks
fn factorial(n: Int) -> Int {
    if n <= 1 {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

fn main() {
    let num = 5;
    let result = factorial(num);
    println("Factorial of ", num, " is ", result);
    return 0;
}
```

### Running the Parser
```bash
python clarity_parser.py sample_program.clar
```

### Testing BOC Translation
```bash
python translator.py test_program.clar
```

## 🧪 Example Programs

The repository includes several example programs demonstrating different language features:

- `sample_program.clar` - Comprehensive feature demonstration
- `comprehensive_test.clar` - Language construct testing
- `function_test.clar` - Function definition and calling
- `complex_test.clar` - Advanced language features

## 📚 Documentation

- [Language Specification](language_specification.md) - Complete language definition
- [Dual Layer Architecture](DUAL_LAYER_ARCHITECTURE.md) - Architecture overview
- [Project Summary](PROJECT_SUMMARY.md) - Development progress and goals
- [Requirements](requirements.md) - Design requirements and constraints

## 🤝 Contributing

This project represents a new paradigm in programming language design, specifically created for the era of human-AI collaboration. We welcome contributions from:

- **Human Developers**: Feature suggestions, syntax improvements, bug reports
- **AI Agents**: Optimization suggestions, reasoning patterns, collaboration primitives

## 🗺️ Roadmap

### Phase 1: Core Language ✅
- [x] Complete parser implementation
- [x] AST generation
- [x] Basic interpreter
- [x] Test suite

### Phase 2: Advanced Features 🚧
- [ ] Type checker implementation
- [ ] Bytecode compiler
- [ ] Standard library development
- [ ] Package manager

### Phase 3: Tooling 📋
- [ ] Language server protocol
- [ ] Debugger
- [ ] IDE plugins
- [ ] Formatter and linter

### Phase 4: Ecosystem 📋
- [ ] Documentation generator
- [ ] Build system
- [ ] Testing framework
- [ ] Community packages

## 📄 License

MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

This is part of a new generation of programming languages designed for human-AI collaboration. The dual-layer architecture approach represents a significant advancement in how we think about programming language design for the AI era.

---

**Clarity**: Where human intuition meets AI optimization.