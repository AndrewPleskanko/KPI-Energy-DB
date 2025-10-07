mkdir -p results

for parts in 3 6 12; do
  echo "--- Running test for $parts partitions ---"

 docker exec kafka_uni kafka-producer-perf-test \
    --topic solar-part-$parts \
    --num-records 10000 \
    --record-size 256 \
    --throughput -1 \
    --producer-props bootstrap.servers=localhost:9092 \
    > "results/part_${parts}.log"
done

echo "Partitioning tests finished!"