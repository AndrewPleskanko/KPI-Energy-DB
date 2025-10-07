mkdir -p results

for algo in none snappy lz4 zstd; do
  echo "Running compression test: $algo"
  docker exec kafka_uni kafka-producer-perf-test \
    --topic solar-comp-$algo \
    --num-records 5000 \
    --record-size 256 \
    --throughput 1000 \
    --producer-props bootstrap.servers=localhost:9092 compression.type=$algo \
    > results/comp_${algo}.log
done

echo "Compression tests finished!"