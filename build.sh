#!/bin/bash

# Generate the knowledge graph
echo "Generating knowledge graph..."
python scripts/generate_graph.py

# Start the web server
echo "Starting web server..."
cd web
npm start 