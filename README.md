# seeker

**seeker** is a real-time desktop memory sentinel for Linux that watches system RAM behavior, detects risky patterns, and surfaces actionable alerts through a lightweight floating UI.

At its core, seeker answers one practical question:

> **"Is memory pressure growing in a way that can hurt system responsiveness, and which application is responsible right now?"**

It does this by continuously sampling system memory and process-level usage, classifying the system state, and converting findings into clear event cards (spikes, warnings, new heavy processes, and kill actions).

---

## Essence of the project

seeker is not just a monitor. It is a **decision-oriented observer**:

- It tracks memory pressure over time (not just a single static number).
- It identifies offending processes and application groups.
- It reduces notification spam with event cooldowns.
- It supports direct intervention from the UI (`Kill`, `Ignore`).
- In danger conditions, it can auto-terminate high-impact non-safe processes.

In short, seeker combines **observation + interpretation + action**.

---

## How seeker works

### 1) Continuous sampling loop

Every second, seeker collects:

- Global memory stats (`total`, `available`, `used`, `percent`)
- Per-process RSS memory usage

### 2) State analysis

The engine assigns a state based on thresholds:

- `NORMAL`
- `WARNING` (high RAM percentage)
- `DANGER` (very low available RAM)

It also checks for rapid growth in used memory to detect `SPIKE` events.

### 3) Process intelligence

seeker derives multiple views from raw process data:

- Top individual processes by memory
- Grouped application footprint (same process names aggregated)
- Newly appeared heavy processes (large memory from new PIDs)

### 4) Event generation + cooldown

Events are emitted only when meaningful and rate-limited with a cooldown window to avoid repetitive noise.

### 5) UI delivery

Events are pushed to a PyQt6 floating widget, rendered as interactive cards with:

- Severity state (`SPIKE`, `WARNING`, `NEW`, `KILLED`)
- Event log history per card
- Process control actions

---

## Major behaviors and triggers

- **SPIKE**: a process or system memory jump is detected.
- **WARNING**: RAM usage is high, and top offender is highlighted.
- **NEW_HEAVY**: a newly started process immediately consumes large memory.
- **PRESSURE_CHANGE**: pressure level moves across ranges (`NORMAL`, `ELEVATED`, `HIGH`, `CRITICAL`).
- **AUTO_KILL**: under danger conditions, seeker can terminate heavy non-safe processes.

Safe process names are protected by default in the core logic.

---

## Project structure

- `main.py`  
  Starts the app, runs core monitoring in a background thread, and launches the PyQt6 UI in the main thread.

- `core.py`  
  Implements data collection, analysis rules, process grouping, event detection, pressure tracking, and optional auto-kill logic.

- `ui.py`  
  Defines the floating event-card interface and action handling (`Kill`, `Ignore`, lifecycle cleanup, event rendering).

---

## Requirements

- Python 3.10+
- Linux environment
- Packages:
  - `psutil`
  - `PyQt6`

---

## Setup

1. Create virtual environment:

   ```bash
   python3 -m venv .venv
   ```

2. Activate it:

   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install psutil PyQt6
   ```

4. Run seeker:

   ```bash
   python main.py
   ```

---

## Using the UI

- **Single click + drag header**: move card/window
- **Double click card header**: expand/collapse event details
- **Ignore**: temporarily suppress alerts for that process key
- **Kill**: terminate matching process instances

Cards automatically update, merge repeated events, and self-clean when processes end.

---

## Design philosophy

seeker is built around three principles:

1. **Fast feedback** – near real-time updates (1s loop)
2. **Low friction** – always-on-top, compact, frameless UI
3. **Actionability** – every critical alert can lead to an immediate response

---

## Limitations and caution

- Thresholds are heuristic and may need tuning per machine/workload.
- Process termination is a destructive action—use with care.
- Name-based grouping is practical but not perfect for all process models.
- Some processes may be inaccessible depending on permissions.

---

## Summary

**seeker** is a focused memory-watch tool that closes the gap between "something is wrong" and "here is exactly what to do now." It monitors, interprets, and enables intervention in one compact desktop workflow.
