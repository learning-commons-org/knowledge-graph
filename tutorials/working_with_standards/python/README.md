Demonstrates how to work with state educational standards data covering:
- **Data Loading**: Reading CSV files with standards frameworks, items, and relationships
- **Hierarchical Queries**: Traversing parent-child relationships in educational standards
- **AI Embeddings**: Generating vector embeddings for semantic search
- **Vector Search**: Performing similarity-based searches on educational standards

Follow the step-by-step tutorial [here](https://docs.learningcommons.org/knowledge-graph/getting-started/tutorials/working-with-state-standards)

## Prerequisites

- Python 3.8 or higher
- Knowledge Graph CSV dataset files:
  - `StandardsFramework.csv`
  - `StandardsFrameworkItem.csv`
  - `Relationships.csv`

## Dependencies

- **transformers**: Hugging Face transformers library for embeddings
- **pandas**: Data manipulation and analysis library
- **torch**: PyTorch for deep learning models
- **scikit-learn**: Machine learning library for cosine similarity
- **python-dotenv**: Environment variable management

## Quick Start

1. **Clone and Set Up Virtual Environment**:
   ```bash
   git clone <repository-url>
   cd tutorials/working_with_standards/python
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set Environment Variables** (create `.env` file):
   ```bash
   KG_DATA_PATH=/path/to/your/knowledge-graph/csv/files
   ```

3. **Run Tutorial**:
   ```bash
   python work_with_state_standards.py
   ```
