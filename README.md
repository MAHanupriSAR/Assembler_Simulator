# RISC-V Assembler & Simulator

> A full two-pass **assembler** and **execution simulator** for a subset of the **RV32I** (RISC-V 32-bit Integer) instruction set, built in pure Python.

[![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![ISA](https://img.shields.io/badge/ISA-RV32I-green)](https://riscv.org/technical/specifications/)

---

## 📖 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Supported Instructions](#supported-instructions)
- [Register Reference](#register-reference)
- [Installation](#installation)
- [Usage](#usage)
  - [Assembler](#assembler)
  - [Simulator](#simulator)
- [Assembly Language Syntax](#assembly-language-syntax)
  - [Labels](#labels)
  - [Virtual Halt](#virtual-halt)
  - [Example Programs](#example-programs)
- [I/O File Formats](#io-file-formats)
  - [Assembler Input](#assembler-input--assembly-code)
  - [Assembler Output](#assembler-output--machine-code)
  - [Simulator Output](#simulator-output--execution-trace)
- [Error Handling](#error-handling)
- [Testing & Grading](#testing--grading)
  - [Directory Setup](#directory-setup-for-grader)
  - [Running the Grader](#running-the-grader)
- [Project Structure](#project-structure)
- [Team Members](#team-members)
- [License](#license)

---

## Overview

This project was developed as part of a **Computer Organization** (CO) course assignment. It implements the two core tools of a typical RISC-V toolchain:

| Tool | Script | Purpose |
|------|--------|---------|
| **Assembler** | `Assembler.py` | Translates RV32I assembly text into 32-bit binary machine code |
| **Simulator** | `Simulator.py` | Executes binary machine code, producing a step-by-step register & memory trace |

The pipeline is:

```
Assembly Source (.txt)  ──►  Assembler.py  ──►  Machine Code (.txt)  ──►  Simulator.py  ──►  Execution Trace (.txt)
```

---

## Architecture

### Assembler — Two-Pass Design

| Pass | What it does |
|------|-------------|
| **Pass 1** | Scans for label definitions, records each label's line number and computes its byte address (`line × 4`). |
| **Pass 2** | Resolves all label references to their PC-relative offsets, then encodes each instruction into a 32-bit binary string. |

Key encoding functions:

| Function | Purpose |
|----------|---------|
| `imm_binary_calc(imm, max_bits)` | Converts a signed integer into a two's-complement binary string of `max_bits` width |
| `reg_binary_calc(name)` | Returns the 5-bit register encoding for an ABI name (`a0`) or canonical name (`x10`) |
| `binary_representation(num, bits)` | Unsigned binary string of `bits` width |
| `binary_rep_compliment(num, bits)` | Two's-complement binary string for negative values |
| `convertible(num, bits)` | Checks if a value fits in a signed `bits`-wide field |

### Simulator — Fetch-Decode-Execute Loop

The simulator reads each 32-bit binary instruction, decodes it by slicing bit fields, dispatches to a type-specific handler, and records state after every instruction.

| Component | Details |
|-----------|---------|
| **Program Counter (PC)** | Starts at `0`; incremented by 4 per sequential instruction |
| **Registers** | `x0`–`x31` (32 × 32-bit); `x0` is hard-wired to `0`; `x2 (sp)` initialised to `256` |
| **Memory** | 32 word-aligned locations: `0x00010000` – `0x0001007c` (128 bytes total) |
| **Halt condition** | `beq zero,zero,0` — the "virtual halt" instruction |

---

## Supported Instructions

### R-Type — Register–Register Operations

| Mnemonic | Operation | funct7 | funct3 |
|----------|-----------|--------|--------|
| `add`    | rd = rs1 + rs2 | `0000000` | `000` |
| `sub`    | rd = rs1 − rs2 | `0100000` | `000` |
| `sll`    | rd = rs1 << rs2[4:0] | `0000000` | `001` |
| `slt`    | rd = (rs1 < rs2) ? 1 : 0 (signed) | `0000000` | `010` |
| `sltu`   | rd = (rs1 < rs2) ? 1 : 0 (unsigned) | `0000000` | `011` |
| `xor`    | rd = rs1 ^ rs2 | `0000000` | `100` |
| `srl`    | rd = rs1 >> rs2[4:0] (logical) | `0000000` | `101` |
| `or`     | rd = rs1 \| rs2 | `0000000` | `110` |
| `and`    | rd = rs1 & rs2 | `0000000` | `111` |

**Encoding:**  `funct7 | rs2 | rs1 | funct3 | rd | 0110011`

---

### I-Type — Immediate & Load Operations

| Mnemonic | Operation | Opcode | funct3 |
|----------|-----------|--------|--------|
| `addi`   | rd = rs1 + imm | `0010011` | `000` |
| `sltiu`  | rd = (rs1 < imm) ? 1 : 0 (unsigned) | `0010011` | `011` |
| `lw`     | rd = Mem[rs1 + imm] | `0000011` | `010` |
| `jalr`   | rd = PC+4; PC = (rs1+imm) & ~1 | `1100111` | `000` |

**Encoding:**  `imm[11:0] | rs1 | funct3 | rd | opcode`

Immediate range: **−2048 to +2047** (12-bit signed)

---

### S-Type — Store Operations

| Mnemonic | Operation | Opcode | funct3 |
|----------|-----------|--------|--------|
| `sw`     | Mem[rs1 + imm] = rs2 | `0100011` | `010` |

**Encoding:**  `imm[11:5] | rs2 | rs1 | funct3 | imm[4:0] | 0100011`

---

### B-Type — Conditional Branch Operations

| Mnemonic | Condition | funct3 |
|----------|-----------|--------|
| `beq`    | rs1 == rs2 | `000` |
| `bne`    | rs1 != rs2 | `001` |
| `blt`    | rs1 < rs2 (signed) | `100` |
| `bge`    | rs1 >= rs2 (signed) | `101` |
| `bltu`   | rs1 < rs2 (unsigned) | `110` |
| `bgeu`   | rs1 >= rs2 (unsigned) | `111` |

**Encoding:**  `imm[12|10:5] | rs2 | rs1 | funct3 | imm[4:1|11] | 1100011`

Branch offset range: **−4096 to +4094** (multiples of 2, encoded in 13 bits)

---

### U-Type — Upper Immediate Operations

| Mnemonic | Operation | Opcode |
|----------|-----------|--------|
| `lui`    | rd = imm << 12 | `0110111` |
| `auipc`  | rd = PC + (imm << 12) | `0010111` |

**Encoding:**  `imm[31:12] | rd | opcode`

---

### J-Type — Unconditional Jump

| Mnemonic | Operation | Opcode |
|----------|-----------|--------|
| `jal`    | rd = PC+4; PC = PC + offset | `1101111` |

**Encoding:**  `imm[20|10:1|11|19:12] | rd | 1101111`

Jump offset range: **−1048576 to +1048574** (multiples of 2, encoded in 21 bits)

---

## Register Reference

The assembler and simulator accept both ABI names and `xN` canonical names.

| ABI Name | Register | 5-bit Encoding | Initial Value | Convention |
|----------|----------|----------------|---------------|------------|
| `zero`   | `x0`  | `00000` | 0 | Hard-wired zero |
| `ra`     | `x1`  | `00001` | 0 | Return address |
| `sp`     | `x2`  | `00010` | **256** | Stack pointer |
| `gp`     | `x3`  | `00011` | 0 | Global pointer |
| `tp`     | `x4`  | `00100` | 0 | Thread pointer |
| `t0`–`t2` | `x5`–`x7` | `00101`–`00111` | 0 | Temporaries |
| `s0`/`fp`, `s1` | `x8`–`x9` | `01000`–`01001` | 0 | Saved / Frame ptr |
| `a0`–`a7` | `x10`–`x17` | `01010`–`10001` | 0 | Function args / return values |
| `s2`–`s11` | `x18`–`x27` | `10010`–`11011` | 0 | Saved registers |
| `t3`–`t6` | `x28`–`x31` | `11100`–`11111` | 0 | Temporaries |

---

## Installation

**Requirements:** Python 3.x — no third-party packages needed.

```bash
# Clone the repository
git clone https://github.com/MAHanupriSAR/Assembler_Simulator.git
cd Assembler_Simulator
```

---

## Usage

### Assembler

```bash
python Assembler.py <input_assembly_file> <output_machine_code_file>
```

**Example:**
```bash
python Assembler.py test_cases/assembly_program/sa1 test_cases/machine_code/sa1_out.txt
```

The assembler will:
1. Resolve all label definitions and references.
2. Encode every instruction into a 32-bit binary string.
3. Validate syntax, register names, and immediate ranges.
4. Write one binary instruction per line to the output file.
5. On error: print `Error generated at line <N>` and produce an **empty** output file.

---

### Simulator

```bash
python Simulator.py <input_machine_code_file> <output_trace_file>
```

**Example:**
```bash
python Simulator.py test_cases/machine_code/sa1_out.txt test_cases/simulator_trace/sa1_trace.txt
```

The simulator will:
1. Load all 32-bit instructions from the machine code file.
2. Execute instructions one at a time, updating the PC, registers, and memory.
3. Append a state snapshot after each instruction to the output file.
4. Halt when it encounters the virtual halt instruction (`beq zero,zero,0`).

---

## Assembly Language Syntax

### General Rules

- **One instruction per line** — blank lines are ignored.
- **Whitespace:** a single space separates the mnemonic from its operands; operands are comma-separated (no spaces between operands except before the first one).
- **Comments:** not supported — keep the source clean.
- **Labels:** must consist only of alphanumeric characters and underscores (`[a-zA-Z0-9_]+`).
- **Case-sensitive:** `beq` is not the same as `BEQ`.

### Labels

Labels are written on a dedicated line followed by a colon. They are replaced by their PC-relative offsets automatically during assembly.

```asm
loop:
    addi t0,t0,1
    blt  t0,a0,loop
```

> **Note:** The assembler resolves label addresses as `(target_line - current_line) × 4`.

### Virtual Halt

Every valid program **must** end with a virtual halt instruction as its **last** instruction:

```asm
beq zero,zero,0
```

The assembler enforces this rule — if the halt is absent or not the final instruction, an error is raised and the output file is cleared.

### Example Programs

#### Arithmetic & Logic (sa1)

```asm
addi a0,zero,-5
addi a1,zero,3
sltiu t0,a0,-1
sltiu t1,a1,2
sll   t2,a0,a1
sub   a0,a0,a1
slt   t3,zero,a0
sll   a0,a0,a3
sltu  t4,a0,t1
xor   a5,a0,t0
srl   t5,a5,t0
or    s0,a0,t0
and   s0,a0,t1
beq   zero,zero,0
```

#### LUI + Mixed Operations (sa5 excerpt)

```asm
lui   s0,10
addi  ra,zero,-10
addi  sp,zero,20
add   s7,s2,s3
sub   s4,s5,s2
xor   s1,s4,s10
or    a4,a3,a1
and   a7,a3,a1
slt   t3,t4,t5
beq   zero,zero,0
```

---

## I/O File Formats

### Assembler Input — Assembly Code

Plain text file (`.txt`). One instruction or label per line.

```
addi a0,zero,-5
addi a1,zero,3
beq  zero,zero,0
```

### Assembler Output — Machine Code

Plain text file. One 32-bit binary string per line (no `0b` prefix, no spaces).

```
11111111011100000000010100010011
00000000001100000000010110010011
00000000000000000000000001100011
```

### Simulator Output — Execution Trace

Each line corresponds to the state **after** one instruction executes.

**Format per line (instruction state):**
```
<PC> <x0> <x1> <x2> ... <x31>
```

- **PC** — next program counter value with `0b` prefix (32 bits), e.g. `0b00000000000000000000000000001000`
- **Registers** — 32 values (`x0`–`x31`) each as a `0b`-prefixed 32-bit signed binary number

**Memory section** (appended once at the end):
```
<address>:<0b32-bit-value>
```
32 word addresses from `0x00010000` to `0x0001007c`.

**Example trace excerpt:**
```
0b00000000000000000000000000000100 0b00000000000000000000000000000000 0b00000000000000000000000000000000 0b00000000000000000001000000000000 ...
0x00010000:0b00000000000000000000000000000000
0x00010004:0b00000000000000000000000000000000
...
```

---

## Error Handling

The assembler performs thorough validation and emits a human-readable error message before clearing the output file.

| Error Condition | Message |
|----------------|---------|
| Invalid instruction mnemonic | `Error generated at line <N>` |
| Wrong number of operands | `Error generated at line <N>` |
| Unknown register name | `Error generated at line <N>` |
| Immediate out of range | `Error generated at line <N>` |
| Malformed label (non-alphanumeric chars) | `Error generated at line <N>` |
| Virtual halt (`beq zero,zero,0`) absent | `Virtual halt absent` |
| Virtual halt is not the last instruction | `Error generated as virtual halt is on line <M> and last instruction is on line <N>` |

On any error the output file is **truncated to zero bytes** so downstream tools cannot silently consume corrupt binary.

---

## Testing & Grading

The `evaluate/` directory contains an automated grading framework for both the assembler and simulator.

### Test Suite Overview

| Component | Simple Tests | Hard Tests |
|-----------|-------------|------------|
| Assembler | 10 (×0.1 each) | 5 (×0.2 each) |
| Simulator | 5 (×0.4 each) | 5 (×0.8 each) |

### Directory Setup for Grader

Place your scripts as follows:

```
evaluate/
├── SimpleAssembler/
│   └── Assembler.py          ← your assembler (must be named exactly this)
├── SimpleSimulator/
│   └── Simulator.py          ← your simulator (must be named exactly this)
└── automatedTesting/
    ├── src/
    │   ├── main.py           ← entry point for all tests
    │   ├── AsmGrader.py
    │   ├── SimGrader.py
    │   ├── Results.py
    │   ├── Grader.py
    │   └── Colors.py
    └── tests/
        ├── assembly/
        │   ├── simpleBin/    ← simple assembler test inputs
        │   ├── hardBin/      ← hard assembler test inputs
        │   ├── errorGen/     ← intentionally invalid inputs (error tests)
        │   ├── bin_s/        ← expected machine code for simpleBin
        │   ├── bin_h/        ← expected machine code for hardBin
        │   ├── user_bin_s/   ← your assembler's output for simpleBin
        │   └── user_bin_h/   ← your assembler's output for hardBin
        ├── bin/
        │   ├── simple/       ← machine code inputs for simulator
        │   └── hard/
        ├── traces/
        │   ├── simple/       ← expected simulator traces
        │   └── hard/
        └── user_traces/
            ├── simple/       ← your simulator's generated traces
            └── hard/
```

### Running the Grader

Run all grader commands from inside `evaluate/automatedTesting/`.

#### Test Assembler Only

```bash
# Linux
python3 src/main.py --no-sim --linux

# Windows
python3 src\main.py --no-sim --windows
```

#### Test Simulator Only

```bash
# Linux
python3 src/main.py --no-asm --linux

# Windows
python3 src\main.py --no-asm --windows
```

#### Test Both (Assembler + Simulator)

```bash
# Linux
python3 src/main.py --linux

# Windows
python3 src\main.py --windows
```

---

## Project Structure

```
Assembler_Simulator/
│
├── Assembler.py              # Two-pass RV32I assembler
├── Simulator.py              # Fetch-decode-execute simulator
│
├── test_cases/
│   ├── assembly_program/     # 8 sample assembly programs (sa1–sa8)
│   ├── machine_code/         # Corresponding expected machine code outputs
│   └── simulator_trace/      # Corresponding expected simulator traces
│
├── evaluate/
│   ├── SimpleAssembler/      # Drop-in location for Assembler.py
│   ├── SimpleSimulator/      # Drop-in location for Simulator.py
│   ├── automatedTesting/
│   │   ├── src/              # Grading scripts (main.py, AsmGrader.py, …)
│   │   └── tests/            # Test inputs and expected outputs
│   └── readme.txt            # Grader usage notes
│
├── description.pdf           # Original assignment specification
├── Members.txt               # Team roster
├── LICENSE                   # MIT License
└── README.md                 # This file
```

---

## Team Members

| Name | Roll Number |
|------|-------------|
| Ashutosh Tiwari | 2023154 |
| Antriksh Mahato | 2023107 |
| Anuraag Tandon  | 2023110 |
| Kunal Jain      | 2023293 |

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for full terms.