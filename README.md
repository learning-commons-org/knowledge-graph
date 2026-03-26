<img style="width:100%" alt="knowledge_graph_banner" src="https://raw.githubusercontent.com/learning-commons-org/.github/refs/heads/main/assets/kg_hero.png" />

<p align="center">
  <a href="https://docs.learningcommons.org/knowledge-graph/v1-4-0/getting-started/download-the-data/" target="_blank">Getting set up</a>
</p>


## **About Knowledge Graph**
Knowledge Graph is a structured dataset that connects state academic standards, curricula, and learning science data from domain experts.

Key use cases include:

* **Standards alignment**: Identify how your content supports specific academic standards and create content rooted in learner competencies across all key subjects  
* **Instructional planning**: Create dependencies, learning progressions, and content coverage, starting with math in the Common Core State Standards  
* **Compare state standards**: Adapt content aligned to one state standard to other states, initially in math across Common Core State Standards and 15+ additional states  
* **Curriculum alignment:** Align your content or create additional materials aligned to curriculum (private-beta access only \- details below on how to join)

Knowledge Graph is distributed as graph-native JSONL export files, making it accessible without specialized infrastructure. These files directly represent the underlying graph model, enabling developers to work with the data in graph databases, while remaining easy to ingest with standard data-processing tools. Developers can load the data into graph databases for relationship-centric querying or transform it for use in relational databases and data pipelines. This structure enables rich querying and supports AI-enhanced educational applications.

