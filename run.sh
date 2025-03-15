
#!/bin/bash

# Start the web server and watch for changes in graph directory
echo "Setting up file watcher for graph directory..."
(
  while true; do
    echo "Changes detected in graph directory. Regenerating graph..."
    python graph/scripts/generate_graph.py --data_dir `pwd`/graph/data --out-dir `pwd`/graph/output
    rm -f ./web/graph.json
    ln -s `pwd`/graph/output/graph.json ./web/graph.json
    echo "Graph updated."
    inotifywait -r -e modify,create,delete,move ./graph ./web
  done
) &
WATCHER_PID=$!

# Ensure watcher is killed when script exits
trap "kill $WATCHER_PID" EXIT
echo "Starting web server..."
cd web
npm start