#!/usr/bin/env python3
"""
Simple HTML Project Index Generator
"""

import os
import sys
import glob
import re
import datetime

def scan_projects(root_dir):
    """Scan for projects and collect their information."""
    projects = []
    exclude_dirs = {'.git', 'node_modules', 'venv', '.venv', 'dist', 'build', '__pycache__', '.idea', '.vscode'}
    
    for item in os.listdir(root_dir):
        project_path = os.path.join(root_dir, item)
        if not os.path.isdir(project_path) or item.startswith('.') or item in exclude_dirs:
            continue
            
        print(f"Analyzing: {item}")
        
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
        
        # Determine primary language based on files
        language = "Unknown"
        ext_counts = {}
        for root, _, files in os.walk(project_path):
            for file in files:
                _, ext = os.path.splitext(file.lower())
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
        
        if ext_counts:
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
                ".scss": "SCSS"
            }
            
            primary_ext = max(ext_counts, key=lambda k: ext_counts.get(k, 0) if k in lang_map else 0)
            language = lang_map.get(primary_ext, "Unknown")
            
        # Try to get last modified date (from git or file system)
        last_modified = "Unknown"
        import subprocess
        try:
            if os.path.isdir(os.path.join(project_path, ".git")):
                try:
                    output = subprocess.check_output(
                        ["git", "log", "-1", "--format=%cd", "--date=short"],
                        cwd=project_path, stderr=subprocess.PIPE, universal_newlines=True
                    )
                    last_modified = output.strip()
                except:
                    pass
            
            if last_modified == "Unknown":
                timestamp = os.path.getmtime(project_path)
                last_modified = datetime.datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
        except:
            pass
            
        # Determine status based on last modified date
        status = "Unknown"
        try:
            last_date = datetime.datetime.strptime(last_modified, "%Y-%m-%d")
            days_ago = (datetime.datetime.now() - last_date).days
            
            if days_ago < 90:  # 3 months
                status = "Active"
            elif days_ago < 365:  # 1 year
                status = "Maintenance"
            else:
                status = "Archived"
        except:
            pass
            
        # Get description from README
        description = "No description available."
        readme_files = glob.glob(os.path.join(project_path, "README*"))
        if readme_files:
            try:
                with open(readme_files[0], 'r', encoding='utf-8', errors='ignore') as f:
                    readme_content = f.read()
                    
                # Look for Project Overview section
                overview_match = re.search(r'#+\s*(?:Project\s+Overview|Overview|About|Description|Introduction)\s*\n+(.+?)(?:\n#+|\n\n|$)', 
                                         readme_content, re.DOTALL | re.IGNORECASE)
                if overview_match:
                    description = overview_match.group(1).strip()
                else:
                    # Try to find a substantial paragraph
                    paragraphs = re.findall(r'\n\n([^#\n][^\n]{30,})', readme_content, re.DOTALL)
                    if paragraphs:
                        description = paragraphs[0].strip()
            except:
                pass
                
        projects.append({
            'name': item,
            'path': project_path,
            'type': project_type,
            'language': language,
            'status': status,
            'last_modified': last_modified,
            'description': description
        })
    
    return projects

def write_html(projects, output_file):
    """Write HTML table of projects with alternating blue/white rows."""
    now = datetime.datetime.now().strftime("%Y-%m-%d")
    
    # Write HTML directly without string formatting for CSS
    with open(output_file, 'w', encoding='utf-8') as f:
        # HTML header and CSS
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
            # Escape HTML special characters
            name = project['name']
            project_type = project['type']
            language = project['language']
            status = project['status']
            last_modified = project['last_modified']
            path = os.path.relpath(project['path'])
            
            # Handle description - escape HTML and convert newlines
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
        f.write(f'    <p><em>Last updated: {now}</em><br>\n')
        f.write('    <em>Generated by Simple HTML Project Index Generator</em></p>\n')
        f.write('</body>\n')
        f.write('</html>')
    
    print(f"HTML index saved to {output_file}")

def main():
    # Check arguments
    if len(sys.argv) < 2:
        print("Usage: python simple-html-generator.py <project_directory> [output.html]")
        sys.exit(1)
    
    # Get directory and output file
    directory = sys.argv[1]
    output_file = "project_index.html"
    if len(sys.argv) >= 3:
        output_file = sys.argv[2]
    
    # Make sure output has HTML extension
    if not output_file.lower().endswith('.html'):
        output_file += '.html'
    
    # Scan projects
    print(f"Scanning projects in {directory}...")
    projects = scan_projects(directory)
    print(f"Found {len(projects)} projects.")
    
    # Generate HTML
    write_html(projects, output_file)

if __name__ == "__main__":
    main()
