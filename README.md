# Linux Command Toolkit (LCAT)

A Python-based interactive Linux command automation utility

### 📑 Table of Contents

Introduction

Project Overview

Objectives

Installation

Code Structure

How It Works

Features

Usage

Interactive Mode

Programmatic Usage

Example Commands

Command History Format

Limitations

Future Enhancements

Introduction

Linux Command Toolkit (LCAT) is a Python-based utility that provides an interactive interface to execute and manage Linux commands programmatically. It simplifies running, monitoring, and automating common Linux operations — such as file manipulation, process inspection, system monitoring, and directory navigation — while collecting a structured execution history.

This toolkit is especially useful for:

developers working across multiple environments

students learning Linux system commands

automation engineers and sysadmins

anyone needing Python wrappers for Linux commands

Project Overview

LCAT encapsulates common Linux shell operations inside a single Python class called LinuxCommandToolkit.
It exposes methods corresponding to Linux utilities such as:

ls, rm, mkdir, touch

cd, pwd, chmod, chown

ps, kill, top, free

grep, find

Each method internally uses Python’s subprocess (except for cd), standardizes the output, and stores full execution metadata in a history log.

You can use LCAT in:

interactive REPL mode, or

import it as a Python module in your own projects

Objectives

Provide a Python interface to execute common Linux commands

Maintain a history of executed commands with stdout, stderr, exit codes, and timestamps

Support advanced functionality (recursive deletes, permission changes, process control, searching, filtering)

Provide a clean interactive mode for real-time command execution

Offer a reusable automation library for system management tasks

Installation
1. Clone the repository
git clone <repository_url>
cd <repository_directory>

2. Ensure Python 3.8+ is installed
python3 --version

3. Dependencies

LCAT only uses Python’s standard library, including:

subprocess

os

datetime

typing

json

re

sys

No external packages are required.

Optional: Set up a virtual environment
python3 -m venv venv
source venv/bin/activate          # Linux/macOS
# OR
venv\Scripts\activate             # Windows

pip install -r requirements.txt   # Only if provided

Code Structure
LCAT.py                 # Main Python script containing LinuxCommandToolkit class
README.md               # Documentation (this file)

How It Works

The toolkit revolves around a single class:

LinuxCommandToolkit
1. Central Execution Engine: _execute_command

All Linux commands eventually call this method.

It handles:

command construction

running commands using subprocess.run()

capturing stdout/stderr

detecting errors

saving command history

returning structured dictionaries

2. Methods That Wrap Linux Commands

Each Linux utility is represented as a method:

User / System Info

who_am_i()

pwd()

free()

top()

File & Directory Ops

ls(), mkdir(), touch(), rm(), cd()

chmod(), chown()

Search / Filtering

grep(), find()

Process Handling

ps(), kill()

The output format is normalized into Python dictionaries and optionally fed to a visualization helper.

3. Interactive Shell (REPL)

When run as:

python3 LCAT.py


LCAT starts an interactive CLI:

Welcome to the Linux Command Toolkit Interactive Mode!
Type 'exit' to quit.
lct>


The REPL:

accepts LinuxCommandToolkit method names

parses arguments

executes the appropriate method

prints structured formatted results

Features

Cross-method command history

Clean stdout/stderr segmentation

Graceful error handling

Timeout protection

Optional summaries for some commands

Interactive mode

Reusable for automation scripts

Behaves consistently across environments

Usage

### 1. Interactive Mode

Run the script directly:

`python3 LCAT.py`


Example session:

```
lct> who_am_i
lct> pwd
lct> ls -l /home/user
lct> mkdir test_folder
lct> rm -r old_logs
```


Exit via:

`lct> exit`

### 2. Programmatic Usage

Import and integrate into your own scripts:

```
from LCAT import LinuxCommandToolkit

lct = LinuxCommandToolkit()

result = lct.ls(long_format=True, path=".")
print(result["stdout"])
```

Or:

```
lct.mkdir("project", parents=True, verbose=True)
lct.chmod("project", mode="755")
lct.touch("project/app.py")
```

Example Commands

| Action          | Command                              |
| --------------- | ------------------------------------ |
| List all files  | `lct> ls -a`                         |
| Long listing    | `lct> ls -l`                         |
| Create folder   | `lct> mkdir test`                    |
| Delete file     | `lct> rm test.txt`                   |
| Kill a process  | `lct> kill 1337`                     |
| Search for text | `lct> grep -i error /var/log/syslog` |
| Find files      | `lct> find . -name '*.py'`           |



### Command History Format

Every command results in a dictionary like:

```
{
  "command": "ls -l",
  "returncode": 0,
  "stdout": "file1.txt\nfile2.txt",
  "stderr": "",
  "success": true,
  "timestamp": "2025-11-24 10:32:45"
}
```


Entries are stored in:

`self.history`

### Limitations

- Designed for Linux systems only
- Commands run inside Python’s environment, not your shell
- Does not support shell operators like pipes (|) or redirection (>)
- REPL does not handle complex quoting