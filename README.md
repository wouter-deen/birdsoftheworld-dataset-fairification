# birdsoftheworld-dataset-fairification

Cleans the messy `Birdsoftheworld.csv` into a structured dataset.

## Persistent dataset identifier

<https://w3id.org/FAIR-course-UT/2026/group11/dataset/bird-observations>

Once the redirects are deployed, requesting this identifier with `Accept: text/turtle`
will return a redirect to [the dataset metadata](metadata/metadata.ttl). Other requests
will be redirected to this repository's landing page.

The metadata describes four distributions, using these persistent access and download URLs:

| Data         | Format-independent access URL                                                                       | Turtle download                                                                                             | CSV download                                                                                                |
| ------------ | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Observations | [observations](https://w3id.org/FAIR-course-UT/2026/group11/dataset/bird-observations/observations) | [observations.ttl](https://w3id.org/FAIR-course-UT/2026/group11/dataset/bird-observations/observations.ttl) | [observations.csv](https://w3id.org/FAIR-course-UT/2026/group11/dataset/bird-observations/observations.csv) |
| Traits       | [traits](https://w3id.org/FAIR-course-UT/2026/group11/dataset/bird-observations/traits)             | [traits.ttl](https://w3id.org/FAIR-course-UT/2026/group11/dataset/bird-observations/traits.ttl)             | [traits.csv](https://w3id.org/FAIR-course-UT/2026/group11/dataset/bird-observations/traits.csv)             |

Format-independent access URLs select Turtle or CSV using `Accept: text/turtle` or
`Accept: text/csv`, respectively, and otherwise redirect to the Turtle file's GitHub
page. Explicit download URLs select the format independently of the `Accept` header.

## Repository layout

```
data/         final RDF dataset (.ttl) will live here
metadata/     metadata ttl and its SHACL schema will live here
preprocessing/ original CSV, preprocessing and feature-extraction scripts,
              and generated intermediate outputs
```
