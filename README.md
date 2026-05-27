# Knowledge Graph

<img style="width:100%" alt="Knowledge Graph banner logo" src="https://raw.githubusercontent.com/learning-commons-org/.github/refs/heads/main/assets/kg_hero_2.jpg" />

<p align="center">
  <a href="https://docs.learningcommons.org/knowledge-graph/getting-started/quickstart" target="_blank">Quickstart</a>
</p>

Knowledge Graph is a structured dataset that connects state academic standards, curricula, and learning science data from domain experts.

It is distributed as graph-native JSONL export files, making it accessible without specialized infrastructure. These files directly represent the underlying graph model, enabling developers to work with the data in graph databases, while remaining easy to ingest with standard data-processing tools. Developers can load the data into graph databases for relationship-centric querying or transform it for use in relational databases and data pipelines. This structure enables rich querying and supports AI-enhanced educational applications.

For complete setup instructions and usage examples, see our [docs site](https://docs.learningcommons.org/knowledge-graph/).

## Use cases

- **Standards alignment**: Identify how your content supports specific academic standards and create content rooted in learner competencies across all key subjects
- **Instructional planning**: Create dependencies, learning progressions, and content coverage, starting with math in the Common Core State Standards
- **Compare state standards**: Adapt content aligned to one state standard to other states, initially in math across Common Core State Standards and 15+ additional states
- **Curriculum alignment:** Align your content or create additional materials aligned to curriculum (private-beta access only \- details below on how to join)

## Repository contents

| Path                       | Description                                                                                                   |
| :------------------------- | :------------------------------------------------------------------------------------------------------------ |
| [tutorials/](./tutorials/) | Standalone example apps to demonstrate how Knowledge Graph data could be applied to solve different use cases |
| [LICENSE](./LICENSE.md)    | Open source license details                                                                                   |

## Quickstart

You can access Knowledge Graph data in several ways:

| Method                                           | Description                                                                                                                                                                                                                 | Best for                                              |
| :----------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------- |
| [REST API](./docs/rest-api.md)                   | Authenticate and make HTTP requests to retrieve academic standards directly.                                                                                                                                                | Applications that need real-time access               |
| MCP Server                                       | AI models can reliably work with academic standards, learning components, and learning progressions. They can resolve standards, decompose them into granular learning components, and trace progressions across standards. | AI agents and MCP-compatible tools                    |
| [Local JSONL files](./docs/local-jsonl-files.md) | Download local JSONL files and query them directly.                                                                                                                                                                         | Offline access, custom processing, or complex queries |

## Support & feedback

For questions or feedback, please [open an issue](https://github.com/learning-commons-org/knowledge-graph/issues) or reach out to us at [support@learningcommons.org](mailto:support@learningcommons.org).

## Partner with us

**Learn more about our Knowledge Graph or join our private beta to access:**

- Full curriculum-aligned datasets
- Early access to new features and APIs
- Personalized support from the Knowledge Graph team

Contact us [here](https://learningcommons.org/contact/?utm_source=github&utm_medium=kg&utm_campaign=privatebeta).

## Reporting security issues

If you believe you have found a security issue, please disclose responsibly by contacting us at [security@learningcommons.org](mailto:security@learningcommons.org).

## Disclaimer

Use of Knowledge Graph and other Learning Commons resources is subject to our [Terms of Use](https://learningcommons.org/terms-of-use/).
