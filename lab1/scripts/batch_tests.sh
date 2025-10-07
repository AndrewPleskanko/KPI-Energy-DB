mkdir -p results

for batch in 16384 65536 262144 1048576; do
  for linger in 0 10 50 100; do
    echo "Running test: batch=${batch}, linger=${linger}"
    docker exec kafka_uni kafka-producer-perf-test \
      --topic solar-batch-test \
      --num-records 10000 --record-size 256 --throughput -1 \
      --producer-props bootstrap.servers=localhost:9092 batch.size=$batch linger.ms=$linger \
      > results/batch_${batch}_${linger}.log
  done
done
