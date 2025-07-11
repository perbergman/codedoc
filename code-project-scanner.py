#!/usr/bin/env python3
"""
Simple HTML Project Index Generator
"""

import os
import sys
import glob
import re
import datetime
import argparse
import subprocess
import json

def generate_readme(project_info, output_path):
    """Generate a README.md file for a project."""
    project_name = project_info['name']
    project_type = project_info['type']
    language = project_info['language']
    
    # Create a basic description
    description = f"This is a {project_type} project written primarily in {language}."
    
    # Generate features based on project type
    features = []
    if 'Web' in project_type:
        features.append("Web interface")
    if 'API' in project_type:
        features.append("API endpoints")
    if 'Mobile' in project_type:
        features.append("Mobile application interface")
    
    # Add a default feature if none detected
    if not features:
        features.append("Core functionality")
    
    # Create README content
    readme_content = f"# {project_name}\n\n"
    readme_content += "## Description\n\n"
    readme_content += f"{description}\n\n"
    readme_content += "## Core Features\n\n"
    
    for feature in features:
        readme_content += f"- {feature}\n"
    
    readme_content += f"\n## Technologies\n\n"
    readme_content += f"- Primary language: {language}\n"
    
    # Add keywords
    keywords = [language.lower(), project_type.lower().split(' ')[0]]
    readme_content += f"\n---\n\n"
    readme_content += f"**Keywords**: {', '.join(keywords)}\n"
    readme_content += f"\n*Last updated: {datetime.datetime.now().strftime('%Y-%m-%d')}*\n"
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    return True

