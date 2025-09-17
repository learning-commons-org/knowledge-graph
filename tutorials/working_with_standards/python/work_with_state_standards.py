#!/usr/bin/env python3
"""
================================
CONFIGURATION & SETUP
================================
"""

# Dependencies
import os
import sys
import json
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables
load_dotenv()

# Domain Constants
GENERATE_EMBEDDINGS = True
MIDDLE_SCHOOL_GRADES = ['6', '7', '8']
# For this tutorial, we use 'all-MiniLM-L6-v2' which provides good quality embeddings
# for short text. You can substitute any compatible embedding model.
EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

# Environment Setup
data_dir = os.getenv('KG_DATA_PATH')
if not data_dir:
    print('❌ KG_DATA_PATH environment variable is not set.')
    sys.exit(1)

data_path = Path(data_dir)
EMBEDDING_FILE_PATH = data_path / 'california_math_embeddings.json'

# Initialize embedding components (will be loaded on first use)
tokenizer = None
model = None


"""
================================
HELPER FUNCTIONS
================================
"""

def load_csv(filename):
    """Load and parse CSV file from data directory"""
    try:
        file_path = data_path / filename
        return pd.read_csv(file_path)
    except Exception as error:
        print(f'❌ Error loading CSV file {filename}: {str(error)}')
        raise error


def find_framework_item(case_identifier_uuid, standards_framework_items_data):
    """Find a framework item by UUID"""
    matching_items = standards_framework_items_data[
        standards_framework_items_data['caseIdentifierUUID'] == case_identifier_uuid
    ]
    if len(matching_items) > 0:
        return matching_items.iloc[0]
    return None


"""
================================
STEP 1: LOAD DATA
================================
"""

def load_data():
    """Load CSV data files needed for the tutorial"""
    standards_frameworks_data = load_csv('StandardsFramework.csv')
    standards_framework_items_data = load_csv('StandardsFrameworkItem.csv')
    
    print('✅ Files loaded from KG CSV files')
    print(f'  Standards Frameworks: {len(standards_frameworks_data)}')
    print(f'  Standards Framework Items: {len(standards_framework_items_data)}')
    
    return {'standards_frameworks_data': standards_frameworks_data, 
            'standards_framework_items_data': standards_framework_items_data}


"""
================================
STEP 2: QUERY FOR STANDARDS DATA
================================
"""

def get_math_standards_frameworks(standards_frameworks_data):
    """
    Get snapshot of mathematics standards frameworks
    
    SQL Equivalent:
        SELECT "name", "academicSubject", "jurisdiction", "identifier"
        FROM standards_framework
        WHERE "academicSubject" = 'Mathematics';
    
    Cypher Equivalent:
        MATCH (sf:StandardsFramework {academicSubject: 'Mathematics'})
        RETURN sf.name, sf.academicSubject, sf.jurisdiction, sf.identifier
    """
    math_frameworks = standards_frameworks_data[
        standards_frameworks_data['academicSubject'] == 'Mathematics'
    ][['caseIdentifierUUID', 'name', 'jurisdiction', 'academicSubject']]
    
    print(f'✅ Retrieved {len(math_frameworks)} state standard frameworks for math (dataframe):')
    print('Sample of first 5 frameworks:')
    for i, (_, framework) in enumerate(math_frameworks.head(5).iterrows()):
        print(f'  {i+1}. {framework["jurisdiction"]}: {framework["name"]}')

    # Get California math framework metadata
    # 
    # SQL: SELECT *
    # FROM standards_framework
    # WHERE "jurisdiction" = 'California'
    #   AND "academicSubject" = 'Mathematics';
    # Cypher: MATCH (sf:StandardsFramework {jurisdiction: 'California', academicSubject: 'Mathematics'}) RETURN sf
    california_framework_df = standards_frameworks_data[
        (standards_frameworks_data['jurisdiction'] == 'California') &
        (standards_frameworks_data['academicSubject'] == 'Mathematics')
    ][['caseIdentifierUUID', 'name', 'jurisdiction', 'academicSubject']]
    
    california_framework = california_framework_df.iloc[0] if len(california_framework_df) > 0 else None

    print(f'✅ Retrieved {1 if california_framework is not None else 0} California math standards framework:')
    if california_framework is not None:
        print(f'  UUID: {california_framework["caseIdentifierUUID"]}')
        print(f'  Name: {california_framework["name"]}')
        print(f'  Jurisdiction: {california_framework["jurisdiction"]}')
        print(f'  Academic Subject: {california_framework["academicSubject"]}')
    
    return {'math_frameworks': math_frameworks, 'california_framework': california_framework}


