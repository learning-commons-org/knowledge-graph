# Changelog

## Knowledge Graph [v1.11.0](https://github.com/learning-commons-org/knowledge-graph/compare/v1.10.1...v1.11.0) (2026-07-09)

**July 09, 2026**

### Data v1.11.0

#### Added and updated [Academic Standards](/knowledge-graph/graph-reference/academic-standards) fields

- [`StandardsFrameworkItem`](/knowledge-graph/graph-reference/academic-standards#standardsframeworkitem)
  - Added optional `alternateStatementCode` field for statement codes that are not included in the [CASE specification](https://www.imsglobal.org/activity/case)&nbsp;↗ but are commonly used by publishers, teachers, and other edtech practitioners – Currently populated for [Texas Essential Knowledge and Skills (TEKS)](https://tea.texas.gov/curriculum-and-instruction/texas-essential-knowledge-and-skills-teks) and various other states' standards
- [`StandardsFramework`](/knowledge-graph/graph-reference/academic-standards#standardsframework) and [`StandardsFrameworkItem`](/knowledge-graph/graph-reference/academic-standards#standardsframeworkitem)
  - Updated `author` and `attributionStatement` fields to include mention of the state
  - Added `isCurrent` field that indicates whether the record is the most up-to-date version for the state-subject pair

## Knowledge Graph [v1.10.1](https://github.com/learning-commons-org/knowledge-graph/compare/v1.10.0...v1.10.1) (2026-07-01)

**July 01, 2026**

### Data v1.10.1

#### Fixed missing math Crosswalks

Restored math Standards Crosswalks between Texas and CCSS that were incorrectly removed in v1.9.0. Both the JSONL downloads and REST API have been updated. No other data was affected.

If you downloaded the Knowledge Graph JSONL files or queried the standards crosswalks during v1.9.0 or v1.10.0, re-download or re-query to pick up the restored data.

## Knowledge Graph [v1.10.0](https://github.com/learning-commons-org/knowledge-graph/compare/v1.9.0...v1.10.0) (2026-06-18)

**June 18, 2026**

### Data v1.10.0

#### English Language Arts (ELA) Learning Components

License and attribution statement values have been updated for each individual row.

#### Illustrative Mathematics

Improved data quality:

- Trimmed whitespace from fields
- Fixed `inLanguage` and `gradeLevel` fields where they didn't match `ENUM`
- Removed duplicate `hasChild` and `hasReference` relationships
- Updated `mutuallyExclusiveWith` relationship to always be bi-directional
- Added missing `Material` entities

#### Standards fixes

- Montana Social Studies - Several standards had `normalizedStatementType` incorrectly set to null
- New York Math - One standard had `statementType` and `normalizedStatementType` incorrectly set to null and was missing some Learning Component aligments
- Indiana Science - Some standards had `subject` incorrectly set to "Other"
- Removed a few Learning Components that were duplicated and causing inaccurate Jaccard scores for state Standards Crosswalks

## Knowledge Graph [v1.9.0](https://github.com/learning-commons-org/knowledge-graph/compare/v1.8.0...v1.9.0) (2026-05-27)

**May 27, 2026**

### Data v1.9.0

#### English Language Arts Learning Components

We've added Learning Components for English Language Arts, authored by Choice-filled Lives Network. The first release covers grades K–2 and is aligned to Common Core State Standards for ELA along with ELA standards from 12 states. Coverage now spans both Mathematics and English Language Arts.

#### Learning Component aligned states

We've added alignments to Learning Components for ELA standards from:
  - Connecticut
  - Delaware
  - Illinois
  - Maryland
  - Michigan
  - Mississippi
  - Nevada
  - New Hampshire
  - Vermont
  - Washington
  - Washington, D.C.
  - Wyoming

## [1.13.0](https://github.com/learning-commons-org/knowledge-graph/compare/v1.12.0...v1.13.0) (2026-08-12)


### Features

* initial upload of Knowledge Graph repository ([e59e3fa](https://github.com/learning-commons-org/knowledge-graph/commit/e59e3fa4524fe8f804e03ce7f85c52da23853158))
* update download links and curl commands to v1.8.0 ([#25](https://github.com/learning-commons-org/knowledge-graph/issues/25)) ([07c9ffb](https://github.com/learning-commons-org/knowledge-graph/commit/07c9ffbb4de518f0fc9c7271dc182f98777137d7))
* Update links and curl commands to version 1.6.0 ([#20](https://github.com/learning-commons-org/knowledge-graph/issues/20)) ([a05fedf](https://github.com/learning-commons-org/knowledge-graph/commit/a05fedf47e2c256fd2950d411ac5ea882062fedf))
* Update S3 links to version 1.1.0 ([#8](https://github.com/learning-commons-org/knowledge-graph/issues/8)) ([833b327](https://github.com/learning-commons-org/knowledge-graph/commit/833b327b9b8bc5c9674431f6d83619b3749b7423))
* v1-3-0 release ([#14](https://github.com/learning-commons-org/knowledge-graph/issues/14)) ([034abfb](https://github.com/learning-commons-org/knowledge-graph/commit/034abfbd784033b03ab64244688f0812524bf022))
* v1.2.0 updates ([#11](https://github.com/learning-commons-org/knowledge-graph/issues/11)) ([154652d](https://github.com/learning-commons-org/knowledge-graph/commit/154652d3aeba8d0ae8845345dec6f2f92b69830d))
* v1.5 graph update ([#18](https://github.com/learning-commons-org/knowledge-graph/issues/18)) ([8c3c020](https://github.com/learning-commons-org/knowledge-graph/commit/8c3c0206d7bff044aea82d2fb66b813dc3d0337a))


### Miscellaneous

* Adding release-please automation and conventional commits to Knowledge Graph repository ([#4](https://github.com/learning-commons-org/knowledge-graph/issues/4)) ([79c8403](https://github.com/learning-commons-org/knowledge-graph/commit/79c8403c829ce51388da5c11d4a2d1338395079b))
* fixing permissions issue in initial workflow push ([#5](https://github.com/learning-commons-org/knowledge-graph/issues/5)) ([3e55c64](https://github.com/learning-commons-org/knowledge-graph/commit/3e55c640d403d5f7cbe9ec349843dc1c2eafa788))
* **main:** release 1.1.0 ([#9](https://github.com/learning-commons-org/knowledge-graph/issues/9)) ([c1b46fb](https://github.com/learning-commons-org/knowledge-graph/commit/c1b46fb670d2c44bae2ea56a96edda5fea8fb017))
* **main:** release 1.10.0 ([#34](https://github.com/learning-commons-org/knowledge-graph/issues/34)) ([52e7dca](https://github.com/learning-commons-org/knowledge-graph/commit/52e7dca856f899e6c85c4da51fc947d91afa3694))
* **main:** release 1.11.0 ([#39](https://github.com/learning-commons-org/knowledge-graph/issues/39)) ([dcf4549](https://github.com/learning-commons-org/knowledge-graph/commit/dcf4549dcdf5ce1dada8b05f04c91068ac58adac))
* **main:** release 1.2.0 ([#13](https://github.com/learning-commons-org/knowledge-graph/issues/13)) ([3171102](https://github.com/learning-commons-org/knowledge-graph/commit/3171102d4c3ce75c69aad1813ed8e88e3864c7ce))
* **main:** release 1.3.0 ([#15](https://github.com/learning-commons-org/knowledge-graph/issues/15)) ([b103dcf](https://github.com/learning-commons-org/knowledge-graph/commit/b103dcf9b7fb42575a7bb6d2fbdddcc000a16b29))
* **main:** release 1.4.0 ([#16](https://github.com/learning-commons-org/knowledge-graph/issues/16)) ([90c2222](https://github.com/learning-commons-org/knowledge-graph/commit/90c2222aa232b7a33d6337b3f44b7198a90df4bf))
* **main:** release 1.5.0 ([#19](https://github.com/learning-commons-org/knowledge-graph/issues/19)) ([8a13bad](https://github.com/learning-commons-org/knowledge-graph/commit/8a13bad70e02cdd9771f8ff2d2265ddf3d7b5849))
* **main:** release 1.6.0 ([#21](https://github.com/learning-commons-org/knowledge-graph/issues/21)) ([a8f84e2](https://github.com/learning-commons-org/knowledge-graph/commit/a8f84e2dd0b4df2ac10b6548af2933e10560e7be))
* **main:** release 1.8.0 ([#26](https://github.com/learning-commons-org/knowledge-graph/issues/26)) ([e0b8e96](https://github.com/learning-commons-org/knowledge-graph/commit/e0b8e960c08d73332a92c95af188ee7d3031c40e))
* **main:** release 1.9.0 ([#28](https://github.com/learning-commons-org/knowledge-graph/issues/28)) ([b44dfed](https://github.com/learning-commons-org/knowledge-graph/commit/b44dfedcc01e838f05f3ba5fca1d7a113132a8c2))
* Update banner image in README.md ([#27](https://github.com/learning-commons-org/knowledge-graph/issues/27)) ([4bb557e](https://github.com/learning-commons-org/knowledge-graph/commit/4bb557e3f797ef38e647a6852d9bd3240d622f12))
* Update CHANGELOG for Knowledge Graph v1.10.1 ([#38](https://github.com/learning-commons-org/knowledge-graph/issues/38)) ([7c6f9ca](https://github.com/learning-commons-org/knowledge-graph/commit/7c6f9ca61984121d714ac6e1811527ae3854a24c))
* update download links to version 1.11.0 ([#40](https://github.com/learning-commons-org/knowledge-graph/issues/40)) ([49adf29](https://github.com/learning-commons-org/knowledge-graph/commit/49adf2983bd205bdc0f40631e0d9f89d16adf254))
* update download links to version 1.12.0 ([#41](https://github.com/learning-commons-org/knowledge-graph/issues/41)) ([7176dea](https://github.com/learning-commons-org/knowledge-graph/commit/7176dea7a441ea6300fde77e721539685ae283fe))

## [1.8.1](https://github.com/learning-commons-org/knowledge-graph/compare/v1.8.0...v1.8.1) (2026-05-27)

### Miscellaneous

* Update banner image in README.md ([#27](https://github.com/learning-commons-org/knowledge-graph/issues/27)) ([4bb557e](https://github.com/learning-commons-org/knowledge-graph/commit/4bb557e3f797ef38e647a6852d9bd3240d622f12))

## Knowledge Graph [v1.8.0](https://github.com/learning-commons-org/knowledge-graph/compare/v1.7.0...v1.8.0) (2026-04-23)

**March 26, 2026**

### API updates
Added a curriculum dependency map endpoint for getting dependencies and prerequisites between Lesson Groupings.

### Data v1.8.0
#### Learning component aligned states

We've added alignments to learning components and crosswalks to Common Core for standards from:

* Alabama
* Arkansas
* Missouri
* North Dakota
* Oregon
* Wyoming

We also completed the alignments to learning components from Texas for grades K-1, which completes all grades for Texas.

## Knowledge Graph [v1.7.0](https://github.com/learning-commons-org/knowledge-graph/compare/v1.6.0...v1.7.0) (2026-03-26)

**March 26, 2026**

### Learning component aligned states

We’ve added alignments to learning components and crosswalks to Common Core for standards from:

* Georgia
* Iowa
* Kentucky
* Tennessee
* West Virginia

### Data quality improvements

We’ve updated some of the alignments between learning components and the state standards from the following states to address inconsistencies:

* Utah
* South Dakota
* Mississippi
* Idaho
* Ohio

### Addition of `publisherIdentifier`

We added a new property `publisherIdentifier` for content nodes in Illustrative Mathematics. This property contains the ID that was originally assigned by Illustrative Mathematics. The field is available in both flat file downloads and REST API responses.

## Knowledge Graph [v1.6.0](https://github.com/learning-commons-org/knowledge-graph/compare/v1.5.0...v1.6.0) (2026-03-12)

**March 12, 2026**

### Learning component aligned states

We’ve added alignments to learning components and crosswalks to Common Core for standards from:

* Kansas

### Data quality improvements

* We've updated some of the alignments between learning components and Massachusetts state standards in order to fix some inconsistent alignments.
* We've fixed the direction of the hasDependency relationship between curriculum components in Illustrative Mathematics content.

## Knowledge Graph [v1.5.0](https://github.com/learning-commons-org/knowledge-graph/compare/v1.4.0...v1.5.0) (2026-02-26)

**February 26, 2026**

### Learning component aligned states

We’ve added alignments to learning components and crosswalks to Common Core for standards from:

* North Carolina

### Curriculum scope and sequence REST API endpoints

We’ve introduced a new set of curriculum endpoints and expanded our academic standards lookup capabilities.

**Curriculum**

* New endpoints provide structured access to curriculum metadata for Illustrative Math’s IM360 scope and sequence  
* Access courses, scope and sequence, lesson groupings (units/modules), lessons, activities, and assessments  
* View academic standards aligned to lessons, activities, and assessments  
* Note: instructional materials (lesson/activity/assessment content) are not included  

**Academic Standards**

* Added three new endpoints to retrieve lessons, activities, and assessments aligned to a specific academic standard by CASE UUID

## Knowledge Graph [v1.4.0](https://github.com/learning-commons-org/knowledge-graph/compare/v1.3.0...v1.4.0) (2026-02-12)

**February 12, 2026**

This release adds new aligned states.

## **Updates**

### Learning component aligned states

We’ve added alignments to learning components and crosswalks to Common Core for standards from:

* Florida
* Idaho
* Mississippi
* Ohio
* South Dakota
* Utah

## **Knowledge Graph [v1.3.0](https://github.com/learning-commons-org/knowledge-graph/compare/v1.2.0...v1.3.0) (2026-01-28)**

**January 28, 2026**

This release adds a new aligned state, makes the Illustrative Mathematics 360 curriculum’s scope and sequence available under CC-BY 4.0, and the Knowledge Graph is now available for download in newline delimited jsonl format with UTF-8 encoding.

## **Updates**

### **Learning component aligned states**

We've added alignment between learning components and standards for the following states:

* Massachusetts

### **Illustrative Mathematics scope and sequence (CC BY-4.0)**

The scope and sequence for the Illustrative Mathematics 360 curriculum is now available under a CC BY-4.0 license. 

### **Learner Variability Navigator**

We’ve added the relevantToStandard relationship that links a Factor to a StandardFrameworkItem for Common Core ELA standards. 

### **Graph-native JSON**

The Knowledge graph data is available for download in newline delimited jsonl format with UTF-8 encoding.

### **CSV deprecation**

The Knowledge Graph can no longer be downloaded as CSV flat files from v1.3.0 onwards. Any CSV flat files that were previously downloaded will be unaffected.

## **Knowledge Graph [v1.2.0](https://github.com/learning-commons-org/knowledge-graph/compare/v1.1.0...v1.2.0) (2025-12-08)**

**December 8, 2025**

This release adds a new learning component aligned state and a new relationship for Standards crosswalks.

## Updates

### Learning component aligned states

We’ve added alignment between learning components and standards for the following states:

* Wisconsin

### Crosswalks

You can now compare the individual state standards to their alignment to Common Core state standards using four new fields. Learn more [here](https://docs.learningcommons.org/knowledge-graph/v1-2-0/entity-and-relationship-reference/crosswalks).

### Learner Variability Navigator

The Learner Variability Navigator dataset from Digital Promise is now available to the private beta.

### Attribution statement

We’ve updated our attribution statement to reflect the name Learning Commons.

## **Knowledge Graph [v1.1.0](https://github.com/learning-commons-org/knowledge-graph/compare/v1.0.0...v1.1.0) (2025-10-30)**

**October 30, 2025**

This release adds new learning component aligned states and a new state academic standards framework.

## **Updates**

### **Learning component aligned states**

We've added alignment between learning components and standards for the following states:

* Louisiana  
* Montana  
* Pennsylvania  
* Washington, D.C.

### **Academic standards**

We've added academic standards for Washington, D.C
