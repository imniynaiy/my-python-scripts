import re
import sqlite3
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python monthly_summarize.py <id>")
        sys.exit(1)
    
    diary_id = int(sys.argv[1])
    
    # Open database (expand ~ to user home)
    import os
    from dotenv import load_dotenv
    load_dotenv()

    db_env = os.getenv('DB')
    db_path = os.path.expanduser(db_env)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Query using the provided SQL, use diary_id instead of 0 (parameterized)
    cursor.execute(
        "select title, original_content from post where id in (select post_id from post_category where category_id = 2) and id > ?",
        (diary_id,)
    )
    
    rows = cursor.fetchall()
    
    # Save results into a string for later use
    parts = []
    for title, content in rows:
        parts.append(f"Date: {title}")
        parts.append(f"Content: \n{content or ''}")
        parts.append("-" * 40)
    output_str = "\n".join(parts)
    print(output_str)

    # Get the id of the newest post where category_id = 2, write it back to this file
    cursor.execute(
        "select id from post where id in (select post_id from post_category where category_id = 2) order by id desc limit 1"
    )
    newest_id = cursor.fetchone()
    if newest_id:
        new_last_line = f"# Last id: {newest_id[0]}"
        with open(__file__, 'r') as f:
            content = f.read()
        content = re.sub(r'# Last id: \d+', new_last_line, content)
        with open(__file__, 'w') as f:
            f.write(content)
    
    conn.close()

if __name__ == "__main__":
    main()


# Last id: 126