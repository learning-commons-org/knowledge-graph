/* ================================
   CONFIGURATION & SETUP
   ================================ */

// Dependencies
const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse/sync');
const OpenAI = require('openai');
require('dotenv').config();

// Constants
const GENERATE_PRACTICE = true;
// Filter criteria for mathematics standards
const JURISDICTION = 'Multi-State';
const ACADEMIC_SUBJECT = 'Mathematics';
const TARGET_CODE = '6.NS.B.4';
// OpenAI configuration
const OPENAI_MODEL = 'gpt-4';
const OPENAI_TEMPERATURE = 0.7;

// Environment setup
const dataDir = process.env.KG_DATA_PATH;
if (!dataDir) {
  console.error('❌ KG_DATA_PATH environment variable is not set.');
  process.exit(1);
}

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

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


/* ================================
   STEP 1: LOAD DATA
   ================================ */
function loadData(aq) {
  /* Load CSV data files and build filtered dataset
   */

  const standardsFrameworkItems = aq.from(loadCSV('StandardsFrameworkItem.csv'));
  const learningComponents = aq.from(loadCSV('LearningComponent.csv'));
  const relationships = aq.from(loadCSV('Relationships.csv'));

  console.log('✅ Files loaded from KG CSV files');
  console.log({
    standardsFrameworkItems: standardsFrameworkItems.numRows(),
    learningComponents: learningComponents.numRows(),
    relationships: relationships.numRows()
  });

  // Filter for relevant StandardsFrameworkItems by jurisdiction and subject
  const relevantStandards = standardsFrameworkItems
    .params({ jurisdiction: JURISDICTION, academicSubject: ACADEMIC_SUBJECT })
    .filter(d => d.jurisdiction === jurisdiction && d.academicSubject === academicSubject);

  // Get array of relevant identifiers for filtering
  const relevantStandardIds = relevantStandards.array('caseIdentifierUUID');
  const relevantStandardSet = new Set(relevantStandardIds);

  // Filter relationships for buildsTowards and supports relationships
  const relevantRelationships = relationships
    .filter(aq.escape(d =>
      (d.relationshipType === 'buildsTowards' &&
        relevantStandardSet.has(d.sourceEntityValue) &&
        relevantStandardSet.has(d.targetEntityValue)) ||
      (d.relationshipType === 'supports' &&
        relevantStandardSet.has(d.targetEntityValue))
    ));

  // Get learning component IDs from supports relationships
  const supportRelationships = relevantRelationships
    .filter(d => d.relationshipType === 'supports');
  const linkedLearningComponentIds = supportRelationships.array('sourceEntityValue');
  const linkedLearningComponentSet = new Set(linkedLearningComponentIds);

  // Filter learning components by identifier
  const relevantLearningComponents = learningComponents
    .filter(aq.escape(d => linkedLearningComponentSet.has(d.identifier)));

  console.log('✅ Retrieved scoped graph:');
  console.log({
    standardsFrameworkItems: relevantStandards.numRows(),
    learningComponents: relevantLearningComponents.numRows(),
    relationships: relevantRelationships.numRows()
  });

  return {
    relevantStandards,
    relevantRelationships,
    relevantLearningComponents
  };
}

/* ================================
   STEP 2: QUERY PREREQUISITE DATA
   ================================ */
