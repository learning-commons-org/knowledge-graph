# Knowledge Graph

<img style="width:100%" alt="Knowledge Graph banner logo" src="https://raw.githubusercontent.com/learning-commons-org/.github/refs/heads/main/assets/kg_hero_2.jpg" />

<p align="center">
  <a href="https://platform.learningcommons.org/apps/knowledge-graph/explorer" target="_blank">Demo</a>
   •
  <a href="https://docs.learningcommons.org/knowledge-graph/understanding-knowledge-graph/introduction" target="_blank">Introduction</a>
   •
  <a href="https://docs.learningcommons.org/knowledge-graph/getting-started/quickstart" target="_blank">Quickstart</a>
   •
  <a href="https://docs.learningcommons.org/knowledge-graph/getting-started/tutorials" target="_blank">Tutorials</a>
</p>

Knowledge Graph is a data graph that can help edtech applications generate research-backed content, make data-driven recommendations, and better serve your users.

It covers a wide range of educational and learning science data:

| Dataset                                                                                                      | Description                                                                                          |
| :----------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------- |
| [Standards](https://docs.learningcommons.org/knowledge-graph/schema-reference/standards)                     | K-12 academic standards from state and national frameworks, with hierarchy and crosswalk alignments  |
| [Learning components](https://docs.learningcommons.org/knowledge-graph/schema-reference/learning-components) | Granular skills and concepts aligned to standards for content tagging and alignment                  |
| [Learning progressions](https://docs.learningcommons.org/knowledge-graph/schema-reference/learning-progressions) | Prerequisite and related-standard relationships between standards items                              |
| [Curriculum](https://docs.learningcommons.org/knowledge-graph/schema-reference/curriculum)                   | Courses, lessons, activities, assessments, and materials aligned to the K-12 curriculum ontology     |
| [Instructional guidance](https://docs.learningcommons.org/knowledge-graph/schema-reference/instructional-guidance) | Learner models, factors, and instructional strategies from learning science research               |

By integrating Knowledge Graph, you can draw from official standards and materials to plan lessons, generate resources, and better support both teachers and students. Knowledge Graph is framework-agnostic and has applications as vast as your users’ goals.

Check out the [Quickstart](https://docs.learningcommons.org/knowledge-graph/getting-started/quickstart) to start downloading and using Knowledge Graph data.

## Example use cases

- Reference [standards](https://docs.learningcommons.org/knowledge-graph/schema-reference/standards) data to generate a 5th grade science lesson that aligns to California’s state standards
- Use [learning components](https://docs.learningcommons.org/knowledge-graph/schema-reference/learning-components) and [progressions](https://docs.learningcommons.org/knowledge-graph/schema-reference/learning-progressions) data to create a cumulative test that assesses a student’s progress through their English Language Arts unit
- Leverage [curriculum](https://docs.learningcommons.org/knowledge-graph/schema-reference/curriculum) data to build personalized assessments for students struggling with a particular concept or skill, like adding improper fractions
- Use [instructional guidance](https://docs.learningcommons.org/knowledge-graph/schema-reference/instructional-guidance) data to anticipate common math mistakes students make and generate differentiated lesson plans for these hurdles

Check out [more use cases](https://docs.learningcommons.org/knowledge-graph/understanding-knowledge-graph/use-cases) for Knowledge Graph data in your edtech application.

## Repository contents

| Path                       | Description                                                                    |
| :------------------------- | :----------------------------------------------------------------------------- |
| [tutorials/](./tutorials/) | Example apps demonstrating Knowledge Graph applications in different use cases |
| [LICENSE](./LICENSE.md)    | Open source license details                                                    |

Check out more [Knowledge Graph tutorials here](https://docs.learningcommons.org/knowledge-graph/getting-started/tutorials).

## Quickstart

You can access Knowledge Graph data in several ways:

| Access method                                                                                         | When to use                                                                                                                                                                                                                                                                                                                                           |
| :---------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Agent plugins](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/agent-plugins) | For asking ChatGPT or Claude about Knowledge Graph data                                                                                                                                                                                                                                                                                               |
| [Local files](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/local-files)     | For offline access and custom processing of Knowledge Graph data — download all data using curl, or download by dataset using the [Dataset catalog](https://platform.learningcommons.org/dataset-catalog). Can be used across graph databases, relational systems, in-memory tools, and AI pipelines without requiring any specialized infrastructure |
| [REST API](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/rest-api)           | For real-time programmatic access to Knowledge Graph data in an application                                                                                                                                                                                                                                                                           |
| [MCP server](https://docs.learningcommons.org/knowledge-graph/using-knowledge-graph/mcp-server)       | For using Knowledge Graph data natively with an LLM                                                                                                                                                                                                                                                                                                   |

## Support & feedback

For questions or feedback, please [open an issue](https://github.com/learning-commons-org/knowledge-graph/issues) or reach out to us at [support@learningcommons.org](mailto:support@learningcommons.org).

To report a security issue, please disclose responsibly by contacting us at [security@learningcommons.org](mailto:security@learningcommons.org).

## Disclaimer

Use of Knowledge Graph and other Learning Commons resources is subject to our [Terms of Use](https://learningcommons.org/terms-of-use/).
