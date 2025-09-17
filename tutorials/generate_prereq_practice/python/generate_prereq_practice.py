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
from openai import OpenAI

# Load environment variables
load_dotenv()

# Domain Constants
GENERATE_PRACTICE = True
# Filter criteria for mathematics standards
JURISDICTION = 'Multi-State'
ACADEMIC_SUBJECT = 'Mathematics'
TARGET_CODE = '6.NS.B.4'
# OpenAI configuration
OPENAI_MODEL = 'gpt-4'
OPENAI_TEMPERATURE = 0.7

# Environment Setup
data_dir = os.getenv('KG_DATA_PATH')
if not data_dir:
    print('❌ KG_DATA_PATH environment variable is not set.')
    sys.exit(1)

data_path = Path(data_dir)

openai_client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)


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


"""
================================
STEP 1: LOAD DATA
================================
"""

def load_data():
    """Load CSV data files and build filtered dataset"""
    
    standards_framework_items = load_csv('StandardsFrameworkItem.csv')
    learning_components = load_csv('LearningComponent.csv')
    relationships = load_csv('Relationships.csv')

    print('✅ Files loaded from KG CSV files')
    print(f'  Standards Framework Items: {len(standards_framework_items)}')
    print(f'  Learning Components: {len(learning_components)}')
    print(f'  Relationships: {len(relationships)}')

    # Filter for relevant StandardsFrameworkItems by jurisdiction and subject
    relevant_standards = standards_framework_items[
        (standards_framework_items['jurisdiction'] == JURISDICTION) &
        (standards_framework_items['academicSubject'] == ACADEMIC_SUBJECT)
    ]

    # Get set of relevant identifiers for filtering
    relevant_standard_ids = set(relevant_standards['caseIdentifierUUID'])

    # Filter relationships for buildsTowards and supports relationships
    relevant_relationships = relationships[
        ((relationships['relationshipType'] == 'buildsTowards') &
         (relationships['sourceEntityValue'].isin(relevant_standard_ids)) &
         (relationships['targetEntityValue'].isin(relevant_standard_ids))) |
        ((relationships['relationshipType'] == 'supports') &
         (relationships['targetEntityValue'].isin(relevant_standard_ids)))
    ]

    # Get learning component IDs from supports relationships
    support_relationships = relevant_relationships[
        relevant_relationships['relationshipType'] == 'supports'
    ]
    linked_learning_component_ids = set(support_relationships['sourceEntityValue'])

    # Filter learning components by identifier
    relevant_learning_components = learning_components[
        learning_components['identifier'].isin(linked_learning_component_ids)
    ]

    print('✅ Retrieved scoped graph:')
    print(f'  Standards Framework Items: {len(relevant_standards)}')
    print(f'  Learning Components: {len(relevant_learning_components)}')
    print(f'  Relationships: {len(relevant_relationships)}')

    return {
        'relevant_standards': relevant_standards,
        'relevant_relationships': relevant_relationships,
        'relevant_learning_components': relevant_learning_components
    }


"""
================================
STEP 2: QUERY PREREQUISITE DATA
================================
"""

def get_standard_and_prerequisites(relevant_standards, relevant_relationships):
    target_standard_df = relevant_standards[
        relevant_standards['statementCode'] == TARGET_CODE
    ]

    if len(target_standard_df) == 0:
        print(f'❌ No StandardsFrameworkItem found for statementCode = "{TARGET_CODE}"')
        return None

    target_standard = target_standard_df.iloc[0]
    print(f'✅ Found StandardsFrameworkItem for "{TARGET_CODE}":')
    print(f'  UUID: {target_standard["caseIdentifierUUID"]}')
    print(f'  Statement Code: {target_standard["statementCode"]}')
    print(f'  Description: {target_standard["description"]}')

    prerequisite_links = relevant_relationships[
        (relevant_relationships['relationshipType'] == 'buildsTowards') &
        (relevant_relationships['targetEntityValue'] == target_standard['caseIdentifierUUID'])
    ]

    prerequisite_standards = prerequisite_links.merge(
        relevant_standards,
        left_on='sourceEntityValue',
        right_on='caseIdentifierUUID',
        suffixes=('_rel', '_std')
    )[['sourceEntityValue', 'statementCode', 'description_std']].rename(columns={
        'sourceEntityValue': 'caseIdentifierUUID',
        'description_std': 'standardDescription'
    })

    print(f'✅ Found {len(prerequisite_standards)} prerequisite(s) for {target_standard["statementCode"]}:')
    for i, (_, std) in enumerate(prerequisite_standards.iterrows(), 1):
        print(f'  {i}. {std["statementCode"]}: {std["standardDescription"][:100]}...')

    return {'target_standard': target_standard, 'prerequisite_standards': prerequisite_standards}