function getStandardAndPrerequisites(relevantStandards, relevantRelationships) {
  const targetStandardTable = relevantStandards
    .params({ targetCode: TARGET_CODE })
    .filter(d => d.statementCode === targetCode);

  if (targetStandardTable.numRows() === 0) {
    console.error(`❌ No StandardsFrameworkItem found for statementCode = "${TARGET_CODE}"`);
    return null;
  }

  const targetStandard = targetStandardTable.object();
  console.log(`✅ Found StandardsFrameworkItem for ${TARGET_CODE}:`)
  console.log({
    caseIdentifierUUID: targetStandard.caseIdentifierUUID,
    statementCode: targetStandard.statementCode,
    description: targetStandard.description
  });

  const prerequisiteLinks = relevantRelationships
    .params({ targetIdentifier: targetStandard.caseIdentifierUUID })
    .filter(d => d.relationshipType === 'buildsTowards' &&
      d.targetEntityValue === targetIdentifier);

  const prerequisiteStandards = prerequisiteLinks
    .join(relevantStandards, ['sourceEntityValue', 'caseIdentifierUUID'])
    .select('sourceEntityValue', 'statementCode', 'description_2')
    .rename({ sourceEntityValue: 'caseIdentifierUUID', description_2: 'standardDescription' });

  console.log(`✅ Found ${prerequisiteStandards.numRows()} prerequisite(s) for ${targetStandard.statementCode}:`);
  console.log(prerequisiteStandards.objects());

  return { targetStandard, prerequisiteStandards };
}

function getLearningComponentsForPrerequisites(prerequisiteStandards, relevantRelationships, relevantLearningComponents) {
  const prerequisiteLearningComponents = prerequisiteStandards
    .join(relevantRelationships, ['caseIdentifierUUID', 'targetEntityValue'])
    .params({ supportsType: 'supports' })
    .filter(d => d.relationshipType === supportsType)
    .join(relevantLearningComponents, ['sourceEntityValue', 'identifier'])
    .select('caseIdentifierUUID', 'statementCode', 'standardDescription', 'description_2')
    .rename({ description_2: 'learningComponentDescription' });

  console.log(`✅ Found ${prerequisiteLearningComponents.numRows()} supporting learning components for prerequisites:`);
  console.log(prerequisiteLearningComponents.objects());

  return prerequisiteLearningComponents;
}

function queryPrerequisiteData(aq, relevantStandards, relevantRelationships, relevantLearningComponents) {
  /* Analyze prerequisite relationships for the target standard
   * This step identifies prerequisites and supporting learning components
   * 
   * SQL:    WITH target AS (
   *           SELECT "caseIdentifierUUID"
   *           FROM standards_framework_item
   *           WHERE "statementCode" = '6.NS.B.4'
   *         ),
   *         prerequisite_standards AS (
   *           SELECT
   *             sfi."caseIdentifierUUID",
   *             sfi."statementCode",
   *             sfi."description"
   *           FROM standards_framework_item sfi
   *           JOIN relationships r
   *             ON sfi."caseIdentifierUUID" = r."sourceEntityValue"
   *           JOIN target t
   *             ON r."targetEntityValue" = t."caseIdentifierUUID"
   *           WHERE r."relationshipType" = 'buildsTowards'
   *         )
   *         SELECT
   *           ps."caseIdentifierUUID",
   *           ps."statementCode",
   *           ps."description",
   *           lc."description"
   *         FROM prerequisite_standards ps
   *         JOIN relationships r
   *           ON ps."caseIdentifierUUID" = r."targetEntityValue"
   *         JOIN learning_component lc
   *           ON r."sourceEntityValue" = lc."identifier"
   *         WHERE r."relationshipType" = 'supports';
   * 
   * Cypher: MATCH (target:StandardsFrameworkItem {statementCode: '6.NS.B.4'})
   *         MATCH (prereq:StandardsFrameworkItem)-[:buildsTowards]->(target)
   *         MATCH (lc:LearningComponent)-[:supports]->(prereq)
   *         RETURN prereq.caseIdentifierUUID, prereq.statementCode, prereq.description, 
   *                lc.description
   */

  const standardAndPrereqData = getStandardAndPrerequisites(relevantStandards, relevantRelationships);
  if (!standardAndPrereqData) {
    return null;
  }

  const { targetStandard, prerequisiteStandards } = standardAndPrereqData;
  const prerequisiteLearningComponents = getLearningComponentsForPrerequisites(prerequisiteStandards, relevantRelationships, relevantLearningComponents);

  return { targetStandard, prerequisiteLearningComponents };
}

/* ================================
   STEP 3: GENERATE PRACTICE
   ================================ */
