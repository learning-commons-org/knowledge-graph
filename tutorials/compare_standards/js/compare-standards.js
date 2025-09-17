/* ================================
   CONFIGURATION & SETUP
   ================================ */

// Dependencies
const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse/sync');
require('dotenv').config();

// Constants
const TARGET_STANDARD_CODE = '6.RP.A.2';

// Environment setup
const dataDir = process.env.KG_DATA_PATH;
if (!dataDir) {
  console.error('❌ KG_DATA_PATH environment variable is not set.');
  process.exit(1);
}


/* ================================
   HELPER FUNCTIONS
   ================================ */

function loadCSV(filename) {
  try {
    const content = fs.readFileSync(path.join(dataDir, filename), 'utf8');
    return parse(content, { columns: true, skip_empty_lines: true });
  } catch (error) {
    console.error(`❌ Error loading CSV file ${filename}: ${error.message}`);
    throw error;
  }
}

function loadData(aq) {
  /* 
   * Find Common Core and Texas standards
   * 
   * SQL:    
   * SELECT * 
   * FROM standards_framework_item 
   * WHERE "jurisdiction" = 'Multi-State' 
   *   AND "academicSubject" = 'Mathematics';
   * 
   * SELECT * 
   * FROM standards_framework_item 
   * WHERE "jurisdiction" = 'Texas' 
   *   AND "academicSubject" = 'Mathematics';
   * 
   * Cypher: 
   * MATCH (sfi:StandardsFrameworkItem) 
   * WHERE sfi.jurisdiction = 'Multi-State' AND sfi.academicSubject = 'Mathematics'
   * RETURN sfi;
   * 
   * MATCH (sfi:StandardsFrameworkItem) 
   * WHERE sfi.jurisdiction = 'Texas' AND sfi.academicSubject = 'Mathematics'
   * RETURN sfi;
   */

  /* Load and filter CSV data files for standards comparison 
   * and filter for Multi-State (Common Core) and Texas math standards
   */
  const allStandardsFrameworkItems = aq.from(loadCSV('StandardsFrameworkItem.csv'));
  const learningComponentsData = aq.from(loadCSV('LearningComponent.csv'));
  const relationshipsData = aq.from(loadCSV('Relationships.csv'));

  console.log('✅ Raw data loaded from KG CSV files');
  console.log({
    allStandardsFrameworkItems: allStandardsFrameworkItems.numRows(),
    learningComponentsData: learningComponentsData.numRows(),
    relationshipsData: relationshipsData.numRows()
  });

  // Filter standards for Multi-State (Common Core) and Texas Mathematics
  const standardsFrameworkItemsData = allStandardsFrameworkItems
    .filter(d => 
      d.academicSubject === 'Mathematics' &&
      (d.jurisdiction === 'Multi-State' || d.jurisdiction === 'Texas')
    );

  const ccCount = standardsFrameworkItemsData
    .filter(d => d.jurisdiction === 'Multi-State')
    .numRows();

  const txCount = standardsFrameworkItemsData
    .filter(d => d.jurisdiction === 'Texas')
    .numRows();

  console.log('✅ Data filtered for Multi-State and Texas Mathematics standards');
  console.log({
    filteredStandardsFrameworkItems: standardsFrameworkItemsData.numRows(),
    "Common Core (Multi-State)": ccCount,
    "Texas": txCount,
    learningComponentsData: learningComponentsData.numRows(),
    relationshipsData: relationshipsData.numRows()
  });

  if (ccCount === 0) {
    console.error('❌ No Common Core mathematics standards found');
    return null;
  }

  if (txCount === 0) {
    console.error('❌ No Texas mathematics standards found');
    return null;
  }

  return { standardsFrameworkItemsData, learningComponentsData, relationshipsData };
}

function findTargetStandard(standardsFrameworkItemsData) {
  /* Find the specific Common Core standard to analyze
   * 
   * SQL:    SELECT * 
   *         FROM standards_framework_item 
   *         WHERE "statementCode" = '6.RP.A.2' 
   *           AND "academicSubject" = 'Mathematics' 
   *           AND "jurisdiction" = 'Multi-State';
   * 
   * Cypher: MATCH (sfi:StandardsFrameworkItem) 
   *         WHERE sfi.statementCode = '6.RP.A.2' AND sfi.academicSubject = 'Mathematics'
   *         AND sfi.jurisdiction = 'Multi-State'
   *         RETURN sfi;
   */
  const targetStandardTable = standardsFrameworkItemsData
    .params({ targetCode: TARGET_STANDARD_CODE })
    .filter(d => d.statementCode === targetCode &&
      d.jurisdiction === 'Multi-State');

  const targetStandard = targetStandardTable.object();

  if (!targetStandard || !targetStandard.statementCode) {
    console.log(`❌ Standard not found: ${TARGET_STANDARD_CODE}`);
    return null;
  }

  console.log(`✅ Found target standard: ${targetStandard.statementCode}`);
  console.log(targetStandardTable.select('caseIdentifierUUID', 'statementCode', 'description').objects());

  return targetStandard;
}

