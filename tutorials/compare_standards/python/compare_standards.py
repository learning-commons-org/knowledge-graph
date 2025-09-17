#!/usr/bin/env python3
"""
================================
CONFIGURATION & SETUP
================================
"""

# Dependencies
import os
import sys
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Domain Constants
TARGET_STANDARD_CODE = '6.RP.A.2'

# Environment Setup
data_dir = os.getenv('KG_DATA_PATH')
if not data_dir:
    print('❌ KG_DATA_PATH environment variable is not set.')
    sys.exit(1)

data_path = Path(data_dir)


"""
================================
HELPER FUNCTIONS
================================
"""

def load_csv(filename):
    """
    Load and parse CSV file from data directory
    
    Args:
        filename (str): Name of the CSV file to load
        
    Returns:
        pd.DataFrame: Loaded CSV data as DataFrame
    """
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
    """
    Load CSV data files and apply initial filtering for mathematics standards
    
    Purpose: Load raw CSV data and filter to only Multi-State (Common Core) and Texas 
    mathematics standards to reduce dataset size and eliminate irrelevant data early
    
    
    Returns:
        dict: Dictionary containing filtered datasets and metadata
    """
    # Load raw CSV files
    all_standards_framework_items = load_csv('StandardsFrameworkItem.csv')
    learning_components_data = load_csv('LearningComponent.csv')
    relationships_data = load_csv('Relationships.csv')

    print('✅ Data loaded from KG CSV files')
    print(f'  Standards Framework Items: {len(all_standards_framework_items)}')
    print(f'  Learning Components Data: {len(learning_components_data)}')
    print(f'  Relationships Data: {len(relationships_data)}')

    # Apply domain-specific filtering
    standards_framework_items_data = all_standards_framework_items[
        (all_standards_framework_items['academicSubject'] == 'Mathematics') &
        (all_standards_framework_items['jurisdiction'].isin(['Multi-State', 'Texas']))
    ].copy()

    # Count by jurisdiction for validation
    common_core_count = len(standards_framework_items_data[
        standards_framework_items_data['jurisdiction'] == 'Multi-State'
    ])

    texas_count = len(standards_framework_items_data[
        standards_framework_items_data['jurisdiction'] == 'Texas'
    ])

    if common_core_count == 0:
        print('❌ No Common Core mathematics standards found')
        return None

    if texas_count == 0:
        print('❌ No Texas mathematics standards found')
        return None

    print('✅ Data loaded and filtered successfully')
    print(f'  Filtered Standards Framework Items: {len(standards_framework_items_data)}')
    print(f'  Common Core Standards: {common_core_count}')
    print(f'  Texas Standards: {texas_count}')
    print(f'  Learning Components: {len(learning_components_data)}')
    print(f'  Relationships: {len(relationships_data)}')

    return {
        'standards_framework_items_data': standards_framework_items_data,
        'learning_components_data': learning_components_data,
        'relationships_data': relationships_data,
        'metadata': {
            'common_core_count': common_core_count,
            'texas_count': texas_count
        }
    }




"""
================================
STEP 2: "UNPACK" A COMMON CORE STANDARD
================================
"""

def find_target_standard(standards_framework_items_data):
    """
    Locate the specific Common Core standard to analyze
    
    Purpose: Find the target standard that will serve as the basis for comparison.
    This standard's learning components will be used to find similar Texas standards.
    
    SQL:    SELECT * 
            FROM standards_framework_item 
            WHERE "statementCode" = '6.RP.A.2' 
              AND "academicSubject" = 'Mathematics' 
              AND "jurisdiction" = 'Multi-State';
    
    Cypher: MATCH (sfi:StandardsFrameworkItem) 
            WHERE sfi.statementCode = '6.RP.A.2' AND sfi.academicSubject = 'Mathematics'
            AND sfi.jurisdiction = 'Multi-State'
            RETURN sfi;
    
    Args:
        standards_framework_items_data (pd.DataFrame): Filtered standards data
        
    Returns:
        pd.Series or None: Target standard data or None if not found
    """
    target_standard_mask = (
        (standards_framework_items_data['statementCode'] == TARGET_STANDARD_CODE) &
        (standards_framework_items_data['jurisdiction'] == 'Multi-State')
    )
    
    target_standards = standards_framework_items_data[target_standard_mask]
    
    if len(target_standards) == 0:
        print(f'❌ Target standard not found: {TARGET_STANDARD_CODE}')
        return None

    target_standard = target_standards.iloc[0]

    print(f'✅ Found target standard: {target_standard["statementCode"]}')
    print(f'  UUID: {target_standard["caseIdentifierUUID"]}')
    print(f'  Code: {target_standard["statementCode"]}') 
    print(f'  Description: {target_standard["description"]}')

    return target_standard



