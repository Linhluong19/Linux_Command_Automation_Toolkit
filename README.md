# Linux Command Toolkit (LCAT)

A Python-based interactive Linux command automation utility. 

------------------------------------------------------------------------

## Table of Contents

- [Introduction](#introduction)
- [Project Overview](#project-overview)
- [Objectives](#objectives)
- [Installation](#installation)
- [Code Structure](#code-structure)
- [How It Works](#how-it-works)
- [Features](#features)
- [Usage](#usage)
    - [Interactive Mode](#interactive-mode)
    - [Programmatic Usage](#programmatic-usage)
- [Example Commands](#example-commands)
- [Command History Format](#command-history-format)
- [Limitations](#limitations)

------------------------------------------------------------------------

## Introduction

Linux Command Toolkit (LCAT) is a Python-based utility that provides an interactive interface to execute and manage Linux commands programmatically. It simplifies running, monitoring, and automating common Linux operations-- such as file manipulation, process inspection, system monitoring, and directory navigation-- while collecting a
structured execution history.

This toolkit is especially useful for: 
- developers working across multiple environments
- students learning Linux system commands
- automation engineers and sysadmins
- anyone needing Python wrappers for Linux commands

------------------------------------------------------------------------

## Project Overview

LCAT encapsulates common Linux shell operations inside a single Python class called LinuxCommandToolkit.

It exposes methods corresponding to Linux utilities such as:
`ls`, `rm`, `mkdir`, `touch`, `cd`, `pwd`, `chmod`, `chown`, `ps`, `kill`, `top`, `free`,`grep`, `find`

Each method internally uses Python's `subprocess` (except for `cd`), standardizes the output, and stores full execution metadata in a history log.

You can use LCAT in interactive REPL mode, or as an imported Python module.


------------------------------------------------------------------------

## Objectives

-   Provide a Python interface to execute common Linux commands
-   Maintain a history of executed commands with stdout, stderr, exit codes, and timestamps
-   Support advanced functionality (recursive deletes, permission changes, process      control, searching)
-   Provide a clean interactive mode for real-time command execution
-   Offer a reusable automation library for system management tasks

------------------------------------------------------------------------


## Installation


### 1. Clone the repository

``` bash
git clone https://github.com/Linhluong19/Linux_Command_Automation_Toolkit.git
cd Linux_Command_Automation_Toolkit
```


### 2. Ensure Python 3.8+ is installed

``` bash
python3 --version
```


### 3. Dependencies

LCAT uses only Python's standard library, including: 
- `subprocess`
- `os`
- `datetime`
- `typing`
- `json`
- `re`
- `sys`

No external packages are required.

### Optional: Create a virtual environment

``` bash
python3 -m venv venv
source venv/bin/activate        # Linux/macOS
# OR
venv\Scripts\activate         # Windows
```

------------------------------------------------------------------------

## Code Structure

    LCAT.py                 # Main Python script containing LinuxCommandToolkit class
    README.md               # Documentation (this file)

------------------------------------------------------------------------

## How It Works

### 1. Central Execution Engine: `_execute_command()`

All Linux commands eventually route through this method.

It handles: 
- building the command\
- executing via subprocess\
- capturing stdout/stderr\
- returning structured results\
- logging history

### 2. Wrapper Methods for Linux Commands

Examples:

#### User / System Info

-   `who_am_i()`\
-   `pwd()`\
-   `free()`\
-   `top()`

#### File & Directory Operations

-   `ls()`, `mkdir()`, `touch()`, `rm()`, `cd()`\
-   `chmod()`, `chown()`

#### Search / Filter

-   `grep()`, `find()`

#### Process Handling

-   `ps()`, `kill()`

Each returns a normalized dictionary.

### 3. Interactive Shell (REPL)

Running:

``` bash
python3 LCAT.py
```

Shows:

```
    Welcome to the Linux Command Toolkit Interactive Mode!
    Type 'exit' to quit.
    lct>
```

The REPL: 
- accepts method names\
- parses arguments\
- executes methods\
- prints formatted results

------------------------------------------------------------------------

## Features

-   Cross-command history tracking\
-   Clean stdout/stderr separation\
-   Graceful error handling\
-   Optional output summaries\
-   REPL mode\
-   Automation-friendly class design\
-   Consistent platform behavior

------------------------------------------------------------------------

## Usage

### 1. Interactive Mode

``` bash
python3 LCAT.py
```

Example session:

```
lct> who_am_i
lct> pwd
lct> ls -l /home/user
lct> mkdir test_folder
lct> rm -r old_logs
```

Exit:

`lct> exit`

------------------------------------------------------------------------

### 2. Programmatic Usage

``` python
from LCAT import LinuxCommandToolkit

lct = LinuxCommandToolkit()

result = lct.ls(long_format=True, path=".")
print(result["stdout"])
```

More examples:

``` python
lct.mkdir("project", parents=True, verbose=True)
lct.chmod("project", mode="755")
lct.touch("project/app.py")
```

------------------------------------------------------------------------

## Example Commands

  Action            Command
  ----------------- --------------------------------------
  List all files    `lct> ls -a`
  Long listing      `lct> ls -l`
  Create folder     `lct> mkdir test`
  Delete file       `lct> rm test.txt`
  Kill a process    `lct> kill 1337`
  Search for text   `lct> grep -i error /var/log/syslog`
  Find files        `lct> find . -name '*.py'`

------------------------------------------------------------------------

## Command History Format

Example entry:

``` json
{
  "command": "ls -l",
  "returncode": 0,
  "stdout": "file1.txt\nfile2.txt",
  "stderr": "",
  "success": true,
  "timestamp": "2025-11-24 10:32:45"
}
```

Stored under:

`self.history`

------------------------------------------------------------------------

## Limitations

-   Designed for Linux systems only\
-   Commands run inside Python, not the user's shell\
-   Pipes (`|`) and redirection (`>`) not supported\
-   REPL does not support complex quoting

