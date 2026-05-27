# REST API

> **Note:** The API is in limited early release and is only available to some private beta users. Because the API is an early release, current users should expect occasional breaking changes.

## What you'll do

- Authenticate using an API key
- Get a standards framework identifier (CASE UUID) for Multi-State Mathematics
- Retrieve a list of academic standards using that framework identifier

## What you'll need

- A Learning Commons Platform account
- An API key generated in the Learning Commons Platform

## Base URL

All REST API requests should be sent to:

```
https://api.learningcommons.org/knowledge-graph/v0
```

## Authentication

Include your API key in the `x-api-key` header on every request:

```
x-api-key: YOUR_API_KEY
```

## STEP 1: Get a standards framework identifier

Use your preferred HTTP client to send a GET request to the standards frameworks endpoint to get the CASE UUID for Multi-State Mathematics.

```bash
curl -X GET \
  -H "x-api-key: YOUR_API_KEY" \
  "https://api.learningcommons.org/knowledge-graph/v0/standards-frameworks?academicSubject=Mathematics&jurisdiction=Multi-State"
```

You should receive a 200 response with the CCSS Math framework for Multi-State, including the framework name, jurisdiction, adoption status, and a `caseIdentifierUUID` (GUID). Copy the `caseIdentifierUUID` from the response for the next step.

## STEP 2: Retrieve academic standards

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
