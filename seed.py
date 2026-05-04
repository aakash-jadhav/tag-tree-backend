"""
Insert sample trees into PostgreSQL. Run from backend/:

  python seed.py

Requires DATABASE_URL (or default in app.config) and existing `trees` table
(create by starting the API once, or run SQLAlchemy create_all via main lifespan).
"""

from app.database import SessionLocal
from app.models import TreeRecord


SAMPLE_TREES = [
    {
        "name": "root",
        "children": [
            {
                "name": "child1",
                "children": [
                    {"name": "child1-child1", "data": "c1-c1 Hello"},
                    {"name": "child1-child2", "data": "c1-c2 JS"},
                ],
            },
            {"name": "child2", "data": "c2 World"},
        ],
    },
    {
        "name": "demo",
        "children": [
            {"name": "notes", "data": "Remember to try Export"},
            {
                "name": "nested",
                "children": [{"name": "deep-leaf", "data": "Deep value"}],
            },
        ],
    },
]


def main() -> None:
    db = SessionLocal()
    try:
        existing = db.query(TreeRecord).count()
        if existing > 0:
            print(f"Skipping seed: {existing} tree(s) already exist.")
            return
        for tree in SAMPLE_TREES:
            db.add(TreeRecord(data=tree))
        db.commit()
        print(f"Seeded {len(SAMPLE_TREES)} sample tree(s).")
    finally:
        db.close()


if __name__ == "__main__":
    main()
