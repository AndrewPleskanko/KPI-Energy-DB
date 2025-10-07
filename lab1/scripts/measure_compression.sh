mkdir -p results
echo "--- Consuming data from topics for compression analysis ---"

for algo in none snappy lz4 zstd; do
  echo "Consuming data from topic solar-comp-$algo..."

  docker exec kafka_uni kafka-console-consumer \
    --bootstrap-server localhost:9092 \
    --topic solar-comp-$algo \
    --from-beginning \
    --max-messages 5000 \
    > "results/consumed_${algo}.log"
done

echo "Data successfully saved to the results folder."