CREATE TABLE station_tb (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL UNIQUE,
    region VARCHAR NOT NULL,
    language VARCHAR NOT NULL,
    uri VARCHAR NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recording_tb (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL UNIQUE,
    station_id INTEGER NOT NULL,
    file_size INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    finished_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    idx INTEGER,
    CONSTRAINT fk_station FOREIGN KEY (station_id) REFERENCES station_tb(id)
);
CREATE TRIGGER IF NOT EXISTS update_station_recording_idx AFTER INSERT ON recording_tb
		BEGIN
		    UPDATE recording_tb SET idx=id WHERE id=NEW.id;
		END;

CREATE INDEX recording_tb_idx ON recording_tb(idx);
