# birdsoftheworld-dataset-fairification

Cleans the messy `Birdsoftheworld.csv` into a structured dataset and publishes bird
occurrences and derived trait observations as RDF.

## Repository layout

```text
data/                  source exports and complete FAIRified RDF publication
metadata/              final public metadata records and SHACL schemas
metadata/fdp-exports/  original FDP record and schema exports
preprocessing/         original CSV and preprocessing code
ontology/ontology.ttl  agreed ontology publication target; file still to be added
```

## Public data and metadata

The published hierarchy is one catalog, one dataset, and two distributions:

| Role                            | File                                                                       |
| ------------------------------- | -------------------------------------------------------------------------- |
| Original data                   | [preprocessing/Birdsoftheworld.csv](preprocessing/Birdsoftheworld.csv)     |
| Complete FAIRified data         | [data/birdsoftheworld-fairified.ttl](data/birdsoftheworld-fairified.ttl)   |
| Catalog metadata                | [metadata/catalog.ttl](metadata/catalog.ttl)                               |
| Dataset metadata                | [metadata/dataset.ttl](metadata/dataset.ttl)                               |
| Original distribution metadata  | [metadata/distribution-original.ttl](metadata/distribution-original.ttl)   |
| FAIRified distribution metadata | [metadata/distribution-fairified.ttl](metadata/distribution-fairified.ttl) |
| Catalog schema                  | [metadata/catalog-shape.ttl](metadata/catalog-shape.ttl)                   |
| Dataset schema                  | [metadata/dataset-shape.ttl](metadata/dataset-shape.ttl)                   |
| Distribution schema             | [metadata/distribution-shape.ttl](metadata/distribution-shape.ttl)         |
| Shared Resource schema          | [metadata/resource-shape.ttl](metadata/resource-shape.ttl)                 |

The complete RDF distribution combines `data/bird-observations.ttl` and
`data/bird-trait-observations.ttl`.

## FDP exports and public copies

Some remarks about our modified Fair Data Point (FDP) exports. The catalog, dataset, and distributions were entered in a local FDP (using Docker). Their raw exports and the three exported resource-specific Form Definitions are preserved in
[metadata/fdp-exports/](metadata/fdp-exports/), separate from the final products. The final products have some minor corrections with the correct W3ID URIs and the correct provenance set.

The public Catalog, Dataset, and Distribution schema files are identical copies of the exported definitions from FDP. The shared Resource parent is in `metadata/resource-shape.ttl`. Load all four schema files when validating the complete public metadata.

## Identifiers and redirects

The publication files use the guide's main prefix:

```text
https://w3id.org/FAIR-course-UT/2025-2026/group11
```

Relative paths to the above prefix:

| W3ID path                          | Repository target                     |
| ---------------------------------- | ------------------------------------- |
| `/ont`                             | `ontology/ontology.ttl`               |
| `/data`                            | `data/birdsoftheworld-fairified.ttl`  |
| `/original.csv`                    | `preprocessing/Birdsoftheworld.csv`   |
| `/metadata/catalog`                | `metadata/catalog.ttl`                |
| `/metadata/dataset`                | `metadata/dataset.ttl`                |
| `/metadata/distribution-original`  | `metadata/distribution-original.ttl`  |
| `/metadata/distribution-fairified` | `metadata/distribution-fairified.ttl` |
| `/schema/catalog`                  | `metadata/catalog-shape.ttl`          |
| `/schema/dataset`                  | `metadata/dataset-shape.ttl`          |
| `/schema/distribution`             | `metadata/distribution-shape.ttl`     |
| `/schema/resource`                 | `metadata/resource-shape.ttl`         |

The original distribution keeps its [Kaggle DOI](https://doi.org/10.34740/kaggle/dsv/6119827)
as source/access URL. Its W3ID download URL resolves to the original CSV in GitHub,
as required in the Project Description.
