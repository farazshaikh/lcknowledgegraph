#!/bin/bash
set -e

# Parse command line arguments
BUILD_ONLY=false

for arg in "$@"; do
  case $arg in
  --buildonly)
    BUILD_ONLY=true
    shift
    ;;
  esac
done

# Function to build the graph and link the output
build_and_link_graph() {
  echo "Building graph..."
  python graph/scripts/generate_graph.py --data_dir $(pwd)/graph/data --out-dir $(pwd)/graph/output
  echo "Linking graph.json to web directory..."
  rm -f ./web/graph.json
  # gh-pages doens't like symlinks so just copy over the file for now
  cp $(pwd)/graph/output/graph.json ./web/graph.json
  echo "Graph built and deployed successfully."
}

# Initial build

if [ "$BUILD_ONLY" = true ]; then
  build_and_link_graph
  echo "Build only mode. Exiting."
  exit 0
fi

# Start the web server and watch for changes in graph directory
echo "Setting up file watcher for graph directory..."
(
  while true; do
    build_and_link_graph
    inotifywait -r -e modify,create,delete,move ./graph ./web
  done
) &
WATCHER_PID=$!

# Ensure watcher is killed when script exits
trap "kill $WATCHER_PID" EXIT
echo "Starting web server..."
cd web
npm start
