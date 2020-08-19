-- =================================== Meta =====================================
-- Author: Ankit Murdia
-- Contributors:
-- Version: 0.0.1
-- Created: 2020-08-18 23:59:36
-- Updated: 2020-08-19 11:30:06
-- Description:
-- Notes:
-- To do:
-- ==============================================================================


-- ================================ Migrate up ==================================
DROP TABLE data_map;
CREATE TABLE data_map (
	id VARCHAR(36) NOT NULL PRIMARY KEY,
	source VARCHAR(30),
	file VARCHAR(200),
	space VARCHAR(10),
	time VARCHAR(10),
	problem TEXT,
	hash VARCHAR(35)
);

CREATE UNIQUE INDEX unqidx_data_map_file ON data_map(file);
CREATE INDEX idx_data_map_source ON data_map(source);

DROP TABLE tag_map;
CREATE TABLE tag_map(
	tag VARCHAR(20),
	data_id VARCHAR(36),
	FOREIGN KEY(data_id) REFERENCES data_map(id)
);

crEate UNIQUE INDEX unqidx_tag_map_tag_data ON tag_map(tag, data_id);
CREATE INDEX idx_tag_map_tag ON tag_map(tag);
-- ==============================================================================


-- =============================== Migrate down =================================

-- ==============================================================================