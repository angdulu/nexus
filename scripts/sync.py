#!/usr/bin/env python3
import os
import re
import datetime

# Find the wiki directory relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WIKI_DIR = os.path.dirname(SCRIPT_DIR)

def parse_frontmatter(content):
    """
    Parses YAML frontmatter from the start of a markdown file.
    Returns (metadata_dict, body_content_string).
    """
    lines = content.split('\n')
    if not lines or lines[0].strip() != '---':
        return {}, content
    
    metadata = {}
    body_lines = []
    in_frontmatter = True
    
    for i in range(1, len(lines)):
        line = lines[i]
        if in_frontmatter:
            if line.strip() == '---':
                in_frontmatter = False
                continue
            if ':' in line:
                key, val = line.split(':', 1)
                key = key.strip()
                val = val.strip()
                
                # Strip quotes if present
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                elif val.startswith("'") and val.endswith("'"):
                    val = val[1:-1]
                
                # Parse arrays e.g., [a, b]
                if val.startswith('[') and val.endswith(']'):
                    val = [item.strip() for item in val[1:-1].split(',')]
                    # Clean quotes inside list
                    val = [v[1:-1] if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")) else v for v in val]
                
                metadata[key] = val
        else:
            body_lines.append(line)
            
    return metadata, '\n'.join(body_lines)

def get_h1_title(content):
    """
    Extracts the first H1 header title from markdown content.
    """
    for line in content.split('\n'):
        line_stripped = line.strip()
        if line_stripped.startswith('# '):
            return line_stripped[2:].strip()
    return None

def extract_existing_index_descriptions(index_path):
    """
    Parses the existing index.md to extract manual descriptions for existing links.
    Returns a dict mapping 'category/filename' -> description_string.
    """
    descriptions = {}
    if not os.path.exists(index_path):
        return descriptions
        
    link_pattern = re.compile(r'-\s+\[\[([^\]]+)\]\]\s+—\s+(.*?)\s*\(\d{4}-\d{2}-\d{2}\)')
    link_pattern_no_date = re.compile(r'-\s+\[\[([^\]]+)\]\]\s+—\s+(.*?)\s*$')
    
    with open(index_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Try to match with date
            m = link_pattern.search(line)
            if m:
                link, desc = m.groups()
                # Split display pipe if exists in link
                link_clean = link.split('|')[0].strip()
                descriptions[link_clean] = desc.strip()
                continue
            # Try to match without date
            m2 = link_pattern_no_date.search(line)
            if m2:
                link, desc = m2.groups()
                link_clean = link.split('|')[0].strip()
                descriptions[link_clean] = desc.strip()
                
    return descriptions

def format_link_display_name(filename):
    """
    Formats lowercase-with-hyphens filename to a clean title.
    Keeps acronyms uppercase.
    """
    words = filename.split('-')
    acronyms = {'ap', 'gpa', 'kisj', 'mcp', 'nhs', 'ode', 'emr', 'ui', 'ux', 'sat', 'cf', 'fda', 'who', 'mfds', 'jnuh'}
    formatted_words = []
    for w in words:
        if w.lower() in acronyms:
            formatted_words.append(w.upper())
        else:
            formatted_words.append(w.capitalize())
    return ' '.join(formatted_words)

def scan_category(category_name):
    """
    Scans a directory (notes, projects, sources) under WIKI_DIR.
    Returns a list of dicts with file metadata.
    """
    dir_path = os.path.join(WIKI_DIR, category_name)
    results = []
    if not os.path.exists(dir_path):
        return results
        
    for root, _, files in os.walk(dir_path):
        for file in files:
            if not file.endswith('.md') or file.startswith('.'):
                continue
            
            abs_path = os.path.join(root, file)
            filename_no_ext = os.path.splitext(file)[0]
            link_path = f"{category_name}/{filename_no_ext}"
            
            with open(abs_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            metadata, body = parse_frontmatter(content)
            
            h1 = get_h1_title(body)
            display_title = h1 if h1 else format_link_display_name(filename_no_ext)
            for prefix in ["Project: ", "Note: ", "Source: "]:
                if display_title.startswith(prefix):
                    display_title = display_title[len(prefix):]
            
            updated_date = metadata.get('updated')
            if not updated_date:
                updated_date = metadata.get('created')
            if not updated_date:
                mtime = os.path.getmtime(abs_path)
                updated_date = datetime.datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
                
            results.append({
                'filename': filename_no_ext,
                'link_path': link_path,
                'display_title': display_title,
                'description': metadata.get('description', ''),
                'status': metadata.get('status', ''),
                'updated': updated_date,
                'abs_path': abs_path
            })
            
    return results

def rebuild_index(index_path, existing_descriptions):
    """
    Rebuilds the projects, sources, and notes sections of index.md.
    """
    if not os.path.exists(index_path):
        print(f"Warning: Index file not found at {index_path}")
        return
        
    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    projects = scan_category('projects')
    sources = scan_category('sources')
    notes = scan_category('notes')
    
    projects.sort(key=lambda x: x['updated'], reverse=True)
    sources.sort(key=lambda x: x['updated'], reverse=True)
    notes.sort(key=lambda x: x['updated'], reverse=True)
    
    def format_section_lines(items, category):
        lines = []
        for item in items:
            desc = item['description']
            if not desc:
                desc = existing_descriptions.get(item['link_path'], '')
            if not desc:
                desc = f"Synthesized notes on {item['display_title']}" if category == 'notes' else f"Project plan for {item['display_title']}"
            
            link_part = item['link_path']
            if item['filename'] == 'andy':
                link_part = f"{item['link_path']}|Andy"
            
            lines.append(f"- [[{link_part}]] — {desc} ({item['updated']})")
        return lines

    project_lines = format_section_lines(projects, 'projects')
    source_lines = format_section_lines(sources, 'sources')
    note_lines = format_section_lines(notes, 'notes')
    
    def replace_section(text, header, new_lines):
        pattern = re.compile(rf'({re.escape(header)}\n)(.*?)(?=\n##|\Z)', re.DOTALL)
        replacement = r'\1' + '\n'.join(new_lines) + '\n'
        return pattern.sub(replacement, text)
        
    content = replace_section(content, '## Projects', project_lines)
    content = replace_section(content, '## Sources', source_lines)
    content = replace_section(content, '## Notes', note_lines)
    
    metadata, body = parse_frontmatter(content)
    today = datetime.date.today().strftime('%Y-%m-%d')
    
    lines = content.split('\n')
    for idx, line in enumerate(lines[:10]):
        if line.strip().startswith('updated:'):
            lines[idx] = f"updated: {today}"
            break
            
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Successfully rebuilt {index_path} with {len(projects)} projects, {len(sources)} sources, and {len(notes)} notes.")

def extract_status_from_file(rel_link):
    """
    Finds the file for a given wikilink and extracts its status from the YAML frontmatter.
    """
    clean_link = rel_link.split('|')[0].strip()
    file_path = os.path.join(WIKI_DIR, f"{clean_link}.md")
    
    if not os.path.exists(file_path):
        return None
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    metadata, _ = parse_frontmatter(content)
    status = metadata.get('status')
    if status:
        return status.strip()
    return None

def update_deliverables_dashboard(tracker_path):
    """
    Updates the Deliverables Status Dashboard table in a given tracker file if present.
    """
    if not os.path.exists(tracker_path):
        return
        
    with open(tracker_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    table_started = False
    table_index_start = -1
    table_index_end = -1
    
    for i, line in enumerate(lines):
        if line.strip().startswith('##') and 'Deliverables' in line:
            table_started = True
            continue
        if table_started:
            if line.strip().startswith('|'):
                if table_index_start == -1:
                    table_index_start = i
                table_index_end = i
            elif table_index_start != -1:
                break
                
    if table_index_start == -1 or table_index_end == -1:
        return # Skip files that don't have a deliverables table
        
    table_lines = lines[table_index_start : table_index_end + 1]
    updated_table_lines = []
    
    link_re = re.compile(r'\[\[([^\]]+)\]\]')
    
    for idx, line in enumerate(table_lines):
        if idx < 2:
            updated_table_lines.append(line)
            continue
            
        columns = [c.strip() for c in line.split('|')]
        if len(columns) < 5:
            updated_table_lines.append(line)
            continue
            
        link_cell = columns[4]
        links = link_re.findall(link_cell)
        
        if links:
            new_status = None
            for l in links:
                status = extract_status_from_file(l)
                if status:
                    new_status = status
                    break
                    
            if new_status:
                columns[3] = new_status
                
        new_line = " | ".join(columns).strip()
        if not new_line.startswith('|'):
            new_line = '| ' + new_line
        if not new_line.endswith('|'):
            new_line = new_line + ' |'
            
        updated_table_lines.append(new_line)
        
    lines[table_index_start : table_index_end + 1] = updated_table_lines
    
    today = datetime.date.today().strftime('%Y-%m-%d')
    for idx, line in enumerate(lines[:10]):
        if line.strip().startswith('updated:'):
            lines[idx] = f"updated: {today}"
            break
            
    with open(tracker_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f"Successfully updated Deliverables Dashboard in {tracker_path}.")

def update_all_deliverables_dashboards():
    """
    Scans WIKI_DIR/projects/ and updates deliverables tables in all markdown files.
    """
    projects_dir = os.path.join(WIKI_DIR, 'projects')
    if not os.path.exists(projects_dir):
        return
        
    for root, _, files in os.walk(projects_dir):
        for file in files:
            if not file.endswith('.md') or file.startswith('.'):
                continue
            abs_path = os.path.join(root, file)
            update_deliverables_dashboard(abs_path)

def main():
    print("Starting Wiki Sync Operation...")
    index_path = os.path.join(WIKI_DIR, 'index.md')
    
    existing_descriptions = extract_existing_index_descriptions(index_path)
    rebuild_index(index_path, existing_descriptions)
    update_all_deliverables_dashboards()
    print("Wiki Sync Operation Completed.")

if __name__ == '__main__':
    main()
