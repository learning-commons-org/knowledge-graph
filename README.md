<img style="width:100%" alt="knowledge_graph_banner" src="https://raw.githubusercontent.com/learning-commons-org/.github/refs/heads/main/assets/kg_hero.png" />

<p align="center">
  <a href="https://docs.learningcommons.org/knowledge-graph/getting-started/download-the-data/" target="_blank">Getting set up</a>
  •
  <a href="https://docs.learningcommons.org/knowledge-graph/getting-started/tutorials/tutorial-overview" target="_blank">Tutorials</a>
</p>


## **About Knowledge Graph**
Knowledge Graph is a structured dataset that connects state academic standards, curricula, and learning science data from domain experts.

Key use cases include:

* **Standards alignment**: Identify how your content supports specific academic standards and create content rooted in learner competencies across all key subjects  
* **Instructional planning**: Create dependencies, learning progressions, and content coverage, starting with math in the Common Core State Standards  
* **Compare state standards**: Adapt content aligned to one state standard to other states, initially in math across Common Core State Standards and 15+ additional states  
* **Curriculum alignment:** Align your content or create additional materials aligned to curriculum (private-beta access only \- details below on how to join)

Knowledge Graph is distributed as CSV and JSON export files, making it accessible without specialized infrastructure. These files reflect a graph-based model, allowing developers to work with the data in relational databases or other environments. This structure enables rich querying and supports AI-enhanced educational applications.

For complete setup instructions and usage examples, see the [full docs](https://docs.learningcommons.org/knowledge-graph/).

## **Repository contents**

| Path | Description |
| :---- | :---- |
| [import\_scripts/](./import_scripts/) | Helper scripts to import Knowledge Graph data into relational databases |
| [sample\_queries/](./sample_queries/) | Example SQL queries for exploring Knowledge Graph data |
| [tutorials/](./tutorials/) | Standalone example apps to demonstrate how Knowledge Graph data could be applied to solve different use cases |
| [LICENSE](./LICENSE.md) | Open source license details |

##  **Quick Start**

The knowledge graph data is available for download in both CSV and JSON formats. The graph data is exported with each file representing a specific entity type, and a relationships file capturing the connections between entities.

**CSV files:** UTF-8 encoded with comma delimiters and quoted fields. All CSV files include header rows with column names.

**JSON files:** Newline delimited JSON format with UTF-8 encoding.

## Files

* `StandardsFramework`: Educational standards frameworks  
* `StandardsFrameworkItem`: Individual standards and learning objectives within frameworks  
* `LearningComponent`: Granular, precise representations of individual skills or concepts 
* `Relationships`: Connections and associations between all entity types

## Download options

There are two options to download the files: direct s3 links, or using curl commands.

### Direct S3 links  

**CSV files:**  
- [StandardsFramework.csv](https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/csv/StandardsFramework.csv?ref=github)  
- [StandardsFrameworkItem.csv](https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/csv/StandardsFrameworkItem.csv?ref=github)  
- [LearningComponent.csv](https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/csv/LearningComponent.csv?ref=github)  
- [Relationships.csv](https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/csv/Relationships.csv?ref=github)  

**JSON files:**  
- [StandardsFramework.json](https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/json/StandardsFramework.json?ref=github)  
- [StandardsFrameworkItem.json](https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/json/StandardsFrameworkItem.json?ref=github)  
- [LearningComponent.json](https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/json/LearningComponent.json?ref=github)  
- [Relationships.json](https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/json/Relationships.json?ref=github)  

### Using curl commands  


If you don't have `curl` installed, see [installation instructions](https://github.com/curl/curl).  

```bash
# Download CSV files
curl -L "https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/csv/StandardsFramework.csv?ref=gh_curl" -o StandardsFramework.csv
curl -L "https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/csv/StandardsFrameworkItem.csv?ref=gh_curl" -o StandardsFrameworkItem.csv
curl -L "https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/csv/LearningComponent.csv?ref=gh_curl" -o LearningComponent.csv
curl -L "https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/csv/Relationships.csv?ref=gh_curl" -o Relationships.csv
```
```bash
# Download JSON files
curl -L "https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/json/StandardsFramework.json?ref=gh_curl" -o StandardsFramework.json
curl -L "https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/json/StandardsFrameworkItem.json?ref=gh_curl" -o StandardsFrameworkItem.json
curl -L "https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/json/LearningComponent.json?ref=gh_curl" -o LearningComponent.json
curl -L "https://aidt-knowledge-graph-datasets-public-prod.s3.us-west-2.amazonaws.com/knowledge-graph/v1.0.0/json/Relationships.json?ref=gh_curl" -o Relationships.json
```

### **Next steps**

This quick start walked you through how to download Knowledge Graph so you can start using it. You can explore next steps under [import\_scripts/](./import_scripts/), [sample\_queries/](./sample_queries/) and [tutorials/](./tutorials/).

## **Support & Feedback**

We want to hear from you. For questions or feedback, please [open an issue](https://github.com/learning-commons-org/knowledge-graph/issues) or reach out to us at support@learningcommons.org. 

## **Partner with us**

**Learn more about our Knowledge Graph or join our private beta to access:**

* Full curriculum-aligned datasets

* Early access to new features and APIs

* Personalized support from the Knowledge Graph team

Contact us [here](https://learningcommons.org/contact/?utm_source=github&utm_medium=kg&utm_campaign=privatebeta).

## **Reporting Security Issues**

If you believe you have found a security issue, please responsibly disclose by contacting us at [security@learningcommons.org](mailto:security@learningcommons.org).

## **Disclaimer**

The resources provided in this repository are made available "as-is", without warranties or guarantees of any kind. They may contain inaccuracies, limitations, or other constraints depending on the context of use. Use of these resources is subject to [our Terms of Use](https://learningcommons.org/terms-of-use/).

By accessing or using these resources, you acknowledge that:

* You are responsible for evaluating their suitability for your specific use case.  
* Learning Commons makes no representations about the accuracy, completeness, or fitness of these resources for any particular purpose.  
* Any use of the materials is at your own risk, and Learning Commons is not liable for any direct or indirect consequences that may result.

Please refer to each resource’s README, license, and associated docs for any additional limitations, attribution requirements, or guidance specific to that resource.
