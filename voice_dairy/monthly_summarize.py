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
    
    conn.close()

if __name__ == "__main__":
    main()


# Last id: 35