def extract_supporting_learning_components(target_standard, relationships_data, learning_components_data):
    """
    Find learning components that support the target standard
    
    Purpose: Extract the learning components (skills/concepts) that support the target
    standard. These components represent the underlying knowledge needed to master
    the standard and will be used to find similar Texas standards.
    
    SQL:    SELECT lc.* 
            FROM learning_component lc 
            JOIN relationships r 
              ON lc."identifier" = r."sourceEntityValue" 
            WHERE r."targetEntityValue" = '0c0bb5f6-4b99-11ec-a82f-0242ac1a0003' 
              AND r."relationshipType" = 'supports';
    
    Cypher: MATCH (lc:LearningComponent)-[:supports]->(standard)
            WHERE standard.caseIdentifierUUID = '0c0bb5f6-4b99-11ec-a82f-0242ac1a0003'
            RETURN lc
    
    Args:
        target_standard (pd.Series): The target standard data
        relationships_data (pd.DataFrame): Relationships dataset
        learning_components_data (pd.DataFrame): Learning components dataset
        
    Returns:
        pd.DataFrame: Supporting learning components data
    """
    # Find relationships where learning components support the target standard
    supporting_relationships = relationships_data[
        (relationships_data['relationshipType'] == 'supports') &
        (relationships_data['targetEntityValue'] == target_standard['caseIdentifierUUID'])
    ]
    
    # Join with learning components data (add suffixes to handle column conflicts)
    supporting_lcs = supporting_relationships.merge(
        learning_components_data,
        left_on='sourceEntityValue',
        right_on='identifier',
        how='inner',
        suffixes=('_rel', '_lc')
    )
    
    # Select and rename columns to match expected output
    supporting_lcs = supporting_lcs[['sourceEntityValue', 'description_lc']].copy()
    supporting_lcs = supporting_lcs.rename(columns={
        'sourceEntityValue': 'identifier',
        'description_lc': 'description'
    })

    print(f'✅ Found {len(supporting_lcs)} supporting learning components:')
    for i, (_, lc) in enumerate(supporting_lcs.iterrows(), 1):
        print(f'  {i}. {lc["identifier"]}: {lc["description"]}')

    return supporting_lcs


"""
================================
STEP 3: COMPARE TO TEXAS STANDARDS
================================
"""

