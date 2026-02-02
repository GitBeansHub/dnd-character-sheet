Below is a **menu of next directions**, grouped by concern. No ordering implied. Pick **one** and we go one step at a time.

**Tree / Data Model**

* Add `parent` wiring during tree construction
* Add a simple debug walker to print the tree as an indented hierarchy
* Decide whether to include non-folder files (future-proofing)

**Navigation State**

* Introduce `current_node` instead of passing raw text everywhere
* Implement “enter folder” (select child)
* Implement “back” using `parent`
* Decide how root navigation should look visually

**UI Integration**

* Replace `md_text` with `current_node.content`
* Render top bar buttons from `root.children`
* Render side nav from `current_node.children`
* Add visual feedback for selected node

**Filesystem Semantics**

* Decide whether to eagerly create missing `text.md` (you currently do)
* Separate “read-only snapshot” vs “future write mode”
* Decide how new folders should be named (prefix rules)

**Error Handling / Safety**

* Handle unreadable folders/files
* Handle non-UTF8 text.md gracefully
* Decide what happens if `sheetroot` is missing or empty

**Architecture Cleanup**

* Move UI layout constants into a config section
* Separate “model” (tree) from “rendering” (ImGui)
* Rename functions to reflect intent instead of UI zones

**Learning / Exploration**

* Replace one `draw_*` function with buttons instead of raw text
* Log navigation changes to console for clarity
* Step through tree creation with prints to solidify recursion understanding

