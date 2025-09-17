# Generate Prerequisite Practice

Demonstrates how to generate prerequisite-based practice questions using Knowledge Graph data covering:
- **Data Loading**: Reading CSV files with educational frameworks and relationships
- **Prerequisite Analysis**: Finding standards that build towards a target standard
- **Relationship Mapping**: Connecting learning components to prerequisite standards
- **Practice Generation**: Creating structured practice questions based on prerequisite knowledge

**Features**: Common Core Math analysis, prerequisite relationship traversal, learning component mapping

Follow the step-by-step tutorial [here](https://docs.learningcommons.org/knowledge-graph/getting-started/tutorials/generating-prerequisite-practice-questions)

## Prerequisites

- Node.js (v14 or higher)
- Knowledge Graph CSV dataset files:
  - `StandardsFrameworkItem.csv`
  - `LearningComponent.csv`
  - `Relationships.csv`

## Dependencies

- **openai**: OpenAI API for generating practice questions
- **csv-parse**: CSV file parsing
- **dotenv**: Environment variable management
- **arquero**: Data manipulation

## Quick Start

1. **Clone and Install**:
   ```bash
   git clone <repository-url>
   cd tutorials/generate_prereq_practice/js
   npm install
   ```

2. **Set Environment Variables** (create `.env` file):
   ```bash
   KG_DATA_PATH=/path/to/your/knowledge-graph/csv/files
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Run Tutorial**:
   ```bash
   npm start
   ```
