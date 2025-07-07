# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based project scanner that generates HTML indexes of code projects. The main script (`code-project-scanner.py`) analyzes directories containing multiple projects, detects their types and languages, and creates a comprehensive HTML index.

## Commands

### Running the Scanner
```bash
python3 code-project-scanner.py <directory> [-o output.html] [-g] [-i] [-r] [-G] [-p] [-f FILTER]
```

Options:
- `directory`: Path to directory containing projects to scan (use ".." to scan parent directory)
- `-o, --output`: Output HTML filename (default: project_index.html)
- `-g, --generate-readmes`: Automatically generate README.md files for projects lacking them
- `-i, --generate-gitignore`: Generate language-specific .gitignore files
- `-r, --init-repos`: Initialize git repositories for projects without them
- `-G, --github`: Create GitHub repositories using gh CLI
- `-p, --private`: Make GitHub repositories private (default: public)
- `-f, --filter`: Filter for GitHub repo creation (e.g., `-f Python JavaScript`)

### Development
```bash
# Make the script executable
chmod +x code-project-scanner.py

# Run with default output
./code-project-scanner.py /path/to/projects

# Run with custom output and README generation
./code-project-scanner.py /path/to/projects -o index.html -g

# Run with all features for Python projects
./code-project-scanner.py .. -g -i -r -G -f Python

# Run with git initialization and private GitHub repos
./code-project-scanner.py .. -r -G -p
```

## Architecture

The scanner works by:
1. Iterating through subdirectories in the specified path
2. Detecting project types based on marker files (package.json, pom.xml, requirements.txt, etc.)
3. Analyzing file extensions to determine primary language
4. Extracting descriptions from existing README files
5. Optionally generating README.md files for projects without documentation
6. Optionally generating language-specific .gitignore files
7. Optionally initializing git repositories with initial commit
8. Optionally creating GitHub repositories using gh CLI with filtering support
9. Creating an HTML table with project information including name, type, language, status, last modified date, location, and description

Key functions:
- `scan_project()`: Analyzes individual project directories
- `generate_readme()`: Creates basic README.md files when requested
- `get_gitignore_template()`: Returns language-specific .gitignore templates
- `generate_gitignore()`: Creates .gitignore files based on detected language
- `init_git_repo()`: Initializes git repository and makes initial commit
- `create_github_repo()`: Creates GitHub repository using gh CLI
- `create_html_index()`: Generates the final HTML output with styled table

The tool supports templates for Python, JavaScript, TypeScript, Java, Go, Rust, Swift, and other languages.