DND Character Sheet

# DND Sheet Design Document (Final)

## Project Goals

This project is meant to replace shitty DND character apps that cause problems for me. This is
for my sole personal use FOR NOW, and will not be turning it in for a grade or anything. I want it
to eventually look good because I will be using it, but that is not a priority. I am a UNLV
sophomore in experience, but I will NOT be submitting this for anything.

## Project Summary

This project is a manual-entry, zone-based character sheet / workspace system built around
**two completely separate subsystems**: **Counters** and **Text**.

In both subsystems, **files on disk are the launch-time source of truth**. The UI is a direct projection of
those files. The system intentionally avoids automation, rule enforcement, and hidden logic. Its
goals are flexibility, predictability, and safety through explicit user control and reliance on
external editors.

All files are read on application launch and snapshotted into memory.
The application **does not perform any filesystem reads after launch**.
The only file ever written to by the application is `Counters.csv`.

---

## 1) Counters Subsystem

### Purpose

A persistent, independently scrolling area for frequently used numeric trackers (HP, resources,
charges, etc.). This area is called the **Counter Zone (CZ)**.

---

### Counter Zone (CZ) UI

* Displays a vertical list of counters.
* Each counter shows:

  * Name
  * Decrement control
  * Current value
  * Increment control
  * Reset control (↻) that sets the current value to the reset value
* Global controls:

  * **Reset All**: resets all counters to their reset values
* CZ scrolling is completely independent from the rest of the application.

---

### Counter Definitions and State File (CSV)

* Stored at: `SheetRoot/Counters.csv`
* This file is **manually editable** and is **read on application launch**.
* It is the authoritative source for **both counter definitions and current values**.
* There is **no separate runtime state file**.

#### Format

Each row represents one counter and must contain **exactly four logical fields**:

1. `id` (string)
2. `name` (string)
3. `reset` (number, ^-?\d+$)
4. `current` (number, ^-?\d+$)

There is **no header row**.

Example:

```
hp,Health,15,12
mp,Mana,32,32
hd,Hit Dice,4,2
pots,Potions,6,6
```

#### Parsing and Error Handling (Intentional Defaults)

* Every row is parsed.
* If a row does **not** contain exactly four values:

  * Treat it as: `error,error,-1,-1`
* If `reset` or `current` is blank or non-numeric:

  * Treat the row as an **error**.
* Malformed rows are therefore **visible in the UI** rather than silently discarded.

#### ID Stability Rule

* The `id` field is the **stable identity** of a counter.
* Changing a counter’s `name` preserves its state.
* Changing a counter’s `id` creates a **new counter**.
* If multiple rows share the same `id`, all subsequent duplicates are treated as **errors**.

---

### Runtime Interaction Model (CSV-Authoritative)

After application launch:

* All counter data is sourced from **in-memory state only**.
* No runtime reads of `Counters.csv` occur.
* Any user interaction that changes a counter value updates:

  1. In-memory state
  2. The CSV file on disk

For any interaction (increment, decrement, reset, reset all, inline edit):

1. Modify the in-memory counter state.
2. Atomically write the **entire CSV file** back to `Counters.csv`.

The UI renders directly from in-memory state.
The file is never re-read while the application is running.

---

### Direct Manipulation

* Double-clicking a counter’s displayed number turns it into an inline text field.
* This edits the **current value only**, not the reset value.
* Commit on Enter or blur of a numeric value.
* Cancel on Escape.
* Cancel on Enter or blur of a non-numeric value.

---

### File Safety and Concurrency

* All writes to `Counters.csv` are **atomic** (write temp file, then replace).
* The application enforces a **single-instance lock** at startup.
* If another instance is already running, the second instance must not take control.
* External edits to the CSV file while the app is running are unsupported and undefined behavior.

---

## 2) Text Subsystem

### Purpose

A flexible navigation and content workspace called the **Text Zone (TZ)**, backed entirely by a
snapshot of folders and plain text files.

---

### File System as Structure

* Root directory: `SheetRoot/`
* Each section’s content is stored in a file named `text.md` inside that folder. If this file doesn’t
  exist, it is assumed to be blank.
* The TZ ignores anything that is not a folder or a file called `text.md`.

Example:

```
SheetRoot/
text.md
counters.csv
1Inventory/
text.md
1Backpack/
text.md
2Equipment/
2Spells/
text.md
```

---

### UI Navigation Model

#### Persistent Top Row (Root Sections)

* The first level of folders under `SheetRoot` is displayed as a **row of tabs/buttons**.
* This row is always visible to allow quick switching between top-level sections.

#### Deeper Navigation (Single Stacked Column)

* Selecting a top-level section shows a single column listing its immediate subfolders.
* Selecting a subfolder navigates deeper.
* The column panel is replaced in-place (no multi-column expansion).
* A **Back** button navigates one level upward.

#### Content Area

* Fixed size.
* Displays the contents of the selected folder’s `text.md`.
* If `text.md` is missing, the content area is blank.

---

### Ordering via Hidden Prefix Character

* Sorting is alphabetical based on folder name.
* The **first character** of each folder name is hidden in the UI.
* Users control order by naming folders with prefix characters.

Example:

* On disk: `1Inventory`, `2Spells`, `3Stats`
* In UI: `Inventory`, `Spells`, `Stats`

---

### Editing Workflow

* All structure changes are performed via the filesystem:

  * Creating, renaming, deleting folders
  * Editing `text.md` files externally
* The Text subsystem is **read only on application launch**.
* No live refresh occurs while the app is running.

---

## 3) System Architecture and Principles

### Two Separate Systems

The application consists of two non-connected parts:

1. **Counters**

   * Definitions and state: `Counters.csv` (manual + app-managed)
2. **Text**

   * Structure and content: folder tree + `text.md` files (manual, launch-only)

There are no dependencies or references between the two systems.

---

### Core Design Principles

* Files are the source of truth.
* UI is a projection of disk state.
* Manual authoring first; no automation or rule enforcement.
* Safety through simplicity and explicit control.
* External editors are preferred for content creation.
* Minimal hidden logic; behavior is predictable and visible.

---

### One-Line Description

A two-part, file-defined, manually authored character/workspace UI: Counters rendered from a single
CSV that stores both definition and live state, and Text rendered from a prefix-ordered folder tree
of plain text sections.

---

### Software used

Python
Git
GitHub
Windows
PowerShell
Text editor / IDE
Dear ImGui
pyimgui
OpenGL

---

If you want, the **next clean step** is to write the **formal CSV write rules** (exact column order, numeric coercion, and error emission) as a short spec block so the implementation can’t drift.
