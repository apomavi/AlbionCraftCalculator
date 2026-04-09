CREATE TABLE IF NOT EXISTS items (
    item_id TEXT PRIMARY KEY,
    unique_name TEXT NOT NULL,
    localized_name TEXT,
    category TEXT,
    subcategory TEXT,
    tier TEXT,
    enchantment_level INTEGER DEFAULT 0,
    item_group TEXT,
    stack_size INTEGER,
    weight NUMERIC,
    raw_source_path TEXT,
    source_run_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS locations (
    location_id TEXT PRIMARY KEY,
    location_name TEXT NOT NULL,
    location_type TEXT,
    continent TEXT,
    region TEXT,
    raw_source_path TEXT,
    source_run_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS market_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id TEXT NOT NULL,
    location_id TEXT NOT NULL,
    quality INTEGER,
    sell_price_min INTEGER,
    sell_price_min_date TEXT,
    buy_price_max INTEGER,
    buy_price_max_date TEXT,
    ingested_at TEXT NOT NULL,
    source_run_id TEXT NOT NULL,
    raw_source_path TEXT,
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

CREATE TABLE IF NOT EXISTS market_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id TEXT NOT NULL,
    location_id TEXT NOT NULL,
    quality INTEGER,
    interval TEXT,
    price_avg INTEGER,
    price_min INTEGER,
    price_max INTEGER,
    item_count INTEGER,
    snapshot_at TEXT NOT NULL,
    source_run_id TEXT NOT NULL,
    raw_source_path TEXT,
    FOREIGN KEY (item_id) REFERENCES items(item_id),
    FOREIGN KEY (location_id) REFERENCES locations(location_id)
);

CREATE TABLE IF NOT EXISTS gold_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    price_gold INTEGER,
    price_silver INTEGER,
    snapshot_at TEXT NOT NULL,
    source_run_id TEXT NOT NULL,
    raw_source_path TEXT
);

CREATE TABLE IF NOT EXISTS rules (
    rule_id TEXT PRIMARY KEY,
    rule_type TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    scope TEXT,
    value_text TEXT,
    value_numeric NUMERIC,
    effective_from TEXT,
    effective_to TEXT,
    source_ref TEXT,
    source_run_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS city_bonuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT NOT NULL,
    bonus_category TEXT NOT NULL,
    bonus_subcategory TEXT,
    bonus_value_text TEXT,
    bonus_value_numeric NUMERIC,
    source_ref TEXT,
    source_run_id TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS user_settings (
    setting_id TEXT PRIMARY KEY,
    user_scope TEXT NOT NULL,
    setting_key TEXT NOT NULL,
    setting_value TEXT,
    value_type TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_market_prices_item_location
    ON market_prices (item_id, location_id, ingested_at);

CREATE INDEX IF NOT EXISTS idx_market_history_item_location
    ON market_history (item_id, location_id, snapshot_at);

CREATE INDEX IF NOT EXISTS idx_gold_prices_snapshot
    ON gold_prices (snapshot_at);

CREATE INDEX IF NOT EXISTS idx_rules_type_scope
    ON rules (rule_type, scope);

CREATE INDEX IF NOT EXISTS idx_city_bonuses_city_category
    ON city_bonuses (city_name, bonus_category);