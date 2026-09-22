<img style="width:100%" alt="Knowledge Graph banner logo" src="https://raw.githubusercontent.com/learning-commons-org/.github/refs/heads/main/assets/kg_hero_2.jpg" />

<p align="center">
  <a href="https://learningcommons.org/" target="_blank">Learning Commons</a>
   •
  <a href="https://platform.learningcommons.org/login?tab=signin" target="_blank">Platform</a>
  •
  <a href="https://docs.learningcommons.org/evaluators/" target="_blank">Docs</a>
</p>

## What is Knowledge Graph?

[Knowledge Graph](https://docs.learningcommons.org/knowledge-graph/understanding-knowledge-graph/introduction) is a structured collection of enriched educational datasets that connects academic standards, curricula, and learning science data. Datasets are modeled as graphs made up of [entities](https://docs.learningcommons.org/knowledge-graph/understanding-knowledge-graph/core-concepts) (the elements in a dataset) and [relationships](https://docs.learningcommons.org/knowledge-graph/understanding-knowledge-graph/core-concepts) (how those elements connect).

Knowledge Graph datasets use a standardized schema, so that edtech developers can build AI-powered tools without having to build a data pipeline themselves.

Check out [common use cases](https://docs.learningcommons.org/knowledge-graph/understanding-knowledge-graph/use-cases) and [tutorials](https://docs.learningcommons.org/knowledge-graph/getting-started/tutorials/) for Knowledge Graph.

## Access Knowledge Graph

Knowledge Graph is database-neutral and interoperable. Start with the [Quickstart](https://docs.learningcommons.org/knowledge-graph/getting-started/quickstart), or pick an access method:

| Access method                                                                                             | When to use                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| :-------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [**Knowledge Graph Explorer**](https://platform.learningcommons.org/apps/knowledge-graph/explorer)       | For a visual demo of Knowledge Graph data                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [**Agent plugins**](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/agent-plugins) | For asking ChatGPT or Claude about Knowledge Graph data                                                                                                                                                                                                                                                                                                                                                                                                                        |
| [**Local files**](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/local-files)     | For offline access and custom processing of Knowledge Graph data — download all data using [`curl`](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/local-files#download-all-data), or download by dataset using the [Dataset catalog](https://platform.learningcommons.org/dataset-catalog)&nbsp;↗<br/><br/>Can be used across graph databases, relational systems, in-memory tools, and AI pipelines without requiring any specialized infrastructure |
| [**REST API**](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/rest-api)           | For real-time programmatic access to Knowledge Graph data in an application                                                                                                                                                                                                                                                                                                                                                                                                    |
| [**MCP server**](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/mcp-server)       | For using Knowledge Graph data natively with an LLM                                                                                                                                                                                                                                                                                                                                                                                                                            |

## Datasets

Knowledge Graph datasets are grouped into [categories](https://docs.learningcommons.org/knowledge-graph/datasets/introduction). Each category shares a schema. Each dataset covers a specific educational domain and includes one or more file downloads.

Download a dataset from its docs page below, or from the [Dataset catalog](https://platform.learningcommons.org/dataset-catalog). To download the full graph as JSONL (`nodes.jsonl` and `relationships.jsonl`), see [Local files](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/local-files).

Access types: **Open** (freely downloadable), **Open + Gated** (some downloads open, others require approval), and **Gated** (approval required — contact [support@learningcommons.org](mailto:support@learningcommons.org)).

### Standards

[Schema reference](https://docs.learningcommons.org/knowledge-graph/schema-reference/standards)

Official expectations for student learning across academic subjects and jurisdictions, plus durable skills and learner competencies. Schema: [Standards](https://docs.learningcommons.org/knowledge-graph/schema-reference/standards).

| Dataset                                                                                                                                                                  | Access | Downloads                          |
| :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----- | :--------------------------------- |
| [U.S. academic standards](https://docs.learningcommons.org/knowledge-graph/datasets/standards/us-academic-standards)                                                     | Open   | Math, ELA, Social Studies, Science |
| [U.S. academic standards crosswalks](https://docs.learningcommons.org/knowledge-graph/datasets/standards/us-academic-standards-crosswalks)                               | Open   | Math crosswalks, ELA crosswalks    |
| [English Language Development Standards Framework](https://docs.learningcommons.org/knowledge-graph/datasets/standards/english-language-development-standards-framework) | Open   | WIDA ELD Standards Framework       |
| [XQ Competencies](https://docs.learningcommons.org/knowledge-graph/datasets/standards/xq-competencies)                                                                   | Open   | XQ Competencies                    |
| [Carnegie Skills Progressions](https://docs.learningcommons.org/knowledge-graph/datasets/standards/carnegie-skills-progressions)                                         | Open   | Carnegie Skills Progressions       |

### Learning components

[Schema reference](https://docs.learningcommons.org/knowledge-graph/schema-reference/learning-components)

Granular skills or concepts that break academic standards into teachable parts. Schema: [Learning components](https://docs.learningcommons.org/knowledge-graph/schema-reference/learning-components).

| Dataset                                                                                                                              | Access | Downloads                 |
| :----------------------------------------------------------------------------------------------------------------------------------- | :----- | :------------------------ |
| [Math learning components](https://docs.learningcommons.org/knowledge-graph/datasets/learning-components/math-learning-components)   | Open   | Math learning components  |
| [ELA learning components](https://docs.learningcommons.org/knowledge-graph/datasets/learning-components/ela-learning-components)     | Open   | ELA learning components   |
| [Eedi Misconceptions Graph](https://docs.learningcommons.org/knowledge-graph/datasets/learning-components/eedi-misconceptions-graph) | Open   | Eedi Misconceptions Graph |

### Learning progressions

[Schema reference](https://docs.learningcommons.org/knowledge-graph/schema-reference/learning-progressions)

How standards build towards and relate to each other. Schema: [Learning progressions](https://docs.learningcommons.org/knowledge-graph/schema-reference/learning-progressions).

| Dataset                                                                                                                  | Access | Downloads          |
| :----------------------------------------------------------------------------------------------------------------------- | :----- | :----------------- |
| [Math Coherence Map](https://docs.learningcommons.org/knowledge-graph/datasets/learning-progressions/math-coherence-map) | Open   | Math Coherence Map |

### Curriculum

[Schema reference](https://docs.learningcommons.org/knowledge-graph/schema-reference/curriculum)

Standards-aligned lessons and assessments from a publisher. Schema: [Curriculum](https://docs.learningcommons.org/knowledge-graph/schema-reference/curriculum).

| Dataset                                                                                     | Access       | Downloads                                                                                |
| :------------------------------------------------------------------------------------------ | :----------- | :--------------------------------------------------------------------------------------- |
| [IM® v.360](https://docs.learningcommons.org/knowledge-graph/datasets/curriculum/im-v360)   | Open + Gated | Scope and sequence (Open); Instructional materials (Gated); Assessment materials (Gated) |
| [OpenSciEd](https://docs.learningcommons.org/knowledge-graph/datasets/curriculum/openscied) | Gated        | OpenSciEd curriculum (Gated)                                                             |

### Instructional guidance

[Schema reference](https://docs.learningcommons.org/knowledge-graph/schema-reference/instructional-guidance)

Grade- and subject-specific learner profiles, research-backed factors, and instructional strategies. Schema: [Instructional guidance](https://docs.learningcommons.org/knowledge-graph/schema-reference/instructional-guidance).

| Dataset                                                                                                                                                                 | Access | Downloads                                           |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----- | :-------------------------------------------------- |
| [Learner Variability Navigator](https://docs.learningcommons.org/knowledge-graph/datasets/instructional-guidance/learner-variability-navigator)                         | Gated  | Math models; Literacy models                        |
| [English Learners Success Forum Guidelines](https://docs.learningcommons.org/knowledge-graph/datasets/instructional-guidance/english-learners-success-forum-guidelines) | Open   | Math guidelines; ELA guidelines; Science guidelines |

## Additional resources

- [Use cases](https://docs.learningcommons.org/knowledge-graph/understanding-knowledge-graph/use-cases)
- [Core concepts](https://docs.learningcommons.org/knowledge-graph/understanding-knowledge-graph/core-concepts)
- [Tutorials](https://docs.learningcommons.org/knowledge-graph/getting-started/tutorials)
- [REST API](https://docs.learningcommons.org/api-reference/overview)

## License

Use of Knowledge Graph is subject to our [Terms of Use](https://docs.learningcommons.org/knowledge-graph/resources/terms-of-use).

Knowledge Graph **datasets** are not all licensed the same way. Each dataset (and sometimes each download) is labeled **Open**, **Open + Gated**, or **Gated**:

- **Open** — Typically [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.en) (attribution required) or [CC0](https://creativecommons.org/public-domain/cc0/)
- **Open + Gated** — Includes both **Open** and **Gated** downloads (e.g., the IM® v.360 dataset's **Scope and sequence** is **Open**, while **Instructional materials** and **Assessment materials** are **Gated**)
- **Gated** — Not covered by an open license; requires approval and separate licensing agreement from the publisher

For the terms that apply to a specific dataset or download, reference that dataset’s page and the [license docs](https://docs.learningcommons.org/knowledge-graph/resources/license).

## Support

Questions or feedback: [open an issue](https://github.com/learning-commons-org/knowledge-graph/issues) or email [support@learningcommons.org](mailto:support@learningcommons.org). See also [Support](https://docs.learningcommons.org/knowledge-graph/resources/support) and [release notes](https://docs.learningcommons.org/knowledge-graph/resources/release-notes).

To report a security issue, contact [security@learningcommons.org](mailto:security@learningcommons.org).