function findSupportingLearningComponents(targetStandard, relationshipsData, learningComponentsData) {
  /* Find learning components that support the target standard
   * 
   * SQL:    SELECT lc.* 
   *         FROM learning_component lc 
   *         JOIN relationships r 
   *           ON lc."identifier" = r."sourceEntityValue" 
   *         WHERE r."targetEntityValue" = '0c0bb5f6-4b99-11ec-a82f-0242ac1a0003' 
   *           AND r."relationshipType" = 'supports';
   * 
   * Cypher: MATCH (lc:LearningComponent)-[:supports]->(standard)
   *         WHERE standard.caseIdentifierUUID = '0c0bb5f6-4b99-11ec-a82f-0242ac1a0003'
   *         RETURN lc
   */
  const supportingLCs = relationshipsData
    .params({ targetId: targetStandard.caseIdentifierUUID })
    .filter(d => d.relationshipType === 'supports' && d.targetEntityValue === targetId)
    .join(learningComponentsData, ['sourceEntityValue', 'identifier'])
    .select('sourceEntityValue', 'description_2')
    .rename({ sourceEntityValue: 'identifier', description_2: 'description' });

  console.log(`✅ Found ${supportingLCs.numRows()} supporting learning components:`);
  console.log(supportingLCs.objects());

  return supportingLCs;
}

function findMatchedTexasStandards(aq, supportingLCs, relationshipsData, standardsFrameworkItemsData, learningComponentsData) {
  /* Find Texas standards with their learning components - two-step process:
   * 1) Find standards that have overlapping learning components
   * 2) Get ALL learning components for those matched standards
   * 
   * SQL:    WITH matched_standards AS (
   *           SELECT DISTINCT ts."caseIdentifierUUID"
   *           FROM standards_framework_item ts
   *           JOIN relationships r
   *             ON ts."caseIdentifierUUID" = r."targetEntityValue"
   *           JOIN learning_component lc
   *             ON r."sourceEntityValue" = lc."identifier"
   *           WHERE r."relationshipType" = 'supports'
   *             AND ts."jurisdiction" = 'Texas'
   *             AND lc."identifier" IN ('db4c25ad-9892-5abb-bcba-2fc9781d10f8',
   *                                     'b9b94f31-b58b-5e26-9efe-680b167046ba',
   *                                     '523d04e7-47d8-55c7-bc44-792f3e01bfda')
   *         )
   *         SELECT
   *           ts."caseIdentifierUUID",
   *           ts."statementCode",
   *           ts."description",
   *           ARRAY_AGG(lc."description") AS lc_descriptions,
   *           ARRAY_AGG(lc."identifier") AS lc_identifiers
   *         FROM standards_framework_item ts
   *         JOIN relationships r
   *           ON ts."caseIdentifierUUID" = r."targetEntityValue"
   *         JOIN learning_component lc
   *           ON r."sourceEntityValue" = lc."identifier"
   *         WHERE r."relationshipType" = 'supports'
   *           AND ts."jurisdiction" = 'Texas'
   *           AND ts."caseIdentifierUUID" IN (SELECT "caseIdentifierUUID" FROM matched_standards)
   *         GROUP BY ts."caseIdentifierUUID", ts."statementCode", ts."description";
   * 
   * Cypher: MATCH (ts:StandardsFrameworkItem)-[r:supports]-(lc:LearningComponent)
   *         WHERE ts.jurisdiction = 'Texas'
   *         AND lc.identifier IN ['db4c25ad-9892-5abb-bcba-2fc9781d10f8', 'b9b94f31-b58b-5e26-9efe-680b167046ba', '523d04e7-47d8-55c7-bc44-792f3e01bfda']
   *         WITH DISTINCT ts.caseIdentifierUUID AS matched_id
   *         MATCH (matched_ts:StandardsFrameworkItem)-[r2:supports]-(all_lc:LearningComponent)
   *         WHERE matched_ts.jurisdiction = 'Texas'
   *         AND matched_ts.caseIdentifierUUID = matched_id
   *         RETURN matched_ts.caseIdentifierUUID,
   *                matched_ts.statementCode,
   *                matched_ts.description,
   *                COLLECT(all_lc.description) AS lc_descriptions,
   *                COLLECT(all_lc.identifier) AS lc_identifiers
   */
  const lcIds = supportingLCs.array('identifier');

  // First, find which Texas standards have overlapping learning components
  const matchedStandardIds = relationshipsData
    .filter(d => d.relationshipType === 'supports')
    .filter(aq.escape(d => lcIds.includes(d.sourceEntityValue)))
    .join(standardsFrameworkItemsData, ['targetEntityValue', 'caseIdentifierUUID'])
    .filter(d => d.jurisdiction === 'Texas')
    .select('targetEntityValue')
    .dedupe('targetEntityValue')
    .array('targetEntityValue');

  // Then get ALL learning components for those matched standards
  const results = relationshipsData
    .filter(d => d.relationshipType === 'supports')
    .filter(aq.escape(d => matchedStandardIds.includes(d.targetEntityValue)))
    .join(standardsFrameworkItemsData, ['targetEntityValue', 'caseIdentifierUUID'])
    .filter(d => d.jurisdiction === 'Texas')
    .join(learningComponentsData, ['sourceEntityValue', 'identifier']);

  // Organize learning component descriptions and identifiers for each matched standard
  const finalResults = results
    .select('targetEntityKey', 'targetEntityValue', 'statementCode', 'description_2', 'identifier', 'description')
    .rename({
      targetEntityValue: 'caseIdentifierUUID',
      description_2: 'standardDescription',
      identifier: 'lc_identifier',
      description: 'lc_description'
    })
    .groupby('caseIdentifierUUID', 'statementCode', 'standardDescription')
    .rollup({
      lcDescription: d => aq.op.array_agg(d.lc_description),
      lcIdentifier: d => aq.op.array_agg(d.lc_identifier)
    })
    .objects();

  console.log(`✅ Found ${finalResults.length} Texas standards with shared learning components (lc):`);
  console.log(finalResults);

  return finalResults;
}


