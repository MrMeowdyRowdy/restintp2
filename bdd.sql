CREATE TABLE reservations (
    reservation_id INTEGER PRIMARY KEY,
    room_number INTEGER NOT NULL,
    customer_name TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    status TEXT DEFAULT 'active'
);
