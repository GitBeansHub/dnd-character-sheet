DND Character Sheet 

### Project Summary

This project is a manual-entry, zone-based character sheet/workspace system (tabletop RPG–oriented) built around two completely separate subsystems: **Counters** and **Text**. Each subsystem has its own editor where **plain text is the source of truth**, and the UI is a projection of that text. The system avoids automation and rule enforcement; it focuses on flexibility, direct control, and preventing accidental edits.

---

## 1) Counters Subsystem

### Purpose

A persistent, independently scrolling area for frequently used numeric trackers (resources, HP, charges, etc.). This area is called the **Counter Zone (CZ)**.

### Counter Zone (CZ) UI

* Displays a vertical list of counters.
* Each counter shows:

  * Name
  * Decrement control
  * Current value
  * Increment control
  * Reset control (↻) that resets the current value to the counter’s reset value
* Global controls in CZ:

  * **Reset All**: resets every counter to its reset value
  * **Edit Counters**: opens the Counter Editor
* CZ scroll behavior is isolated from the rest of the app.

### Counter Editor (CE)

* A text editor used to define counters as lines of text.
* **Parsing rule (critical):**

  * **Name** = everything on the line except the last token
  * **Reset value** = the last token, must be a number
  * Example: `Level 1 Spell Slot 123` → name `Level 1 Spell Slot`, reset `123`
* Save/Cancel workflow:

  * Changes apply only on Save
  * Invalid lines (missing numeric final token) should be rejected or highlighted
* Runtime behavior:

  * Current values start at reset values
  * Reset returns current value to reset value
* Direct manipulation:

  * Double-clicking a counter’s displayed number in the CZ turns it into an inline text box for editing the **current value** (not the reset value), then commits on enter/blur and cancels on escape.

---

## 2) Text Subsystem

### Purpose

A flexible, user-defined navigation + content workspace called the **Text Zone (TZ)**. This system is for manually maintained content such as Inventory, Spells, Stats, Notes, Abilities, Links, People, etc. These are not special categories to the system; they are just user-defined structures.

### Text Zone (TZ) UI

* Shows structured text content driven by user-defined buttons/sections.
* Supports:

  * Free text blocks
  * Variable numbers of text columns
  * Rows/columns as organizational structures
  * Nested subsections (“sub-buttons”)
* Independent scrolling (separate from CZ).
* Editing safety:

  * Locking to prevent accidental edits
  * Save/Cancel editing workflow

### Zone Editor (ZE)

* A text editor that defines TZ structure and content.
* The entire editor is treated as a single string and decoded into zones/sections.
* **Indentation-based structure (Python-like):**

  * Indentation defines hierarchy (parent/child relationships).
  * Line order defines display order.
* Optional layout markers can exist (e.g., `ROW:`, `COLUMN:`) to express intent, but content remains manual-entry.
* The UI is generated from the ZE definition; ZE is authoritative.

### Hierarchy rules (positional concept)

* The intended navigation model supports nested “buttons”/sections.
* Sub-structure can be inferred by relative placement conceptually (right/below implies child), but the ZE provides explicit hierarchical definition through indentation.

---

## 3) System Architecture and Principles

### Two separate systems

* The application consists of **two non-connected parts**:

  1. **Counters** (CZ + CE)
  2. **Text** (TZ + ZE)
* No required references, dependencies, or shared structure between them.

### Core design principles

* Manual entry first: user types everything.
* Text is the source of truth: editors define content/structure; UI renders it.
* Safety: lock editing; require Save/Cancel; avoid accidental edits.
* Flexibility: add/remove/reorder content freely (especially in TZ); counters can be added/removed via CE.
* Minimal hidden logic: structure and relationships are visible and user-controlled.

---

### One-line description

A two-part, text-defined, manually authored character/workspace UI: **Counters** managed via a line-based Counter Editor and rendered in a Counter Zone, and **structured Text** managed via an indentation-based Zone Editor and rendered in a Text Zone—fully independent, flexible, and protected against accidental edits.