def find_matched_texas_standards(supporting_lcs, relationships_data, standards_framework_items_data, learning_components_data):
    """
    Find Texas standards that share learning components with the target standard
    
    Purpose: Identify Texas standards that have overlapping learning components with 
    the target Common Core standard. This two-step process first finds standards with
    any overlap, then retrieves ALL learning components for those matched standards.
    
    SQL:    WITH matched_standards AS (
              SELECT DISTINCT ts."caseIdentifierUUID"
              FROM standards_framework_item ts
              JOIN relationships r
                ON ts."caseIdentifierUUID" = r."targetEntityValue"
              JOIN learning_component lc
                ON r."sourceEntityValue" = lc."identifier"
              WHERE r."relationshipType" = 'supports'
                AND ts."jurisdiction" = 'Texas'
                AND lc."identifier" IN ('db4c25ad-9892-5abb-bcba-2fc9781d10f8',
                                        'b9b94f31-b58b-5e26-9efe-680b167046ba',
                                        '523d04e7-47d8-55c7-bc44-792f3e01bfda')
            )
            SELECT
              ts."caseIdentifierUUID",
              ts."statementCode",
              ts."description",
              ARRAY_AGG(lc."description") AS lc_descriptions,
              ARRAY_AGG(lc."identifier") AS lc_identifiers
            FROM standards_framework_item ts
            JOIN relationships r
              ON ts."caseIdentifierUUID" = r."targetEntityValue"
            JOIN learning_component lc
              ON r."sourceEntityValue" = lc."identifier"
            WHERE r."relationshipType" = 'supports'
              AND ts."jurisdiction" = 'Texas'
              AND ts."caseIdentifierUUID" IN (SELECT "caseIdentifierUUID" FROM matched_standards)
            GROUP BY ts."caseIdentifierUUID", ts."statementCode", ts."description";
    
    Cypher: MATCH (ts:StandardsFrameworkItem)-[r:supports]-(lc:LearningComponent)
            WHERE ts.jurisdiction = 'Texas'
            AND lc.identifier IN ['db4c25ad-9892-5abb-bcba-2fc9781d10f8', 'b9b94f31-b58b-5e26-9efe-680b167046ba', '523d04e7-47d8-55c7-bc44-792f3e01bfda']
            WITH DISTINCT ts.caseIdentifierUUID AS matched_id
            MATCH (matched_ts:StandardsFrameworkItem)-[r2:supports]-(all_lc:LearningComponent)
            WHERE matched_ts.jurisdiction = 'Texas'
            AND matched_ts.caseIdentifierUUID = matched_id
            RETURN matched_ts.caseIdentifierUUID,
                   matched_ts.statementCode,
                   matched_ts.description,
                   COLLECT(all_lc.description) AS lc_descriptions,
                   COLLECT(all_lc.identifier) AS lc_identifiers
    
    Args:
        supporting_lcs (pd.DataFrame): Learning components from target standard
        relationships_data (pd.DataFrame): Relationships dataset
        standards_framework_items_data (pd.DataFrame): Standards dataset
        learning_components_data (pd.DataFrame): Learning components dataset
        
    Returns:
        list: List of dictionaries with matched Texas standards and their components
    """
    lc_ids = supporting_lcs['identifier'].tolist()

    # Step 1: Find Texas standards with overlapping learning components
    overlapping_relationships = relationships_data[
        (relationships_data['relationshipType'] == 'supports') &
        (relationships_data['sourceEntityValue'].isin(lc_ids))
    ]
    
    texas_standards_with_overlap = overlapping_relationships.merge(
        standards_framework_items_data[standards_framework_items_data['jurisdiction'] == 'Texas'],
        left_on='targetEntityValue',
        right_on='caseIdentifierUUID',
        how='inner'
    )
    
    matched_standard_ids = texas_standards_with_overlap['caseIdentifierUUID'].unique()

    # Step 2: Get ALL learning components for those matched standards
    all_support_relationships = relationships_data[
        (relationships_data['relationshipType'] == 'supports') &
        (relationships_data['targetEntityValue'].isin(matched_standard_ids))
    ]
    
    # Join with Texas standards (add suffixes to handle column conflicts)
    results_with_standards = all_support_relationships.merge(
        standards_framework_items_data[standards_framework_items_data['jurisdiction'] == 'Texas'],
        left_on='targetEntityValue',
        right_on='caseIdentifierUUID',
        how='inner',
        suffixes=('_rel', '_std')
    )
    
    # Join with learning components (add suffixes to handle column conflicts)
    results_with_components = results_with_standards.merge(
        learning_components_data,
        left_on='sourceEntityValue',
        right_on='identifier',
        how='inner',
        suffixes=('', '_lc')
    )

    # Group by standard to aggregate learning components
    final_results = []
    for standard_uuid in matched_standard_ids:
        standard_data = results_with_components[
            results_with_components['caseIdentifierUUID'] == standard_uuid
        ]
        
        if len(standard_data) > 0:
            first_row = standard_data.iloc[0]
            lc_descriptions = standard_data['description'].tolist()  # description is from learning_components (no _lc suffix)
            lc_identifiers = standard_data['identifier'].tolist()    # identifier is from learning_components (no _lc suffix)
            
            final_results.append({
                'caseIdentifierUUID': standard_uuid,
                'statementCode': first_row['statementCode'],
                'standardDescription': first_row['description_std'],  # description_std is from standards
                'lcDescription': lc_descriptions,
                'lcIdentifier': lc_identifiers
            })

    print(f'✅ Found {len(final_results)} Texas standards with shared learning components (lc):')
    for i, result in enumerate(final_results, 1):
        print(f'  {i}. {result["statementCode"]}: {result["standardDescription"]}')
        print(f'     Learning Components: {len(result["lcDescription"])} components')

    return final_results



