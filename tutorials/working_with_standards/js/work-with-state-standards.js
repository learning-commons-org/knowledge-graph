/* ================================
   CONFIGURATION & SETUP
   ================================ */

// Dependencies
const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse/sync');
const { cosineSimilarity } = require('fast-cosine-similarity');
require('dotenv').config();

// Constants
const GENERATE_EMBEDDINGS = true;
const MIDDLE_SCHOOL_GRADES = ['6', '7', '8'];
// For this tutorial, we use 'all-MiniLM-L6-v2' which provides good quality embeddings
// for short text. You can substitute any compatible embedding model.
const EMBEDDING_MODEL = 'Xenova/all-MiniLM-L6-v2';

// Environment setup
const dataDir = process.env.KG_DATA_PATH;
if (!dataDir) {
  console.error('❌ KG_DATA_PATH environment variable is not set.');
  process.exit(1);
}
const EMBEDDING_FILE_PATH = path.join(dataDir, 'california_math_embeddings.json');

// Initialize embedding pipeline (will be loaded on first use)
let embedder = null;
let pipeline = null;

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

function findFrameworkItem(caseIdentifierUUID, standardsFrameworkItemsData) {
  return standardsFrameworkItemsData.find(item => item.caseIdentifierUUID === caseIdentifierUUID);
}


/* ================================
   STEP 1: LOAD DATA
   ================================ */
function loadData(aq) {
  /* Load CSV data files needed for the tutorial
   */
  const standardsFrameworksData = loadCSV('StandardsFramework.csv');
  const standardsFrameworkItemsData = loadCSV('StandardsFrameworkItem.csv');
  
  console.log('✅ Files loaded from KG CSV files');
  console.log({
    standardsFrameworks: standardsFrameworksData.length,
    standardsFrameworkItems: standardsFrameworkItemsData.length
  });
  
  return { standardsFrameworksData, standardsFrameworkItemsData };
}

/* ================================
   STEP 2: QUERY FOR STANDARDS DATA
   ================================ */

function getMathStandardsFrameworks(aq, standardsFrameworksData) {
  /* Get snapshot of mathematics standards frameworks
   * 
   * SQL:    SELECT "name", "academicSubject", "jurisdiction", "identifier"
   *         FROM standards_framework
   *         WHERE "academicSubject" = 'Mathematics';
   * 
   * Cypher: MATCH (sf:StandardsFramework {academicSubject: 'Mathematics'})
   *         RETURN sf.name, sf.academicSubject, sf.jurisdiction, sf.identifier
   */
  const mathFrameworks = aq.from(standardsFrameworksData)
    .filter(d => d.academicSubject === 'Mathematics')
    .select('caseIdentifierUUID', 'name', 'jurisdiction', 'academicSubject');
    
  console.log(`✅ Retrieved ${mathFrameworks.numRows()} state standard frameworks for math (dataframe):`);
  console.log('Sample of first 5 frameworks:');
  console.log(mathFrameworks.slice(0,5).objects());

  /* Get California math framework metadata
   * 
   * SQL: SELECT *
   * FROM standards_framework
   * WHERE "jurisdiction" = 'California'
   *   AND "academicSubject" = 'Mathematics';
   * Cypher: MATCH (sf:StandardsFramework {jurisdiction: 'California', academicSubject: 'Mathematics'}) RETURN sf
   */
  const californiaFrameworkTable = aq.from(standardsFrameworksData)
    .filter(d => d.jurisdiction === 'California' && d.academicSubject === 'Mathematics')
    .select('caseIdentifierUUID', 'name', 'jurisdiction', 'academicSubject');
  
  const californiaFramework = californiaFrameworkTable.object();

  console.log(`✅ Retrieved ${californiaFramework ? 1 : 0} California math standards framework:`);
  if (californiaFramework) {
    console.log(californiaFramework);
  }
  
  return { mathFrameworks, californiaFramework };
}