def get_middle_school_standards_groupings(standards_framework_items_data):
    """
    Filter for middle school standard groupings from California framework
    
    SQL Equivalent:
        SELECT *
        FROM standards_framework_item
        WHERE "jurisdiction" = 'California'
          AND "academicSubject" = 'Mathematics'
          AND "normalizedStatementType" = 'Standard Grouping'
          AND (
                EXISTS (SELECT 1 FROM json_array_elements_text("gradeLevel") AS elem WHERE elem = '6')
             OR EXISTS (SELECT 1 FROM json_array_elements_text("gradeLevel") AS elem WHERE elem = '7')
             OR EXISTS (SELECT 1 FROM json_array_elements_text("gradeLevel") AS elem WHERE elem = '8')
          );
    
    Cypher Equivalent:
        MATCH (sfi:StandardsFrameworkItem)
        WHERE sfi.jurisdiction = 'California'
          AND sfi.academicSubject = 'Mathematics'
          AND sfi.normalizedStatementType = 'Standard Grouping'
          AND any(g IN sfi.gradeLevel WHERE g IN ['6','7','8'])
        RETURN sfi;
    """
    def has_middle_school_grade(grade_level_str):
        try:
            if pd.isna(grade_level_str):
                return False
            grade_levels = json.loads(grade_level_str)
            return any(level in MIDDLE_SCHOOL_GRADES for level in grade_levels)
        except:
            return False

    ca_math_items = standards_framework_items_data[
        (standards_framework_items_data['jurisdiction'] == 'California') &
        (standards_framework_items_data['academicSubject'] == 'Mathematics') &
        (standards_framework_items_data['normalizedStatementType'] == 'Standard Grouping')
    ]
    
    groupings = ca_math_items[
        ca_math_items['gradeLevel'].apply(has_middle_school_grade)
    ][['caseIdentifierUUID', 'statementCode', 'description', 'normalizedStatementType', 'statementType', 'gradeLevel']]
    
    print(f'✅ Retrieved {len(groupings)} standard groupings for middle school math in California (dataframe):')
    print('Sample of first 5 standard groupings:')
    for i, (_, grouping) in enumerate(groupings.head(5).iterrows()):
        print(f'  {i+1}. {grouping["statementCode"]}: {grouping["description"][:100]}...')
    
    return groupings


