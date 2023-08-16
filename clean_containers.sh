for container_id in $(docker ps -a --filter "name=artists" --format "{{.ID}}"); do
    docker rm "$container_id"
done