function getMiddleSchoolStandardsGroupings(aq, standardsFrameworkItemsData) {
  /* Filter for middle school standard groupings from California framework
   * 
   * SQL:    SELECT *
   *         FROM standards_framework_item
   *         WHERE "jurisdiction" = 'California'
   *           AND "academicSubject" = 'Mathematics'
   *           AND "normalizedStatementType" = 'Standard Grouping'
   *           AND (
   *                 EXISTS (SELECT 1 FROM json_array_elements_text("gradeLevel") AS elem WHERE elem = '6')
   *              OR EXISTS (SELECT 1 FROM json_array_elements_text("gradeLevel") AS elem WHERE elem = '7')
   *              OR EXISTS (SELECT 1 FROM json_array_elements_text("gradeLevel") AS elem WHERE elem = '8')
   *           );
   * 
   * Cypher: MATCH (sfi:StandardsFrameworkItem)
   *         WHERE sfi.jurisdiction = 'California'
   *           AND sfi.academicSubject = 'Mathematics'
   *           AND sfi.normalizedStatementType = 'Standard Grouping'
   *           AND any(g IN sfi.gradeLevel WHERE g IN ['6','7','8'])
   *         RETURN sfi;
   */
  const groupings = aq.from(standardsFrameworkItemsData)
    .filter(aq.escape(item => item.jurisdiction === 'California' && 
                              item.academicSubject === 'Mathematics' &&
                              item.normalizedStatementType === 'Standard Grouping' &&
                              (JSON.parse(item.gradeLevel || '[]')).some(level => MIDDLE_SCHOOL_GRADES.includes(level))))
    .select('caseIdentifierUUID', 'statementCode',  'description', 'normalizedStatementType', 'statementType', 'gradeLevel');
  
  console.log(`✅ Retrieved ${groupings.numRows()} standard groupings for middle school math in California (dataframe):`);
  console.log('Sample of first 5 standard groupings:');
  console.log(groupings.slice(0,5).objects());
  
  return groupings;
}

function getMiddleSchoolStandards(aq, standardsFrameworkItemsData) {
  /* Get all standards for California middle school mathematics
   * 
   * SQL:    SELECT *
   *         FROM standards_framework_item
   *         WHERE "jurisdiction" = 'California'
   *           AND "academicSubject" = 'Mathematics'
   *           AND "normalizedStatementType" = 'Standard'
   *           AND (
   *                 EXISTS (SELECT 1 FROM json_array_elements_text("gradeLevel") AS elem WHERE elem = '6')
   *              OR EXISTS (SELECT 1 FROM json_array_elements_text("gradeLevel") AS elem WHERE elem = '7')
   *              OR EXISTS (SELECT 1 FROM json_array_elements_text("gradeLevel") AS elem WHERE elem = '8')
   *           );
   * 
   * Cypher: MATCH (sfi:StandardsFrameworkItem)
   *         WHERE sfi.jurisdiction = 'California'
   *           AND sfi.academicSubject = 'Mathematics'
   *           AND sfi.normalizedStatementType = 'Standard'
   *           AND any(g IN sfi.gradeLevel WHERE g IN ['6','7','8'])
   *         RETURN sfi;
   */
  const standards = aq.from(standardsFrameworkItemsData)
    .filter(aq.escape(item => item.jurisdiction === 'California' && 
                              item.academicSubject === 'Mathematics' &&
                              item.normalizedStatementType === 'Standard' &&
                              (JSON.parse(item.gradeLevel || '[]')).some(level => MIDDLE_SCHOOL_GRADES.includes(level))))
    .select('caseIdentifierUUID', 'statementCode',  'description', 'normalizedStatementType', 'gradeLevel');
  
  console.log(`✅ Retrieved ${standards.numRows()} standards for California middle school mathematics (dataframe):`);
  console.log('Sample of first 5 standards:');
  console.log(standards.slice(100, 105).objects());
  
  return standards;
}

function queryForStandardsData(aq, standardsFrameworksData, standardsFrameworkItemsData) {
  const { mathFrameworks, californiaFramework } = getMathStandardsFrameworks(aq, standardsFrameworksData);
  const groupings = getMiddleSchoolStandardsGroupings(aq, standardsFrameworkItemsData);
  const standards = getMiddleSchoolStandards(aq, standardsFrameworkItemsData);
  
  return { californiaFramework, groupings, standards };
}

/* ================================
   STEP 3: EMBED STANDARD DATA
   ================================ */
