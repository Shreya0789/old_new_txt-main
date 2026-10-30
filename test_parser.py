#!/usr/bin/env python3
"""
Test script for the file parsing logic
"""

def parse_txt_file(content: str) -> list:
    """Parse txt file content to extract names and links."""
    entries = []
    lines = content.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if line and ':' in line:
            # Split by first colon to separate name and link
            parts = line.split(':', 1)
            if len(parts) == 2:
                name = parts[0].strip()
                link = parts[1].strip()
                if name and link:
                    entries.append({
                        'name': name,
                        'link': link,
                        'original_line': line
                    })
    
    return entries

def create_result_file(entries: list) -> str:
    """Create result file content from entries."""
    if not entries:
        return "No new entries found."
    
    result_lines = []
    for entry in entries:
        result_lines.append(entry['original_line'])
    
    return '\n'.join(result_lines)

# Test with sample data
if __name__ == "__main__":
    # Sample old file content
    old_content = """May Month Class Schedule.png: https://cdn-wl-assets.classplus.co/production/812410/747f13df-e31a-407f-a78e-5286f9156d3c.png
JUNE Month Class Schedule: https://cdn-wl-assets.classplus.co/production/812410/43ffde2d-5504-43c7-b4b6-a62eaade9fb5.jpeg
How to download Free Electrical PYPs: https://media-cdn.classplusapp.com/812410/cc/1da52d1cd41d43f8964ebdb6e7f07945-lr/master.m3u8"""

    # Sample new file content (with one new entry)
    new_content = """May Month Class Schedule.png: https://cdn-wl-assets.classplus.co/production/812410/747f13df-e31a-407f-a78e-5286f9156d3c.png
JUNE Month Class Schedule: https://cdn-wl-assets.classplus.co/production/812410/43ffde2d-5504-43c7-b4b6-a62eaade9fb5.jpeg
How to download Free Electrical PYPs: https://media-cdn.classplusapp.com/812410/cc/1da52d1cd41d43f8964ebdb6e7f07945-lr/master.m3u8
NEW CLASS ADDED: https://example.com/new-class-link"""

    # Parse files
    old_entries = parse_txt_file(old_content)
    new_entries = parse_txt_file(new_content)
    
    print(f"Old entries: {len(old_entries)}")
    print(f"New entries: {len(new_entries)}")
    
    # Find differences
    old_links = {entry['link'] for entry in old_entries}
    old_names = {entry['name'] for entry in old_entries}
    
    new_only_entries = []
    for entry in new_entries:
        if entry['link'] not in old_links and entry['name'] not in old_names:
            new_only_entries.append(entry)
    
    print(f"New only entries: {len(new_only_entries)}")
    
    # Create result
    result = create_result_file(new_only_entries)
    print("\nResult file content:")
    print(result)