def get_learning_components_for_prerequisites(prerequisite_standards, relevant_relationships, relevant_learning_components):
    prerequisite_learning_components = prerequisite_standards.merge(
        relevant_relationships,
        left_on='caseIdentifierUUID',
        right_on='targetEntityValue',
        suffixes=('_std', '_rel')
    )
    
    prerequisite_learning_components = prerequisite_learning_components[
        prerequisite_learning_components['relationshipType'] == 'supports'
    ].merge(
        relevant_learning_components,
        left_on='sourceEntityValue',
        right_on='identifier',
        suffixes=('_rel', '_lc')
    )
    
    # Select the correct columns - after merge with suffixes, learning component description becomes description_lc
    prerequisite_learning_components = prerequisite_learning_components[
        ['caseIdentifierUUID', 'statementCode', 'standardDescription', 'description_lc']
    ].rename(columns={
        'description_lc': 'learningComponentDescription'
    })

    print(f'✅ Found {len(prerequisite_learning_components)} supporting learning components for prerequisites:')
    for i, (_, lc) in enumerate(prerequisite_learning_components.iterrows(), 1):
        print(f'  {i}. {lc["learningComponentDescription"][:100]}...')

    return prerequisite_learning_components


def query_prerequisite_data(relevant_standards, relevant_relationships, relevant_learning_components):
    """
    Analyze prerequisite relationships for the target standard
    This step identifies prerequisites and supporting learning components
    
    SQL:    WITH target AS (
              SELECT "caseIdentifierUUID"
              FROM standards_framework_item
              WHERE "statementCode" = '6.NS.B.4'
            ),
            prerequisite_standards AS (
              SELECT
                sfi."caseIdentifierUUID",
                sfi."statementCode",
                sfi."description"
              FROM standards_framework_item sfi
              JOIN relationships r
                ON sfi."caseIdentifierUUID" = r."sourceEntityValue"
              JOIN target t
                ON r."targetEntityValue" = t."caseIdentifierUUID"
              WHERE r."relationshipType" = 'buildsTowards'
            )
            SELECT
              ps."caseIdentifierUUID",
              ps."statementCode",
              ps."description",
              lc."description"
            FROM prerequisite_standards ps
            JOIN relationships r
              ON ps."caseIdentifierUUID" = r."targetEntityValue"
            JOIN learning_component lc
              ON r."sourceEntityValue" = lc."identifier"
            WHERE r."relationshipType" = 'supports';
    
    Cypher: MATCH (target:StandardsFrameworkItem {statementCode: '6.NS.B.4'})
            MATCH (prereq:StandardsFrameworkItem)-[:buildsTowards]->(target)
            MATCH (lc:LearningComponent)-[:supports]->(prereq)
            RETURN prereq.caseIdentifierUUID, prereq.statementCode, prereq.description, 
                   lc.description
    """

    standard_and_prereq_data = get_standard_and_prerequisites(relevant_standards, relevant_relationships)
    if not standard_and_prereq_data:
        return None

    target_standard = standard_and_prereq_data['target_standard']
    prerequisite_standards = standard_and_prereq_data['prerequisite_standards']
    prerequisite_learning_components = get_learning_components_for_prerequisites(prerequisite_standards, relevant_relationships, relevant_learning_components)

    return {'target_standard': target_standard, 'prerequisite_learning_components': prerequisite_learning_components}


