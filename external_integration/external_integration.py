
import collections, concurrent.futures as cf, pathlib
import requests
from rdflib import Graph, Namespace, RDF

ROOT = pathlib.Path(__file__).resolve().parent.parent
DWC = Namespace("http://rs.tdwg.org/dwc/terms/")
DWCIRI = Namespace("http://rs.tdwg.org/dwc/iri/")
UA = {"User-Agent": "FAIR-course-UT-group11/1.0 (student project)"}
POPULATION = 5_000_000

g = Graph().parse(ROOT / "data" / "birdsoftheworld-fairified.ttl")
sightings = []
for occ in g.subjects(RDF.type, DWC.Occurrence):
    sightings.append(dict(
        taxon=str(g.value(occ, DWCIRI.toTaxon)).rsplit("/", 1)[1],
        place=str(g.value(occ, DWCIRI.inDescribedPlace)),
        locality=str(g.value(occ, DWC.locality)),
    ))


def gbif(key):
    return key, requests.get(f"https://api.gbif.org/v1/species/{key}", timeout=30).json()


with cf.ThreadPoolExecutor(8) as pool:
    taxa = dict(pool.map(gbif, sorted({s["taxon"] for s in sightings})))
family = {k: v.get("family") for k, v in taxa.items()}
print(f"{len(taxa)} GBIF taxa -> {len(set(family.values()))} families, {len({v.get('order') for v in taxa.values()})} orders")

london = {family[s["taxon"]] for s in sightings if s["locality"] == "London"}
print(f"families seen in London: {len(london)}")

# Query A, on the Wikidata endpoint: cities above the population threshold
query_a = f"""SELECT ?place WHERE {{
  ?place wdt:P31/wdt:P279* wd:Q515 ;      # instance of (a subclass of) city
         wdt:P1082 ?population .          # population
  FILTER(?population > {POPULATION})
}}"""
r = requests.get("https://query.wikidata.org/sparql", params={"query": query_a, "format": "json"}, headers=UA, timeout=120)
r.raise_for_status()
big = {b["place"]["value"] for b in r.json()["results"]["bindings"]}

# Query B, on our data: the sightings in those cities
big_sightings = [s for s in sightings if s["place"] in big]
print(f"cities with more than {POPULATION:,} inhabitants: {len({s['place'] for s in big_sightings})}, "
      f"sightings: {len(big_sightings)}, taxa: {len({s['taxon'] for s in big_sightings})}, "
      f"families: {len({family[s['taxon']] for s in big_sightings})}")
