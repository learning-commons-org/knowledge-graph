# Changelog

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
