# Knowledge Graph Visualization

A web-based visualization tool for concept knowledge graphs.

## Setup

### Prerequisites

- Python 3.6+
- Node.js 12+
- npm

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Install dependencies:
   ```
   cd web
   npm install
   ```

### Usage

1. Generate the knowledge graph:
   ```
   python scripts/generate_graph.py
   ```

2. Start the web server:
   ```
   cd web
   npm start
   ```

3. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

## Features

- Interactive graph visualization
- Search for concepts
- Highlight related concepts
- Double-click to focus on a specific concept
- Reset view to see the entire graph

## Project Structure

- `data/`: Contains the problem data files
- `scripts/`: Python scripts for generating the knowledge graph
- `web/`: Web application for visualizing the graph
  - `index.html`: Main entry point for the web application
  - `server.js`: Simple Node.js server for serving the web application
  - `graph.json`: Generated graph data (created by the Python script)