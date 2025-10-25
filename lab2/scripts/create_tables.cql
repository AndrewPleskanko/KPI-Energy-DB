CREATE KEYSPACE IF NOT EXISTS solar_kv
            WITH replication = {'class':'SimpleStrategy', 'replication_factor':1};

USE solar_kv;

CREATE TABLE IF NOT EXISTS readings_by_station
(
    station_id uuid,
    ts         timestamp,
    power_kw   double,
    voltage    double,
    current    double,
    panel_temp double,
    region     text,
    PRIMARY KEY (station_id, ts)
) WITH CLUSTERING ORDER BY (ts DESC);

CREATE TABLE IF NOT EXISTS weather_by_station
(
    station_id      uuid,
    ts              timestamp,
    solar_radiation double,
    air_temp        double,
    cloudiness      int,
    PRIMARY KEY (station_id, ts)
) WITH CLUSTERING ORDER BY (ts DESC);

CREATE TABLE IF NOT EXISTS daily_generation_by_station
(
    station_id   uuid,
    day          date,
    energy_kwh   double,
    max_power_kw double,
    min_power_kw double,
    PRIMARY KEY (station_id, day)
);

CREATE TABLE IF NOT EXISTS analytics_by_region_date
(
    region           text,
    date             date,
    station_id       uuid,
    total_energy_kwh double,
    avg_power_kw     double,
    PRIMARY KEY ((region, date), station_id)
);