function embedStandardData(aq, standardsFrameworkItemsData) {
  // Generate embeddings for California middle school mathematics standards
  const embeddingStandards = aq.from(standardsFrameworkItemsData)
    .filter(aq.escape(item => item.jurisdiction === 'California' && 
                              item.academicSubject === 'Mathematics' &&
                              item.normalizedStatementType === 'Standard' &&
                              (JSON.parse(item.gradeLevel || '[]')).some(level => MIDDLE_SCHOOL_GRADES.includes(level)) &&
                              !!item.description))
    .objects();

  /* Generate and save embeddings for each standard
   * This creates vector representations of standard descriptions for semantic search
   */
  return async function generateEmbeddings() {
    const results = [];
    console.log(`🔄 Generating embeddings for ${embeddingStandards.length} standards...`);

    // Initialize embedder if not already done
    if (!embedder) {
      console.log('📥 Loading embedding model (first time only)...');
      if (!pipeline) {
        const { pipeline: pipelineImport } = await import('@xenova/transformers');
        pipeline = pipelineImport;
      }
      embedder = await pipeline('feature-extraction', EMBEDDING_MODEL);
      console.log('✅ Embedding model loaded');
    }

    for (const standard of embeddingStandards) {
      const code = standard.statementCode || '(no code)';
      
      try {
        const output = await embedder(standard.description, { pooling: 'mean', normalize: true });
        const embedding = Array.from(output.data);

        results.push({
          caseIdentifierUUID: standard.caseIdentifierUUID,
          statementCode: standard.statementCode,
          embedding: embedding
        });

        console.log(`✅ ${code}`);
      } catch (err) {
        console.error(`❌ ${code}: ${err.message}`);
        throw err;
      }
    }

    // Save embeddings to file
    fs.writeFileSync(EMBEDDING_FILE_PATH, JSON.stringify(results, null, 2));
    console.log(`✅ Saved ${results.length} embeddings to ${EMBEDDING_FILE_PATH}`);
  };
}

/* ================================
   STEP 4: VECTOR SEARCH STANDARD DATA
   ================================ */
function vectorSearchStandardData(standardsFrameworkItemsData) {
  /* Perform vector search using cosine similarity
   */
  return async function vectorSearch(query, topK = 5) {
    // Initialize embedder if not already done
    if (!embedder) {
      console.log('📥 Loading embedding model...');
      if (!pipeline) {
        const { pipeline: pipelineImport } = await import('@xenova/transformers');
        pipeline = pipelineImport;
      }
      embedder = await pipeline('feature-extraction', EMBEDDING_MODEL);
      console.log('✅ Embedding model loaded');
    }

    let queryEmbedding;
    try {
      const output = await embedder(query, { pooling: 'mean', normalize: true });
      queryEmbedding = Array.from(output.data);
    } catch (error) {
      console.error(`❌ Error generating embedding for query "${query}": ${error.message}`);
      return;
    }

    let storedEmbeddings;
    try {
      storedEmbeddings = JSON.parse(fs.readFileSync(EMBEDDING_FILE_PATH, 'utf8'));
    } catch (error) {
      console.error(`❌ Error loading embeddings from ${EMBEDDING_FILE_PATH}: ${error.message}`);
      console.error('💡 Make sure to run the embedding generation step first (Step 3)');
      return;
    }

    const topResults = storedEmbeddings
      .map(item => ({
        caseIdentifierUUID: item.caseIdentifierUUID,
        score: cosineSimilarity(queryEmbedding, item.embedding)
      }))
      .sort((a, b) => b.score - a.score)
      .slice(0, topK);

    console.log(`\nTop ${topK} results for "${query}":\n`);

    

    topResults.forEach((result, i) => {
      const frameworkItem = findFrameworkItem(result.caseIdentifierUUID, standardsFrameworkItemsData);
      const statementCode = frameworkItem?.statementCode || '(no code)';
      const description = frameworkItem?.description || '(no statement)';

      topResults[i].statementCode = statementCode;
      topResults[i].description = description;
    });

    console.log(topResults);
  };
}

async function main() {
  const aq = await import('arquero');
  
  console.log('\n=== WORKING WITH STATE STANDARDS TUTORIAL ===\n');
  
  console.log('🔄 Step 1: Loading data...');
  const { standardsFrameworksData, standardsFrameworkItemsData } = loadData(aq);
  
  console.log('\n🔄 Step 2: Querying for standards data...');
  queryForStandardsData(aq, standardsFrameworksData, standardsFrameworkItemsData);
  
  console.log('\n🔄 Step 3: Embedding standard data...');
  const generateEmbeddings = embedStandardData(aq, standardsFrameworkItemsData);
  if (GENERATE_EMBEDDINGS) {
    await generateEmbeddings();
  } else {
    console.log('🚫 Embedding generation disabled');
  }
  
  console.log('\n🔄 Step 4: Vector searching standard data...');
  const vectorSearch = vectorSearchStandardData(standardsFrameworkItemsData);
  await vectorSearch('linear equations');
}

main().catch(console.error);