"""Check sample row counts and display joined book information."""
from sqlalchemy import text
from db_config import get_engine

expected = {
    "categories": 3,
    "authors": 5,
    "users": 2,
    "books": 4,
    "book_authors": 5
}

query = text("""
    SELECT b.title, c.name AS category,
           string_agg(a.full_name, ', ' ORDER BY a.full_name) AS authors
    FROM books AS b
    JOIN categories AS c ON c.category_id = b.category_id
    JOIN book_authors AS ba ON ba.book_id = b.book_id
    JOIN authors AS a ON a.author_id = ba.author_id
    GROUP BY b.book_id, b.title, c.name
    ORDER BY b.book_id
""")

with get_engine().connect() as connection:
    for table, wanted in expected.items():
        found = connection.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        ).scalar_one()
        print(f"{table}: {found} rows (expected {wanted})")
        if found != wanted:
            raise AssertionError(f"Unexpected count for {table}")

    rows = connection.execute(query).mappings().all()
    if len(rows) != expected["books"]:
        raise AssertionError("Some books have no linked authors")
    
    for row in rows:
        print(f"{row['title']} | {row['category']} | {row['authors']}")

print("All sample checks passed.")