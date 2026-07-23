-- Mandi Price App — SQLite schema
-- Populate `mandi_prices` from the cleaned Agmarknet dataset.

DROP TABLE IF EXISTS user_prefs;
DROP TABLE IF EXISTS mandi_prices;

CREATE TABLE user_prefs (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    session_key  TEXT UNIQUE NOT NULL,
    language     TEXT NOT NULL CHECK (language IN ('en', 'hi', 'gu')),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE mandi_prices (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    state          TEXT NOT NULL,
    district       TEXT NOT NULL,
    market         TEXT NOT NULL,
    commodity      TEXT NOT NULL,
    variety        TEXT,
    grade          TEXT,
    arrival_date   DATE NOT NULL,
    min_price      REAL,
    max_price      REAL,
    modal_price    REAL
);

CREATE INDEX idx_prices_commodity ON mandi_prices(commodity);
CREATE INDEX idx_prices_state_market ON mandi_prices(state, market);
CREATE INDEX idx_prices_date ON mandi_prices(arrival_date);