function displayComparisonResults(targetStandard, supportingLCs, matchedTexasStandards) {
  // Display the full comparison results between the target Common Core standard
  // and the matched Texas standards, including supporting learning components.

  // Calculate overlap with the target standard
  const supportingLCDescriptions = supportingLCs.array('description');
  const resultsWithOverlap = matchedTexasStandards.map(std => {
    const overlapCount = std.lcDescription.filter(lc =>
      supportingLCDescriptions.includes(lc)
    ).length;
    const totalTargetLCs = supportingLCDescriptions.length;

    return {
      ...std,
      overlapCount,
      totalTargetLCs,
      overlapRatio: `${overlapCount}/${totalTargetLCs}`
    };
  });

  console.log(`✅ Full comparison between Common Core standard ${targetStandard.statementCode} and matched Texas standards:`);
  console.log(`📋 TARGET STANDARD:`);
  console.log(`  Code: ${targetStandard.statementCode}`);
  console.log(`  Description: ${targetStandard.description}`);
  console.log(`  Supporting Learning Components (${supportingLCs.numRows()}):`);
  supportingLCs.objects().forEach((lc, i) => {
    console.log(`   • ${lc.description}`);
  });
  console.log('');

  resultsWithOverlap.forEach((match, i) => {
    console.log(`📋 MATCHED STANDARD #${i + 1}:`);
    console.log(`  Code: ${match.statementCode}`);
    console.log(`  Description: ${match.standardDescription}`);
    console.log(`  Supporting Learning Components (${match.lcDescription.length}) - Overlap: ${match.overlapRatio}:`);

    const supportingLCDescriptions = supportingLCs.array('description');
    match.lcDescription.forEach((lc, j) => {
      const isShared = supportingLCDescriptions.includes(lc);
      const emoji = isShared ? '➕' : '➖';
      console.log(`   ${emoji} ${lc || '(no description)'}`);
    });
    console.log('');
  });
}

async function main() {
  const aq = await import('arquero');

  console.log('\n=== COMPARE STANDARDS TUTORIAL ===\n');

  console.log('🔄 Step 1: Loading data...');
  const { standardsFrameworkItemsData, learningComponentsData, relationshipsData } = loadData(aq);

  if (!standardsFrameworkItemsData) {
    console.log('❌ Failed to load and validate data.');
    return;
  }

  console.log('');
  console.log('');
  console.log('🔄 Step 2: "Unpack" a Common Core standard...');
  const targetStandard = findTargetStandard(standardsFrameworkItemsData);
  if (!targetStandard) {
    console.log('❌ Failed to find target standard.');
    return;
  }

  const supportingLCs = findSupportingLearningComponents(targetStandard, relationshipsData, learningComponentsData);

  console.log('');
  console.log('');
  console.log('🔄 Step 3: Compare to Texas standards...');
  const matchedTexasStandards = findMatchedTexasStandards(aq, supportingLCs, relationshipsData, standardsFrameworkItemsData, learningComponentsData);

  displayComparisonResults(targetStandard, supportingLCs, matchedTexasStandards);
}

main().catch(console.error);