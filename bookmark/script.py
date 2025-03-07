import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime

# Fix the HTML file
# Read the HTML file
# Set the file name as a variable
file_name = './bookmark/bookmarks_2025_03_06.html'

with open(file_name, 'r') as file:
    html_content = file.read()

# Remove all <p> tags using string replacement
html_content = html_content.replace('<p>', '').replace('</p>', '')
html_content = html_content.replace('</H3>', '</H3></DT>').replace('</A>', '</A></DT>')

# Save the modified HTML back to the file with "_fixed" suffix
fixed_file_name = file_name.replace('.html', '_fixed.html')
with open(fixed_file_name, 'w') as file:
    file.write(html_content)

# Read the modified HTML file
with open(fixed_file_name, 'r') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Connect to SQLite database (or create it if it doesn't exist)
# Generate a timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

# Create the database name with the timestamp
db_name = f'/Users/kokugo/Desktop/scripts/bookmark/bookmarks_{timestamp}.db'

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_name)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS folders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    parent_id INTEGER,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_archived BOOLEAN,
    is_personal BOOLEAN,
    FOREIGN KEY (parent_id) REFERENCES folders (id)
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    parent_id INTEGER,
    href TEXT,
    icon TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    is_archived BOOLEAN,
    is_personal BOOLEAN,
    FOREIGN KEY (parent_id) REFERENCES folders (id)
)
''')

root = soup.find('dl').find('dl')

# Create a stack to save parents info of tags
parent_stack = []

# Depth-first traversal of the HTML tree and print each tag
def depth_first_traverse(node):
    children = node.contents
    print("children length:", len(children))
    for child in children:
        if child.name == 'dt':
            if child.h3:
                title = child.h3.text
                updated_at = datetime.fromtimestamp(int(child.h3['last_modified']))
                created_at = datetime.fromtimestamp(int(child.h3['add_date']))
                parent_id = parent_stack[-1][1] if parent_stack else None
                is_archived = False  # Assuming default value
                is_personal = False  # Assuming default value
                print("folders:", title, parent_id)
                cursor.execute('''
                    INSERT INTO folders (title, parent_id, created_at, updated_at, is_archived, is_personal)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (title, parent_id, created_at, updated_at, is_archived, is_personal))
                conn.commit()
                folder_id = cursor.lastrowid
                parent_stack.append((title, folder_id))
            elif child.a:
                title = child.a.text
                href = child.a['href']
                icon = child.a.get('icon', None)
                created_at = datetime.fromtimestamp(int(child.a['add_date']))
                parent_id = parent_stack[-1][1] if parent_stack else None
                print("links:", title, parent_id)
                cursor.execute('''
                    INSERT INTO links (title, parent_id, href, icon, created_at, updated_at, is_archived, is_personal)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (title, parent_id, href, icon, created_at, created_at, False, False))
                conn.commit()
        elif child.name == 'dl':
            depth_first_traverse(child)
    print("pop stack")
    if len(parent_stack):
        parent_stack.pop()

depth_first_traverse(root)