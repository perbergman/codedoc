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

def scan_project(project_path, generate_readme_flag=False):
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
    
    # Parse arguments
    args = parser.parse_args()
    
    # Ensure output has HTML extension
    if not args.output.lower().endswith('.html'):
        args.output += '.html'
    
    # Print settings
    print(f"Scanning projects in {args.directory}")
    print(f"README generation is {'enabled' if args.generate_readmes else 'disabled'}")
    
    # Find all projects
    projects = []
    readme_count = 0
    
    for item in os.listdir(args.directory):
        item_path = os.path.join(args.directory, item)
        if os.path.isdir(item_path) and not item.startswith('.'):
            project_info = scan_project(item_path, args.generate_readmes)
            projects.append(project_info)
    
    print(f"Found {len(projects)} projects")
    
    # Create HTML index
    create_html_index(projects, args.output)

if __name__ == '__main__':
    main()
