Demonstrates how to work with state educational standards data covering:
- **Data Loading**: Reading CSV files with standards frameworks, items, and relationships
- **Hierarchical Queries**: Traversing parent-child relationships in educational standards
- **AI Embeddings**: Generating vector embeddings for semantic search
- **Vector Search**: Performing similarity-based searches on educational standards

Follow the step-by-step tutorial [here](https://docs.learningcommons.org/knowledge-graph/getting-started/tutorials/working-with-state-standards)

## Prerequisites

- Node.js (v14 or higher)
- Knowledge Graph CSV dataset files:
  - `StandardsFramework.csv`
  - `StandardsFrameworkItem.csv`
  - `Relationships.csv`

## Dependencies

- **@xenova/transformers**: Local AI embeddings (no API required)
- **arquero**: Data manipulation and analysis library
- **csv-parse**: CSV file parsing
- **fast-cosine-similarity**: Vector similarity calculations
- **dotenv**: Environment variable management

## Quick Start

1. **Clone and Install**:
   ```bash
   git clone <repository-url>
   cd tutorials/working_with_standards/js
   npm install
   ```

2. **Set Environment Variables** (create `.env` file):
   ```bash
   KG_DATA_PATH=/path/to/your/knowledge-graph/csv/files
   ```

3. **Run Tutorial**:
   ```bash
   npm start
   ```
