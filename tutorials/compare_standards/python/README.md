# Compare Standards

Demonstrates how to compare educational standards across different frameworks (Common Core vs Texas)

Follow the step-by-step tutorial [here](https://docs.learningcommons.org/knowledge-graph/getting-started/tutorials/comparing-standards-across-states)

## Prerequisites

- Python 3.8 or higher
- Knowledge Graph CSV dataset files:
  - `StandardsFrameworkItem.csv`
  - `LearningComponent.csv`
  - `Relationships.csv`

## Dependencies

- **pandas**: Data manipulation and analysis library
- **python-dotenv**: Environment variable management

## Quick Start

1. **Clone and Set Up Virtual Environment**:
   ```bash
   git clone <repository-url>
   cd tutorials/compare_standards/python
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
   python compare_standards.py
   ```
