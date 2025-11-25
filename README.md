# Linux_Command_Automation_Toolkit

A Python-based wrapper around common Linux commands such as `ls`, `grep`, `find`, `ps`, and `kill`.

This toolkit provides:
- Human-readable summaries
- Optional visualized outputs
- A simple interactive CLI
- Safer, structured interfaces for common system operations



Each wrapper returns a structured dictionary:

```
{
  "command": "ls -l",
  "success": true,
  "stdout": "...",
  "stderr": ""
}
```


### Example Usage:

```
lct> ls -l
lct> grep error logs/
lct> ps
lct> kill 1010
lct> find . -name "*.txt"
```

# Algorithm Explanations

### 1. Command Execution Layer

The core of the toolkit is `_execute_command()`, which internally uses subprocess
`.run(...)`

This allows:

- Capturing output (stdout, stderr)
- Returning exit codes
- Enforcing a timeout
- Logging command history


### 2. High-Level Abstraction

Each Linux command is converted into a Python-friendly function.

Instead of typing:
`ps aux | grep python`,
You can write:
`lct.ps(filter="python")`.

### 3. Enhanced Features

- All results are stored in self.history.
- Automatic formatting of outputs.
- Visual summaries via `visualization_result(result)`.

### 4. Interactive Mode

This mini-shell allows:

- Typing method names directly
- Parsing arguments safely
- Preventing dangerous command chaining (&&, ;, pipes)

It works like a safer version of bash for beginners.






