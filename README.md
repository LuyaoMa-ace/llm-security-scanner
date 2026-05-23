# LLM Security Scanner

A security analysis tool that uses **Claude (claude-sonnet-4-20250514)** to detect vulnerabilities in Python source code. Identifies issues like command injection, path traversal, hardcoded secrets, and code injection — with severity ratings and fix suggestions.

Built as a research prototype exploring LLM-based static analysis for open-source software security.

---

## Features

- **4 vulnerability types** detected out of the box: Command Injection, Path Traversal, Hardcoded Secrets, Code Injection
- **Severity classification**: HIGH / MEDIUM / LOW
- **Line-level precision**: points to the exact line of vulnerable code
- **Fix suggestions**: actionable recommendations for each issue
- **Two interfaces**: interactive web demo + CLI tool

---

## Project Structure

```
llm-security-scanner/
├── index.html              # Web demo (open in browser)
├── scanner.py              # CLI tool
├── examples/
│   ├── command_injection.py
│   ├── path_traversal.py
│   ├── hardcoded_secret.py
│   └── code_injection.py
└── README.md
```

---

## Setup

### 1. Get an Anthropic API key

Sign up at [console.anthropic.com](https://console.anthropic.com) and create an API key.

### 2. Set your API key

**macOS / Linux:**
```bash
export ANTHROPIC_API_KEY=your_key_here
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY = "your_key_here"
```

### 3. Install dependencies (CLI only)

```bash
pip install anthropic
```

---

## Usage

### Web Demo

1. Open `index.html` in your browser
2. Select a preset from the left panel, or paste your own Python code
3. Click **Analyze Code**
4. View the security report with severity badges and fix suggestions

> Note: The web demo calls the Anthropic API directly from the browser. Your API key is not required in the HTML — the demo uses the Claude.ai proxy. For self-hosted use, add your key to the fetch headers in `index.html`.

---

### CLI Tool

```bash
python scanner.py <path_to_file>
```

**Examples:**

```bash
# Scan a single file
python scanner.py examples/command_injection.py

# Scan your own code
python scanner.py myproject/app.py
```

**Sample output:**

```
============================================================
  LLM Security Scanner — powered by Claude
============================================================

Scanning: examples/command_injection.py
Sending to Claude for analysis...

Summary:  2 HIGH  0 MEDIUM  1 LOW

Issues found:

Issue 1
  Type      Command Injection
  Severity  HIGH
  Line      line 6
  Problem   os.system() passes raw user input directly to the shell
  Fix       Use subprocess.run() with a list of arguments and shell=False

Issue 2
  Type      Command Injection
  Severity  HIGH
  Line      line 11
  Problem   subprocess.call() with shell=True enables shell injection
  Fix       Pass arguments as a list: subprocess.call(["ping", "-c", "1", hostname])
...
```

---

## Example Vulnerabilities

| File | Vulnerability | Severity |
|------|--------------|----------|
| `command_injection.py` | `os.system(user_input)` | HIGH |
| `path_traversal.py` | `open(filename)` without validation | MEDIUM |
| `hardcoded_secret.py` | API keys in source code | HIGH |
| `code_injection.py` | `eval(user_input)` | HIGH |

---

## How It Works

1. The tool reads the Python source file
2. Sends it to Claude with a structured security analysis prompt
3. Claude returns a JSON array of detected issues
4. The tool renders results with severity, location, and fix suggestions

The prompt instructs Claude to act as a security analyst and return structured JSON — enabling reliable parsing and display.

---

## Screenshot

![Security Scanner Web Demo](screenshot.png)

*(Add a screenshot of the web demo here)*

---

## Limitations

- Analysis quality depends on the LLM — may produce false positives or miss subtle issues
- Best used as a complement to traditional static analysis tools (Bandit, Semgrep)
- Currently supports Python only

---

## Related Work

This prototype is inspired by research on using LLMs for automated security assessment of open-source repositories, including vulnerability detection, malware pattern recognition, and supply-chain security analysis.

---

## Author

**Luyao Ma**  
M.Sc. Artificial Intelligence — University of Bologna  
[github.com/LuyaoMa-ace](https://github.com/LuyaoMa-ace)
