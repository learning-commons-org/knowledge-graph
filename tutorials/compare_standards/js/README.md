# Compare Standards

Demonstrates how to compare educational standards across different frameworks (Common Core vs Texas)

Follow the step-by-step tutorial [here](https://docs.learningcommons.org/knowledge-graph/getting-started/tutorials/comparing-standards-across-states)

## Prerequisites

- Node.js (v14 or higher)
- Knowledge Graph CSV dataset files:
  - `StandardsFrameworkItem.csv`
  - `LearningComponent.csv`
  - `Relationships.csv`

## Dependencies

- **arquero**: Data manipulation and analysis library
- **csv-parse**: CSV file parsing
- **dotenv**: Environment variable management

## Quick Start

1. **Clone and Install**:
   ```bash
   git clone <repository-url>
   cd tutorials/compare_standards/js
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