def display_comparison_results(target_standard, supporting_lcs, matched_texas_standards):
    """
    Display comprehensive comparison results between standards
    
    Purpose: Present the analysis results in a structured, readable format showing
    the target standard, matched Texas standards, and overlap analysis
    
    Args:
        target_standard (pd.Series): The target Common Core standard
        supporting_lcs (pd.DataFrame): Learning components for target standard
        matched_texas_standards (list): Matched Texas standards with components
    """
    # Calculate overlap metrics for each matched standard
    supporting_lc_descriptions = supporting_lcs['description'].tolist()
    results_with_overlap = []
    
    for std in matched_texas_standards:
        overlap_count = len([lc for lc in std['lcDescription'] 
                           if lc in supporting_lc_descriptions])
        total_target_lcs = len(supporting_lc_descriptions)

        results_with_overlap.append({
            **std,
            'overlapCount': overlap_count,
            'totalTargetLCs': total_target_lcs,
            'overlapRatio': f'{overlap_count}/{total_target_lcs}'
        })

    print(f'✅ Full comparison between Common Core standard {target_standard["statementCode"]} and matched Texas standards:')
    print('📋 TARGET STANDARD:')
    print(f'  Code: {target_standard["statementCode"]}')
    print(f'  Description: {target_standard["description"]}')
    print(f'  Supporting Learning Components ({len(supporting_lcs)}):')
    for _, lc in supporting_lcs.iterrows():
        print(f'   • {lc["description"]}')
    print('')

    for i, match in enumerate(results_with_overlap):
        print(f'📋 MATCHED STANDARD #{i + 1}:')
        print(f'  Code: {match["statementCode"]}')
        print(f'  Description: {match["standardDescription"]}')
        print(f'  Supporting Learning Components ({len(match["lcDescription"])}) - Overlap: {match["overlapRatio"]}:')

        for lc in match['lcDescription']:
            is_shared = lc in supporting_lc_descriptions
            emoji = '➕' if is_shared else '➖'
            print(f'   {emoji} {lc or "(no description)"}')
        print('')

"""
================================
MAIN EXECUTION
================================
"""

def main():
    """
    Main execution function - orchestrates all tutorial steps
    """
    print('\n=== COMPARE STANDARDS TUTORIAL ===\n')
    
    print('🔄 Step 1: Loading data...')
    prepared_data = load_data()
    
    standards_framework_items_data = prepared_data['standards_framework_items_data']
    learning_components_data = prepared_data['learning_components_data']
    relationships_data = prepared_data['relationships_data']
    
    print('')
    print('')
    print('🔄 Step 2: "Unpack" a Common Core standard...')
    target_standard = find_target_standard(standards_framework_items_data)
    if target_standard is None:
        print('❌ Failed to find target standard.')
        return
    
    supporting_lcs = extract_supporting_learning_components(target_standard, relationships_data, learning_components_data)
    
    print('')
    print('')
    print('🔄 Step 3: Compare to Texas standards...')
    matched_texas_standards = find_matched_texas_standards(supporting_lcs, relationships_data, standards_framework_items_data, learning_components_data)
    
    display_comparison_results(target_standard, supporting_lcs, matched_texas_standards)


if __name__ == '__main__':
    main()