def get_middle_school_standards(standards_framework_items_data):
    """
    Get all standards for California middle school mathematics
    
    SQL Equivalent:
        SELECT *
        FROM standards_framework_item
        WHERE "jurisdiction" = 'California'
          AND "academicSubject" = 'Mathematics'
          AND "normalizedStatementType" = 'Standard'
          AND (
                EXISTS (SELECT 1 FROM json_array_elements_text("gradeLevel") AS elem WHERE elem = '6')
             OR EXISTS (SELECT 1 FROM json_array_elements_text("gradeLevel") AS elem WHERE elem = '7')
             OR EXISTS (SELECT 1 FROM json_array_elements_text("gradeLevel") AS elem WHERE elem = '8')
          );
    
    Cypher Equivalent:
        MATCH (sfi:StandardsFrameworkItem)
        WHERE sfi.jurisdiction = 'California'
          AND sfi.academicSubject = 'Mathematics'
          AND sfi.normalizedStatementType = 'Standard'
          AND any(g IN sfi.gradeLevel WHERE g IN ['6','7','8'])
        RETURN sfi;
    """
    def has_middle_school_grade(grade_level_str):
        try:
            if pd.isna(grade_level_str):
                return False
            grade_levels = json.loads(grade_level_str)
            return any(level in MIDDLE_SCHOOL_GRADES for level in grade_levels)
        except:
            return False

    ca_math_items = standards_framework_items_data[
        (standards_framework_items_data['jurisdiction'] == 'California') &
        (standards_framework_items_data['academicSubject'] == 'Mathematics') &
        (standards_framework_items_data['normalizedStatementType'] == 'Standard')
    ]
    
    standards = ca_math_items[
        ca_math_items['gradeLevel'].apply(has_middle_school_grade)
    ][['caseIdentifierUUID', 'statementCode', 'description', 'normalizedStatementType', 'gradeLevel']]
    
    print(f'✅ Retrieved {len(standards)} standards for California middle school mathematics (dataframe):')
    print('Sample of first 5 standards:')
    # Show slice from 100-105 like JS version
    start_idx = min(100, len(standards))
    end_idx = min(105, len(standards))
    sample_standards = standards.iloc[start_idx:end_idx]
    
    for i, (_, standard) in enumerate(sample_standards.iterrows(), start_idx + 1):
        print(f'  {i}. {standard["statementCode"]}: {standard["description"][:100] if pd.notna(standard["description"]) else "No description"}...')
    
    return standards


def query_for_standards_data(standards_frameworks_data, standards_framework_items_data):
    """Query and organize standards data"""
    math_data = get_math_standards_frameworks(standards_frameworks_data)
    groupings = get_middle_school_standards_groupings(standards_framework_items_data)
    standards = get_middle_school_standards(standards_framework_items_data)
    
    return {
        'california_framework': math_data['california_framework'],
        'groupings': groupings,
        'standards': standards
    }


"""
================================
STEP 3: EMBED STANDARD DATA
================================
"""

def embed_standard_data(standards_framework_items_data):
    """Generate embeddings for California middle school mathematics standards"""
    
    def has_middle_school_grade(grade_level_str):
        try:
            if pd.isna(grade_level_str):
                return False
            grade_levels = json.loads(grade_level_str)
            return any(level in MIDDLE_SCHOOL_GRADES for level in grade_levels)
        except:
            return False

    # Filter for embedding standards
    ca_math_standards = standards_framework_items_data[
        (standards_framework_items_data['jurisdiction'] == 'California') &
        (standards_framework_items_data['academicSubject'] == 'Mathematics') &
        (standards_framework_items_data['normalizedStatementType'] == 'Standard') &
        (standards_framework_items_data['gradeLevel'].apply(has_middle_school_grade)) &
        (standards_framework_items_data['description'].notna())
    ]
    
    embedding_standards = ca_math_standards.to_dict('records')

    def generate_embeddings():
        """Generate and save embeddings for each standard"""
        global tokenizer, model
        
        results = []
        print(f'🔄 Generating embeddings for {len(embedding_standards)} standards...')

        # Initialize embedding model if not already done
        if tokenizer is None or model is None:
            print('📥 Loading embedding model (first time only)...')
            tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
            model = AutoModel.from_pretrained(EMBEDDING_MODEL)
            print('✅ Embedding model loaded')

        for standard in embedding_standards:
            code = standard.get('statementCode') or '(no code)'
            
            try:
                # Generate embedding
                inputs = tokenizer(standard['description'], return_tensors='pt', padding=True, truncation=True)
                with torch.no_grad():
                    outputs = model(**inputs)
                    # Mean pooling
                    embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

                results.append({
                    'caseIdentifierUUID': standard['caseIdentifierUUID'],
                    'statementCode': standard['statementCode'],
                    'embedding': embedding.tolist()
                })

                print(f'✅ {code}')
            except Exception as err:
                print(f'❌ {code}: {str(err)}')
                raise err

        # Save embeddings to file
        with open(EMBEDDING_FILE_PATH, 'w') as f:
            json.dump(results, f, indent=2)
        print(f'✅ Saved {len(results)} embeddings to {EMBEDDING_FILE_PATH}')

    return generate_embeddings


