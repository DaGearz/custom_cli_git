# 🧠 High-Level View of Daggit CLI Code

This guide walks through the architecture and logic of a simple Python-based
version control system called `daggit`. Each section explains a different part
of the codebase.

---

### ✍️ Purpose:

> This is meant to be used as a guide if someone wants to create their own
> version control system in Python.

---

## 📦 Used Modules

- `argparse`
- `os`
- `hashlib`
- `datetime` (from `datetime`)

---

## 🛠️ Define Variables for Reusable Paths

These include:

- `.daggit/`
- `.daggit/objects/`
- `.daggit/commits/`
- `.daggit/index`
- `.daggit/logs/`

---

## 🚀 CLI Initialization

- Set up `ArgumentParser`
- Add arguments for:
  - `command`: the CLI action (e.g. `init`, `add`, `commit`, etc.)
  - `target`: file name or commit message (optional)
- Use `parse_args()` to retrieve values

---

## 🧱 INIT Logic

### Purpose:

Create the repository folder and its subdirectories.

### Steps:

- Check if `.daggit/` exists
  - ✅ If yes → print "Repository already initialized"
  - ❌ If no →
    - Create `.daggit/`, `.daggit/objects/`, and `.daggit/commits/`
    - Print "Initialized Daggit repository"

---

## ➕ ADD Logic

### Purpose:

Stage a file by storing its content in the objects directory and logging its
hash in `.daggit/index`.

### Steps:

- Exit early if:
  - `.daggit/` doesn't exist
  - No target file provided
  - File does not exist
- Read the file as binary content
- Hash the content using SHA1
- Construct a path using the hash in `.daggit/objects/`
- If that file doesn't exist:
  - Create and write the file
  - Print "File stored as: <hash>"
- Else:
  - Print "File already stored"
- Append the following to `.daggit/index`:
  ```
  <hash> <filename>
  ```

---

## 💾 COMMIT Logic

### Purpose:

Create a snapshot of the staged index.

### Steps:

- Exit early if:
  - `.daggit/` or `.daggit/index` doesn't exist
- Read `.daggit/index` into a string
- If index is empty → print "Nothing to commit"
- Hash the index content (encode as bytes)
- Generate a commit hash
- Check if `.daggit/commits/<hash>` exists
  - ✅ If yes → print "There are no updates to commit"
  - ❌ If no →
    - Capture `args.target` as commit message
    - Capture current timestamp
    - Write to `.daggit/commits/<hash>`:
      ```
      Timestamp: <timestamp>
      Message: <message>
      <contents of index>
      ```
    - Print "Committed as: <hash>"

---

## 📜 LOG Logic

### Purpose:

Show the history of all commits and save it to a logs file.

### Steps:

- Exit early if `.daggit/commits/` doesn't exist or is empty
- Create `.daggit/logs/` if needed
- Get list of commit files
- Sort by modification time, newest first
- For each file:
  - Read first two lines → timestamp and message
  - Append this info to `.daggit/logs/logs.txt`
  - Print to terminal:
    ```
    Commit hash: <hash>
    Timestamp: ...
    Message: ...
    ----------------------------------------
    ```

---

## 📊 STATUS Logic

### Purpose:

Display the difference between what's in the index and what's in the current
directory:

- ✅ Staged (unchanged)
- 🟡 Modified (changed since added)
- 🔴 Untracked (never staged)

### Steps:

- Create three arrays:
  - `staged`, `modified`, `untracked`
- Build a dictionary from `.daggit/index`:
  ```python
  { filename: hash }
  ```
- Loop over each file in the working directory:
  - Skip hidden files and `daggit.py`
  - If it's a regular file:
    - Read file as bytes
    - Compute hash
    - Compare with index:
      - ✅ If matches → staged
      - 🟡 If different → modified
    - If not in index → untracked
- Print lists under headings:
  - Staged files
  - Modified files
  - Untracked files

---

## ✅ Todo

- ❗ Track deleted files (exist in index, but not in folder)
- ➕ Add a `.daggit/HEAD` to point to latest commit
- 🔁 Implement undo/rollback support
- 🌲 Branching system
- 🎨 Color output with `colorama`

---

🛠 Built as a custom Python CLI tool to learn core version control concepts.
