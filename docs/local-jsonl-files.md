# Local JSONL files

Knowledge Graph data is available for download as JSONL files (`nodes.jsonl` and `relationships.jsonl`) with UTF-8 encoding:

| File                  | Description                                                                                                                                            | Download                                                                                                    | `curl` command                                                                                                                    |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| `nodes.jsonl`         | Contains graph node records, defining each node by a unique identifier, labels, and a set of associated properties.                                    | [JSONL file](https://cdn.learningcommons.org/knowledge-graph/v1.8.0/exports/nodes.jsonl?ref=github)         | `curl -L "https://cdn.learningcommons.org/knowledge-graph/v1.8.0/exports/nodes.jsonl?ref=gh_curl" -o nodes.jsonl`                 |
| `relationships.jsonl` | Contains graph relationship records, describing how nodes are connected, including the relationship type, properties, and the source and target nodes. | [JSONL file](https://cdn.learningcommons.org/knowledge-graph/v1.8.0/exports/relationships.jsonl?ref=github) | `curl -L "https://cdn.learningcommons.org/knowledge-graph/v1.8.0/exports/relationships.jsonl?ref=gh_curl" -o relationships.jsonl` |

If you don't have curl installed, visit https://github.com/curl/curl for installation instructions.

## Querying with `jq`

You can query the JSONL files using [`jq`](https://jqlang.github.io/jq/).

For example, to extract Common Core math standards, you can filter for nodes with a `StandardsFrameworkItem` label, `Multi-State` jurisdiction, and `Mathematics` as the subject:

```bash
jq -c 'select((.labels | contains(["StandardsFrameworkItem"])) and .properties.jurisdiction == "Multi-State" and .properties.academicSubject == "Mathematics")' nodes.jsonl > common_core_math_standards.jsonl
```