For complete setup instructions and usage examples, see the [full docs](https://docs.learningcommons.org/knowledge-graph/).

## **Repository contents**

| Path | Description |
| :---- | :---- |
| [tutorials/](./tutorials/) | Standalone example apps to demonstrate how Knowledge Graph data could be applied to solve different use cases |
| [LICENSE](./LICENSE.md) | Open source license details |

##  **Quick Start**

You can access the Knowledge Graph data using:

- **REST API**: Authenticate and make HTTP requests to retrieve academic standards directly. Best for applications that need real-time access. *(Currently available only to private beta users)*
- **MCP Server**: AI models can reliably work with academic standards, learning components, and learning progressions. They can resolve standards, decompose them into granular learning components, and trace progressions across standards. *(Currently available only to private beta users)*
- **Local JSONL**: Download local JSONL files and query them directly. Best for offline access, custom processing, or complex queries. *(Publicly available)*

### REST API

> **Note:** The API is in limited early release and is only available to some private beta users. Because the API is an early release, current users should expect occasional breaking changes.

#### What you'll do

- Authenticate using an API key
- Get a standards framework identifier (CASE UUID) for Multi-State Mathematics
- Retrieve a list of academic standards using that framework identifier

#### What you'll need

- A Learning Commons Platform account
- An API key generated in the Learning Commons Platform

#### Base URL

All REST API requests should be sent to:

```
https://api.learningcommons.org/knowledge-graph/v0
```

#### Authentication

Include your API key in the `x-api-key` header on every request:

```
x-api-key: YOUR_API_KEY
```

#### STEP 1: Get a standards framework identifier

Use your preferred HTTP client to send a GET request to the standards frameworks endpoint to get the CASE UUID for Multi-State Mathematics.

```bash
curl -X GET \
  -H "x-api-key: YOUR_API_KEY" \
  "https://api.learningcommons.org/knowledge-graph/v0/standards-frameworks?academicSubject=Mathematics&jurisdiction=Multi-State"
```

You should receive a 200 response with the CCSS Math framework for Multi-State, including the framework name, jurisdiction, adoption status, and a `caseIdentifierUUID` (GUID). Copy the `caseIdentifierUUID` from the response for the next step.

#### STEP 2: Retrieve academic standards

Use the `caseIdentifierUUID` you copied from Step 1's response with the academic standards endpoint to retrieve the individual standards for that framework.

```bash
curl -X GET \
  -H "x-api-key: YOUR_API_KEY" \
  "https://api.learningcommons.org/knowledge-graph/v0/academic-standards?standardsFrameworkCaseIdentifierUUID=YOUR_UUID_FROM_STEP_1"
```

> **Note:** If you skipped Step 1, you can use the CCSS Math framework UUID: `c6496676-d7cb-11e8-824f-0242ac160002` in place of `YOUR_UUID_FROM_STEP_1`.

You should see a paginated list of academic standards aligned to that framework, including statement codes, descriptions, grade levels, and subject information.

Example response:

```json
{
  "data": [
    {
      "identifier": "e1755456-c533-5a84-891e-59725c0479e0",
      "caseIdentifierURI": "https://satchelcommons.com/ims/case/v1p0/CFItems/6b9bf846-d7cc-11e8-824f-0242ac160002",
      "caseIdentifierUUID": "6b9bf846-d7cc-11e8-824f-0242ac160002",
      "name": null,
      "statementCode": "3.NF.A.1",
      "description": "Understand a fraction $\\frac{1}{b}$ as the quantity formed by 1 part when a whole is partitioned into b equal parts; understand a fraction $\\frac{a}{b}$ as the quantity formed by a parts of size $\\frac{1}{b}$.",
      "statementType": "Standard",
      "normalizedStatementType": "Standard",
      "jurisdiction": "Multi-State",
      "academicSubject": "Mathematics",
      "gradeLevel": ["3"],
      "inLanguage": "en-US",
      "dateCreated": null,
      "dateModified": "2025-02-05",
      "notes": null,
      "author": "1EdTech",
      "provider": "Learning Commons",
      "license": "https://creativecommons.org/licenses/by/4.0/",
      "attributionStatement": "Knowledge Graph is provided by Learning Commons under the CC BY-4.0 license. Learning Commons received state standards and written permission under CC BY-4.0 from 1EdTech."
    }
  ],
  "pagination": {
    "limit": 1,
    "nextCursor": "eyJpZGVudGlmaWVyIjogImUxNzU1NDU2LWM1MzMtNWE4NC04OTFlLTU5NzI1YzA0NzllMCJ9",
    "hasMore": true
  }
}
```

### Local JSONL Files

The Knowledge Graph data is available for download in newline delimited JSONL format with UTF-8 encoding. The graph data is exported with `nodes.jsonl` representing the nodes of the knowledge graph and the `relationships.jsonl` file capturing the connections between nodes.

#### Files

- `nodes.jsonl`: Contains graph node records, defining each node by a unique identifier, labels, and a set of associated properties.
- `relationships.jsonl`: Contains graph relationship records, describing how nodes are connected, including the relationship type, properties, and the source and target nodes.

#### Download options

You can download the files through direct links or using curl commands.

**Direct links**

- [nodes.jsonl](https://cdn.learningcommons.org/knowledge-graph/v1.7.0/exports/nodes.jsonl?ref=github)
- [relationships.jsonl](https://cdn.learningcommons.org/knowledge-graph/v1.7.0/exports/relationships.jsonl?ref=github)

**Using curl commands**

If you don't have curl installed, visit https://github.com/curl/curl for installation instructions.

```bash
curl -L "https://cdn.learningcommons.org/knowledge-graph/v1.7.0/exports/nodes.jsonl?ref=gh_curl" -o nodes.jsonl
curl -L "https://cdn.learningcommons.org/knowledge-graph/v1.7.0/exports/relationships.jsonl?ref=gh_curl" -o relationships.jsonl
```

#### Querying with jq

One option for querying the JSONL files is to use [jq](https://jqlang.github.io/jq/). Example to extract Common Core math standards:

```bash
jq -c 'select((.labels | contains(["StandardsFrameworkItem"])) and .properties.jurisdiction == "Multi-State" and .properties.academicSubject == "Mathematics")' nodes.jsonl > common_core_math_standards.jsonl
```

This filters for nodes with:
- **Label:** `StandardsFrameworkItem`
- **Jurisdiction:** `Multi-State` (Common Core)
- **Academic Subject:** `Mathematics`

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