"""
================================
STEP 4: VECTOR SEARCH STANDARD DATA
================================
"""

def vector_search_standard_data(standards_framework_items_data):
    """Perform vector search using cosine similarity"""
    
    def vector_search(query, top_k=5):
        global tokenizer, model
        
        # Initialize embedding model if not already done
        if tokenizer is None or model is None:
            print('📥 Loading embedding model...')
            tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
            model = AutoModel.from_pretrained(EMBEDDING_MODEL)
            print('✅ Embedding model loaded')

        # Generate query embedding
        try:
            inputs = tokenizer(query, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                outputs = model(**inputs)
                query_embedding = outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
        except Exception as error:
            print(f'❌ Error generating embedding for query "{query}": {str(error)}')
            return

        # Load stored embeddings
        try:
            with open(EMBEDDING_FILE_PATH, 'r') as f:
                stored_embeddings = json.load(f)
        except Exception as error:
            print(f'❌ Error loading embeddings from {EMBEDDING_FILE_PATH}: {str(error)}')
            print('💡 Make sure to run the embedding generation step first (Step 3)')
            return

        # Calculate similarities and get top results
        similarities = []
        for item in stored_embeddings:
            similarity = cosine_similarity([query_embedding], [item['embedding']])[0][0]
            similarities.append({
                'caseIdentifierUUID': item['caseIdentifierUUID'],
                'score': float(similarity)
            })

        top_results = sorted(similarities, key=lambda x: x['score'], reverse=True)[:top_k]

        print(f'\nTop {top_k} results for "{query}":\n')

        # Add framework item details to results
        for i, result in enumerate(top_results):
            framework_item = find_framework_item(result['caseIdentifierUUID'], standards_framework_items_data)
            
            statement_code = framework_item['statementCode'] if framework_item is not None and pd.notna(framework_item['statementCode']) else '(no code)'
            description = framework_item['description'] if framework_item is not None and pd.notna(framework_item['description']) else '(no statement)'

            top_results[i]['statementCode'] = statement_code
            top_results[i]['description'] = description

        # Print results in readable format
        for i, result in enumerate(top_results, 1):
            print(f'  {i}. {result["statementCode"]} (Score: {result["score"]:.4f})')
            print(f'     {result["description"][:200]}...' if len(result["description"]) > 200 else f'     {result["description"]}')
            print()

    return vector_search


"""
================================
MAIN EXECUTION
================================
"""

def main():
    """Main execution function - orchestrates all tutorial steps"""
    print('\n=== WORKING WITH STATE STANDARDS TUTORIAL ===\n')
    
    print('🔄 Step 1: Loading data...')
    data = load_data()
    standards_frameworks_data = data['standards_frameworks_data']
    standards_framework_items_data = data['standards_framework_items_data']
    
    print('\n🔄 Step 2: Querying for standards data...')
    query_for_standards_data(standards_frameworks_data, standards_framework_items_data)
    
    print('\n🔄 Step 3: Embedding standard data...')
    generate_embeddings = embed_standard_data(standards_framework_items_data)
    if GENERATE_EMBEDDINGS:
        generate_embeddings()
    else:
        print('🚫 Embedding generation disabled')
    
    print('\n🔄 Step 4: Vector searching standard data...')
    vector_search = vector_search_standard_data(standards_framework_items_data)
    vector_search('linear equations')


if __name__ == '__main__':
    main()