def get_gitignore_template(language, project_type):
    """Get appropriate .gitignore template based on language/type."""
    templates = {
        'Python': """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# C extensions
*.so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
pip-wheel-metadata/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.py,cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Django stuff:
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal

# Flask stuff:
instance/
.webassets-cache

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# IPython
profile_default/
ipython_config.py

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery stuff
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
""",
        'JavaScript': """# Logs
logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
lerna-debug.log*

# Diagnostic reports
report.[0-9]*.[0-9]*.[0-9]*.[0-9]*.json

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Directory for instrumented libs generated by jscoverage/JSCover
lib-cov

# Coverage directory used by tools like istanbul
coverage
*.lcov

# nyc test coverage
.nyc_output

# Grunt intermediate storage
.grunt

# Bower dependency directory
bower_components

# node-waf configuration
.lock-wscript

# Compiled binary addons
build/Release

# Dependency directories
node_modules/
jspm_packages/

# TypeScript v1 declaration files
typings/

# TypeScript cache
*.tsbuildinfo

# Optional npm cache directory
.npm

# Optional eslint cache
.eslintcache

# Microbundle cache
.rpt2_cache/
.rts2_cache_cjs/
.rts2_cache_es/
.rts2_cache_umd/

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env
.env.test

# parcel-bundler cache
.cache

# Next.js build output
.next

# Nuxt.js build / generate output
.nuxt
dist

# Gatsby files
.cache/
public

# vuepress build output
.vuepress/dist

# Serverless directories
.serverless/

# FuseBox cache
.fusebox/

# DynamoDB Local files
.dynamodb/

# TernJS port file
.tern-port
""",
        'TypeScript': """# See JavaScript template
node_modules/
dist/
*.tsbuildinfo
.npm
.eslintcache
coverage/
.nyc_output
.env
.env.test
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.DS_Store
""",
        'Java': """# Compiled class file
*.class

# Log file
*.log

# BlueJ files
*.ctxt

# Mobile Tools for Java (J2ME)
.mtj.tmp/

# Package Files #
*.jar
*.war
*.nar
*.ear
*.zip
*.tar.gz
*.rar

# virtual machine crash logs
hs_err_pid*

# Maven
target/
pom.xml.tag
pom.xml.releaseBackup
pom.xml.versionsBackup
pom.xml.next
release.properties
dependency-reduced-pom.xml
buildNumber.properties
.mvn/timing.properties
.mvn/wrapper/maven-wrapper.jar

# Gradle
.gradle
build/
!gradle/wrapper/gradle-wrapper.jar
!**/src/main/**/build/
!**/src/test/**/build/

# IntelliJ IDEA
.idea
*.iws
*.iml
*.ipr
out/
!**/src/main/**/out/
!**/src/test/**/out/

# Eclipse
.apt_generated
.classpath
.factorypath
.project
.settings
.springBeans
.sts4-cache

# NetBeans
/nbproject/private/
/nbbuild/
/dist/
/nbdist/
/.nb-gradle/

# VS Code
.vscode/

# OS files
.DS_Store
""",
        'Go': """# Binaries for programs and plugins
*.exe
*.exe~
*.dll
*.so
*.dylib

# Test binary, built with go test -c
*.test

# Output of the go coverage tool
*.out

# Dependency directories
vendor/

# Go workspace file
go.work

# Environment variables
.env

# IDE specific files
.idea/
.vscode/
*.swp
*.swo
*~

# OS files
.DS_Store
""",
        'Rust': """# Generated by Cargo
# will have compiled files and executables
debug/
target/

# Remove Cargo.lock from gitignore if creating an executable
# Cargo.lock

# These are backup files generated by rustfmt
**/*.rs.bk

# MSVC Windows builds of rustc generate these
*.pdb
""",
        'Swift': """# Xcode
#
# gitignore contributors: remember to update Global/Xcode.gitignore, Objective-C.gitignore & Swift.gitignore

## User settings
xcuserdata/

## compatibility with Xcode 8 and earlier (ignoring not required starting Xcode 9)
*.xcscmblueprint
*.xccheckout

## compatibility with Xcode 3 and earlier (ignoring not required starting Xcode 4)
build/
DerivedData/
*.moved-aside
*.pbxuser
!default.pbxuser
*.mode1v3
!default.mode1v3
*.mode2v3
!default.mode2v3
*.perspectivev3
!default.perspectivev3

## Obj-C/Swift specific
*.hmap

## App packaging
*.ipa
*.dSYM.zip
*.dSYM

## Playgrounds
timeline.xctimeline
playground.xcworkspace

# Swift Package Manager
.build/
Packages/
Package.pins
Package.resolved
.swiftpm
*.xcodeproj

# CocoaPods
Pods/

# Carthage
Carthage/Build/

# Accio dependency management
Dependencies/
.accio/

# fastlane
fastlane/report.xml
fastlane/Preview.html
fastlane/screenshots/**/*.png
fastlane/test_output

# Code Injection
iOSInjectionProject/
""",
        'Default': """# OS generated files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Editor directories and files
.idea
.vscode
*.suo
*.ntvs*
*.njsproj
*.sln
*.sw?

# Logs
logs
*.log

# Environment variables
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# Temporary files
*.tmp
*.temp
.tmp/
.temp/
"""
    }
    
    # Try to match by language first
    if language in templates:
        return templates[language]
    
    # Try to match by project type
    if 'JavaScript' in project_type or 'Node.js' in project_type:
        return templates['JavaScript']
    elif 'Java' in project_type:
        return templates['Java']
    elif 'Swift' in project_type or 'iOS' in project_type or 'macOS' in project_type:
        return templates['Swift']
    
    # Return default template
    return templates['Default']

def generate_gitignore(project_path, language, project_type):
    """Generate a .gitignore file for the project."""
    gitignore_path = os.path.join(project_path, '.gitignore')
    
    # Check if .gitignore already exists
    if os.path.exists(gitignore_path):
        return False
    
    # Get appropriate template
    template = get_gitignore_template(language, project_type)
    
    # Write .gitignore file
    with open(gitignore_path, 'w', encoding='utf-8') as f:
        f.write(template)
    
    print(f"  Generated .gitignore for {os.path.basename(project_path)}")
    return True

def init_git_repo(project_path):
    """Initialize a git repository if not already initialized."""
    git_dir = os.path.join(project_path, '.git')
    
    # Check if git repo already exists
    if os.path.exists(git_dir):
        return False
    
    try:
        # Initialize git repo
        subprocess.run(['git', 'init'], cwd=project_path, capture_output=True, text=True, check=True)
        
        # Make initial commit if there are files
        files_to_commit = subprocess.run(['git', 'status', '--porcelain'], 
                                       cwd=project_path, capture_output=True, text=True)
        
        if files_to_commit.stdout.strip():
            # Add all files
            subprocess.run(['git', 'add', '.'], cwd=project_path, capture_output=True, text=True, check=True)
            
            # Make initial commit
            subprocess.run(['git', 'commit', '-m', 'Initial commit'], 
                         cwd=project_path, capture_output=True, text=True, check=True)
        
        print(f"  Initialized git repository for {os.path.basename(project_path)}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Failed to initialize git repo for {os.path.basename(project_path)}: {e}")
        return False