"""
================================
STEP 3: GENERATE PRACTICE
================================
"""

def package_context_data(target_standard, prerequisite_learning_components):
    """
    Package the standards and learning components data for text generation
    This creates a structured context that can be used for generating practice questions
    """

    # Convert dataframe to context format for LLM
    all_rows = prerequisite_learning_components.to_dict('records')
    standards_map = {}

    # Group learning components by standard for context
    for row in all_rows:
        case_id = row['caseIdentifierUUID']
        if case_id not in standards_map:
            standards_map[case_id] = {
                'statementCode': row['statementCode'],
                'description': row['standardDescription'] or '(no statement)',
                'supportingLearningComponents': []
            }

        standards_map[case_id]['supportingLearningComponents'].append({
            'description': row['learningComponentDescription'] or '(no description)'
        })

    full_standards_context = {
        'targetStandard': {
            'statementCode': target_standard['statementCode'],
            'description': target_standard['description'] or '(no statement)'
        },
        'prereqStandards': list(standards_map.values())
    }

    print('✅ Packaged full standards context for text generation')
    print(json.dumps(full_standards_context, indent=2))
    return full_standards_context


def generate_practice_data(full_standards_context):
    """Generate practice questions using OpenAI API
    This creates educational content based on prerequisite data
    """
    def generate_practice():
        print(f'🔄 Generating practice questions for {full_standards_context["targetStandard"]["statementCode"]}...')

        try:
            # Build prompt inline
            prerequisite_text = ''
            for prereq in full_standards_context['prereqStandards']:
                prerequisite_text += f'- {prereq["statementCode"]}: {prereq["description"]}\n'
                prerequisite_text += '  Supporting Learning Components:\n'
                for lc in prereq['supportingLearningComponents']:
                    prerequisite_text += f'    • {lc["description"]}\n'

            prompt = f"""You are a math tutor helping middle school students. Based on the following information, generate 3 practice questions for the target standard. Questions should help reinforce the key concept and build on prerequisite knowledge.

Target Standard:
- {full_standards_context["targetStandard"]["statementCode"]}: {full_standards_context["targetStandard"]["description"]}

Prerequisite Standards & Supporting Learning Components:
{prerequisite_text}"""

            response = openai_client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {'role': 'system', 'content': 'You are an expert middle school math tutor.'},
                    {'role': 'user', 'content': prompt}
                ],
                temperature=OPENAI_TEMPERATURE
            )

            practice_questions = response.choices[0].message.content.strip()

            print('✅ Generated practice questions:\n')
            print(practice_questions)

            return {
                'aiGenerated': practice_questions,
                'targetStandard': full_standards_context['targetStandard']['statementCode'],
                'prerequisiteCount': len(full_standards_context['prereqStandards'])
            }
        except Exception as err:
            print(f'❌ Error generating practice questions: {str(err)}')
            raise err

    return generate_practice


"""
================================
MAIN EXECUTION
================================
"""

def main():
    """Main execution function - orchestrates all tutorial steps"""
    print('\n=== GENERATE PREREQUISITE PRACTICE TUTORIAL ===\n')

    print('🔄 Step 1: Loading data...')
    data = load_data()
    relevant_standards = data['relevant_standards']
    relevant_relationships = data['relevant_relationships']
    relevant_learning_components = data['relevant_learning_components']

    print('\n🔄 Step 2: Querying prerequisite data...')
    prerequisite_data = query_prerequisite_data(relevant_standards, relevant_relationships, relevant_learning_components)

    if not prerequisite_data:
        print('❌ Failed to find prerequisite data')
        return

    target_standard = prerequisite_data['target_standard']
    prerequisite_learning_components = prerequisite_data['prerequisite_learning_components']

    print('\n🔄 Step 3: Generating practice...')
    full_standards_context = package_context_data(target_standard, prerequisite_learning_components)
    generate_practice = generate_practice_data(full_standards_context)
    if GENERATE_PRACTICE:
        generate_practice()
    else:
        print('🚫 Practice question generation disabled')


if __name__ == '__main__':
    main()