function packageContextData(targetStandard, prerequisiteLearningComponents) {
  /* Package the standards and learning components data for text generation
   * This creates a structured context that can be used for generating practice questions
   */

  // Convert dataframe to context format for LLM
  const allRows = prerequisiteLearningComponents.objects();
  const standardsMap = new Map();

  // Group learning components by standard for context
  for (const row of allRows) {
    if (!standardsMap.has(row.caseIdentifierUUID)) {
      standardsMap.set(row.caseIdentifierUUID, {
        statementCode: row.statementCode,
        description: row.standardDescription || '(no statement)',
        supportingLearningComponents: []
      });
    }

    standardsMap.get(row.caseIdentifierUUID).supportingLearningComponents.push({
      description: row.learningComponentDescription || '(no description)'
    });
  }

  const fullStandardsContext = {
    targetStandard: {
      statementCode: targetStandard.statementCode,
      description: targetStandard.description || '(no statement)'
    },
    prereqStandards: Array.from(standardsMap.values())
  };

  console.log(`✅ Packaged full standards context for text generation`);
  console.log(JSON.stringify(fullStandardsContext, null, 2));
  return fullStandardsContext;
}

function generatePracticeData(fullStandardsContext) {
  /* Generate practice questions using OpenAI API
   * This creates educational content based on prerequisite data
   */
  return async function generatePractice() {
    console.log(`🔄 Generating practice questions for ${fullStandardsContext.targetStandard.statementCode}...`);

    try {
      // Build prompt inline
      let prerequisiteText = '';
      for (const prereq of fullStandardsContext.prereqStandards) {
        prerequisiteText += `- ${prereq.statementCode}: ${prereq.description}\n`;
        prerequisiteText += '  Supporting Learning Components:\n';
        for (const lc of prereq.supportingLearningComponents) {
          prerequisiteText += `    • ${lc.description}\n`;
        }
      }

      const prompt = `You are a math tutor helping middle school students. Based on the following information, generate 3 practice questions for the target standard. Questions should help reinforce the key concept and build on prerequisite knowledge.

Target Standard:
- ${fullStandardsContext.targetStandard.statementCode}: ${fullStandardsContext.targetStandard.description}

Prerequisite Standards & Supporting Learning Components:
${prerequisiteText}`;

      const response = await openai.chat.completions.create({
        model: OPENAI_MODEL,
        messages: [
          { role: 'system', content: 'You are an expert middle school math tutor.' },
          { role: 'user', content: prompt }
        ],
        temperature: OPENAI_TEMPERATURE
      });

      const practiceQuestions = response.choices[0].message.content.trim();

      console.log(`✅ Generated practice questions:\n`);
      console.log(practiceQuestions);

      return {
        aiGenerated: practiceQuestions,
        targetStandard: fullStandardsContext.targetStandard.statementCode,
        prerequisiteCount: fullStandardsContext.prereqStandards.length
      };
    } catch (err) {
      console.error('❌ Error generating practice questions:', err.message);
      throw err;
    }
  };
}


async function main() {
  console.log('\n=== GENERATE PREREQUISITE PRACTICE TUTORIAL ===\n');

  console.log('🔄 Step 1: Loading data...');
  const aq = await import('arquero');
  const { relevantStandards, relevantRelationships, relevantLearningComponents } = loadData(aq);

  console.log('\n🔄 Step 2: Querying prerequisite data...');
  const prerequisiteData = queryPrerequisiteData(aq, relevantStandards, relevantRelationships, relevantLearningComponents);

  if (!prerequisiteData) {
    console.error('❌ Failed to find prerequisite data');
    return;
  }

  const { targetStandard, prerequisiteLearningComponents } = prerequisiteData;

  console.log('\n🔄 Step 3: Generating practice...');
  const fullStandardsContext = packageContextData(targetStandard, prerequisiteLearningComponents);
  const generatePractice = generatePracticeData(fullStandardsContext);
  if (GENERATE_PRACTICE) {
    await generatePractice();
  } else {
    console.log('🚫 Practice question generation disabled');
  }
}

main().catch(console.error);