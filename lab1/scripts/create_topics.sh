# Main topics
docker exec -it kafka_uni kafka-topics --create --topic solar-main --bootstrap-server localhost:9092 --partitions 6 --replication-factor 1
docker exec -it kafka_uni kafka-topics --create --topic solar-batch-test --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

# Compression: one topic per algorithm for clean results
docker exec -it kafka_uni kafka-topics --create --topic solar-comp-none --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
docker exec -it kafka_uni kafka-topics --create --topic solar-comp-snappy --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
docker exec -it kafka_uni kafka-topics --create --topic solar-comp-lz4 --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
docker exec -it kafka_uni kafka-topics --create --topic solar-comp-zstd --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1

# Partitioning tests: a separate topic for each partition configuration
docker exec -it kafka_uni kafka-topics --create --topic solar-part-3  --bootstrap-server localhost:9092 --partitions 3  --replication-factor 1
docker exec -it kafka_uni kafka-topics --create --topic solar-part-6  --bootstrap-server localhost:9092 --partitions 6  --replication-factor 1
docker exec -it kafka_uni kafka-topics --create --topic solar-part-12 --bootstrap-server localhost:9092 --partitions 12 --replication-factor 1