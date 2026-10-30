-- Expected counts after the sample import:
-- categories = 3, authors = 5, users = 2, books = 4, book_authors = 5.
SELECT 'categories' AS table_name, COUNT(*) AS rows FROM categories
UNION ALL
SELECT 'authors', COUNT(*) FROM authors
UNION ALL
SELECT 'users', COUNT(*) FROM users
UNION ALL
SELECT 'books', COUNT(*) FROM books
UNION ALL
SELECT 'book_authors', COUNT(*) FROM book_authors;

-- Relationships: each book and its authors.
SELECT b.title, c.name AS category,
       string_agg(a.full_name, ', ' ORDER BY a.full_name) AS authors
FROM books AS b
JOIN categories AS c ON c.category_id = b.category_id
JOIN book_authors AS ba ON ba.book_id = b.book_id
JOIN authors AS a ON a.author_id = ba.author_id
GROUP BY b.book_id, b.title, c.name
ORDER BY b.book_id;

-- This query should return zero rows (no broken references).
SELECT b.book_id, b.category_id
FROM books AS b
LEFT JOIN categories AS c ON c.category_id = b.category_id
WHERE c.category_id IS NULL;