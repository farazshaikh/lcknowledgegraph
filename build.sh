#!/bin/bash

# Generate the knowledge graph
echo "Generating knowledge graph..."
python graph/scripts/generate_graph.py --data_dir `pwd`/graph/data --out-dir `pwd`/graph/output

# update the symlink
rm -f ./web/graph.json
ln -s `pwd`/graph/output/graph.json ./web/graph.json

# Start the web server
echo "Starting web server..."
cd web
npm start