def create_github_repo(project_path, project_name, private=False):
    """Create a GitHub repository using gh CLI."""
    try:
        # Check if we're in a git repo first
        git_check = subprocess.run(['git', 'rev-parse', '--git-dir'], 
                                 cwd=project_path, capture_output=True, text=True)
        
        if git_check.returncode != 0:
            print(f"  Skipping GitHub repo creation for {project_name} - not a git repository")
            return False
        
        # Check if remote already exists
        remote_check = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                    cwd=project_path, capture_output=True, text=True)
        
        if remote_check.returncode == 0:
            print(f"  Remote already exists for {project_name}")
            return False
        
        # Create GitHub repo
        visibility = '--private' if private else '--public'
        create_cmd = ['gh', 'repo', 'create', project_name, visibility, '--confirm']
        
        result = subprocess.run(create_cmd, cwd=project_path, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"  Created GitHub repository for {project_name}")
            
            # Push to remote
            push_result = subprocess.run(['git', 'push', '-u', 'origin', 'main'], 
                                       cwd=project_path, capture_output=True, text=True)
            
            if push_result.returncode != 0:
                # Try with master branch
                subprocess.run(['git', 'push', '-u', 'origin', 'master'], 
                             cwd=project_path, capture_output=True, text=True)
            
            return True
        else:
            print(f"  Failed to create GitHub repo for {project_name}: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"  Error creating GitHub repo for {project_name}: {e}")
        return False

def scan_project(project_path, generate_readme_flag=False, generate_gitignore_flag=False, init_git_flag=False):
    """Analyze a single project directory."""
    project_name = os.path.basename(project_path)
    print(f"Analyzing: {project_name}")
    
    # Detect project type
    project_type = "Unknown"
    if os.path.exists(os.path.join(project_path, "package.json")):
        project_type = "JavaScript/Node.js"
    elif os.path.exists(os.path.join(project_path, "pom.xml")):
        project_type = "Java (Maven)"
    elif os.path.exists(os.path.join(project_path, "build.gradle")):
        project_type = "Java/Kotlin (Gradle)"
    elif os.path.exists(os.path.join(project_path, "go.mod")):
        project_type = "Go"
    elif os.path.exists(os.path.join(project_path, "Cargo.toml")):
        project_type = "Rust"
    elif os.path.exists(os.path.join(project_path, "requirements.txt")) or glob.glob(os.path.join(project_path, "*.py")):
        project_type = "Python" 
    elif os.path.exists(os.path.join(project_path, "Dockerfile")):
        project_type = "Docker"
    elif glob.glob(os.path.join(project_path, "*.xcodeproj")) or glob.glob(os.path.join(project_path, "*.xcworkspace")):
        project_type = "iOS/macOS (Swift/Objective-C)"
    # Additional check for Xcode projects that might be in subdirectories
    else:
        for root, dirs, _ in os.walk(project_path):
            if any(d.endswith('.xcodeproj') or d.endswith('.xcworkspace') for d in dirs):
                project_type = "iOS/macOS (Swift/Objective-C)"
                break
            if glob.glob(os.path.join(root, '*.swift')):
                project_type = "iOS/macOS (Swift)"
                break
    
    # Detect primary language
    language = "Unknown"
    ext_counts = {}
    lang_map = {
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".py": "Python",
        ".java": "Java",
        ".kt": "Kotlin",
        ".go": "Go",
        ".rs": "Rust",
        ".html": "HTML",
        ".css": "CSS",
        ".sh": "Shell",
        ".erl": "Erlang",
        ".sql": "SQL",
        ".sol": "Solidity",
        ".scss": "SCSS",
        ".swift": "Swift",
        ".m": "Objective-C",
        ".pl": "Prolog",
        ".pro": "Prolog",
        ".P": "Prolog",
        ".circom": "Circom",
        ".vy": "Vyper",
        ".rb": "Ruby",
        ".php": "PHP",
        ".c": "C",
        ".cpp": "C++",
        ".cs": "C#",
        ".lua": "Lua",
        ".r": "R",
        ".scala": "Scala",
        ".clj": "Clojure",
        ".ex": "Elixir",
        ".dart": "Dart",
        ".nim": "Nim",
        ".zig": "Zig",
        ".v": "V"
    }
    
    for root, _, files in os.walk(project_path):
        for file in files:
            _, ext = os.path.splitext(file.lower())
            if ext in lang_map:
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
    
    if ext_counts:
        primary_ext = max(ext_counts, key=lambda k: ext_counts.get(k, 0))
        if primary_ext in lang_map:
            language = lang_map[primary_ext]
    
    # Get last modified date
    last_modified = "Unknown"
    try:
        timestamp = os.path.getmtime(project_path)
        last_modified = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    except:
        pass
    
    # Get status based on last modified date
    status = "Active"  # Default to active
    
    # Check if README exists
    readme_exists = False
    for readme_name in ["README.md", "Readme.md", "readme.md", "README.txt", "README"]:
        if os.path.exists(os.path.join(project_path, readme_name)):
            readme_exists = True
            break
    
    # Get description from README if it exists
    description = "No description available."
    if readme_exists:
        readme_files = glob.glob(os.path.join(project_path, "README*"))
        if readme_files:
            try:
                with open(readme_files[0], 'r', encoding='utf-8', errors='ignore') as f:
                    readme_content = f.read()
                
                # Look for a description section
                overview_match = re.search(r'#+\s*(?:Project\s+Overview|Overview|About|Description|Introduction)\s*\n+(.+?)(?:\n#+|\n\n|$)', 
                                         readme_content, re.DOTALL | re.IGNORECASE)
                if overview_match:
                    description = overview_match.group(1).strip()
                else:
                    # Find first substantial paragraph
                    paragraphs = re.findall(r'\n\n([^#\n][^\n]{30,})', readme_content, re.DOTALL)
                    if paragraphs:
                        description = paragraphs[0].strip()
            except:
                pass
    
    # Generate README if requested and none exists
    if generate_readme_flag and not readme_exists:
        readme_path = os.path.join(project_path, "README.md")
        print(f"  Generating README.md for {project_name}")
        
        project_info = {
            'name': project_name,
            'path': project_path,
            'type': project_type,
            'language': language
        }
        
        generate_readme(project_info, readme_path)
        
        # Update description from the new README
        try:
            with open(readme_path, 'r', encoding='utf-8') as f:
                description = "This is a generated README."
        except:
            pass
    
    # Generate .gitignore if requested
    if generate_gitignore_flag:
        generate_gitignore(project_path, language, project_type)
    
    # Initialize git repo if requested
    if init_git_flag:
        init_git_repo(project_path)
    
    return {
        'name': project_name,
        'path': project_path,
        'type': project_type, 
        'language': language,
        'status': status,
        'last_modified': last_modified,
        'description': description
    }

def create_html_index(projects, output_file):
    """Create HTML index of projects."""
    with open(output_file, 'w', encoding='utf-8') as f:
        # HTML header
        f.write('<!DOCTYPE html>\n')
        f.write('<html>\n')
        f.write('<head>\n')
        f.write('    <meta charset="UTF-8">\n')
        f.write('    <title>Code Projects Index</title>\n')
        f.write('    <style>\n')
        f.write('        body { font-family: Arial, sans-serif; margin: 20px; }\n')
        f.write('        table { border-collapse: collapse; width: 100%; }\n')
        f.write('        th { background-color: #4a86e8; color: white; font-weight: bold; text-align: left; padding: 8px; border: 1px solid #ddd; }\n')
        f.write('        tr:nth-child(even) { background-color: #e6f0ff; } /* Light blue for even rows */\n')
        f.write('        tr:nth-child(odd) { background-color: white; } /* White for odd rows */\n')
        f.write('        td { padding: 8px; border: 1px solid #ddd; vertical-align: top; }\n')
        f.write('        td.description { word-wrap: break-word; max-width: 500px; }\n')
        f.write('    </style>\n')
        f.write('</head>\n')
        f.write('<body>\n')
        f.write('    <h1>Code Projects Index</h1>\n')
        f.write(f'    <p>Contains information about {len(projects)} projects.</p>\n')
        
        # Start table
        f.write('    <table>\n')
        f.write('        <tr>\n')
        f.write('            <th>Project Name</th>\n')
        f.write('            <th>Type</th>\n')
        f.write('            <th>Language</th>\n')
        f.write('            <th>Status</th>\n')
        f.write('            <th>Last Updated</th>\n')
        f.write('            <th>Location</th>\n')
        f.write('            <th>Description</th>\n')
        f.write('        </tr>\n')
        
        # Project rows
        for project in sorted(projects, key=lambda p: p['name'].lower()):
            name = project['name']
            project_type = project['type']
            language = project['language']
            status = project['status']
            last_modified = project['last_modified']
            path = os.path.relpath(project['path'])
            
            # Handle description
            desc = project['description']
            desc = desc.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            desc = desc.replace('\n', '<br>')
            
            f.write('        <tr>\n')
            f.write(f'            <td>{name}</td>\n')
            f.write(f'            <td>{project_type}</td>\n')
            f.write(f'            <td>{language}</td>\n')
            f.write(f'            <td>{status}</td>\n')
            f.write(f'            <td>{last_modified}</td>\n')
            f.write(f'            <td>{path}</td>\n')
            f.write(f'            <td class="description">{desc}</td>\n')
            f.write('        </tr>\n')
        
        # Close table and HTML
        f.write('    </table>\n')
        f.write(f'    <p><em>Last updated: {datetime.datetime.now().strftime("%Y-%m-%d")}</em></p>\n')
        f.write('</body>\n')
        f.write('</html>')
    
    print(f"HTML index saved to {output_file}")

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate HTML index of code projects")
    parser.add_argument('directory', help='Directory containing projects')
    parser.add_argument('-o', '--output', default='project_index.html', help='Output HTML file')
    parser.add_argument('-g', '--generate-readmes', action='store_true', help='Generate READMEs for projects that need them')
    parser.add_argument('-i', '--generate-gitignore', action='store_true', help='Generate language-specific .gitignore files')
    parser.add_argument('-r', '--init-repos', action='store_true', help='Initialize git repositories for projects')
    parser.add_argument('-G', '--github', action='store_true', help='Create GitHub repositories for projects')
    parser.add_argument('-p', '--private', action='store_true', help='Make GitHub repositories private (default: public)')
    parser.add_argument('-f', '--filter', nargs='+', help='Filter for GitHub repo creation (e.g., Python JavaScript)')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Ensure output has HTML extension
    if not args.output.lower().endswith('.html'):
        args.output += '.html'
    
    # Print settings
    print(f"Scanning projects in {args.directory}")
    print(f"README generation is {'enabled' if args.generate_readmes else 'disabled'}")
    print(f".gitignore generation is {'enabled' if args.generate_gitignore else 'disabled'}")
    print(f"Git repo initialization is {'enabled' if args.init_repos else 'disabled'}")
    print(f"GitHub repo creation is {'enabled' if args.github else 'disabled'}")
    if args.github and args.filter:
        print(f"GitHub creation filter: {', '.join(args.filter)}")
    
    # Find all projects
    projects = []
    readme_count = 0
    
    for item in os.listdir(args.directory):
        item_path = os.path.join(args.directory, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            project_info = scan_project(item_path, args.generate_readmes, args.generate_gitignore, args.init_repos)
            projects.append(project_info)
            
            # Create GitHub repo if requested and matches filter
            if args.github:
                should_create = True
                if args.filter:
                    # Check if language or project type matches filter
                    language_match = project_info['language'] in args.filter
                    type_match = any(f in project_info['type'] for f in args.filter)
                    should_create = language_match or type_match
                
                if should_create:
                    create_github_repo(project_info['path'], project_info['name'], args.private)
    
    print(f"Found {len(projects)} projects")
    
    # Create HTML index
    create_html_index(projects, args.output)

if __name__ == '__main__':
    main()
