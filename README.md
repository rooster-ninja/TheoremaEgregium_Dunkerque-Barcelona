# Theorema Egregium: Dunkerque–Barcelona

The Delambre–Méchain meridian survey (1792–1798) re-read from inside the surface only, as Gauss's Theorema Egregium allows. Lengths come from the measured Melun base; curvature comes from the observed angles. No latitudes, azimuths or stars go into the curvature result.

**Read the report:** [`index.html`](index.html) (open it in a browser, or through GitHub Pages if enabled).

## Results

| Result | Value | Uncertainty |
| --- | --- | --- |
| Melun base, measured on the ground | 6 075.8973 toises = 11 842.146 m | ≈ 1 pouce (2.7 cm), per Delambre |
| Perpignan base: measured − carried through 115 triangles from Melun | 0.1485 toise = 28.9 cm | 25 ppm over ≈ 900 km |
| Radius from spherical excess of observed angles (91 triangles) | **5 360 km** | 1σ 5 160–5 590 km; 0.66″/triangle systematic bias |
| Same, constant bias per triangle fitted | 5 700 km | 1σ 5 200–6 300 km |
| Flattening from the 8 seconds-pendulum lengths (Tome IV), via Clairaut | 1/313 | 1σ 1/303–1/323 (needs star latitudes and the sidereal day) |
| Flattening from Tome III's 6 degree lengths | 1/240 | 1σ 1/185–1/339 (needs star latitudes) |

From the triangles alone the survey shows a curved Earth of roughly the right size, but only to about ±10–15%: the curvature signal is ≈ 1.5″ per triangle. The oblate figure needs the astronomical reference too. All results are fallible, inductive measurements, good to the sigma stated.

## Contents

| Folder | What's in it |
| --- | --- |
| `index.html` | The report |
| `supplemental/` | `Melun_base_reduction.xlsx` (the base reduction, every step a formula) and `Triangle_chain_Dunkerque_Barcelona.xlsx` (115-triangle chain, Perpignan check, curvature fit, source discrepancies) |
| `sources/` | Page extracts from the scanned volumes. `*_annotated.pdf` carry the checks as PDF notes: yellow = a step, green = verified, red = misprint or open question |
| `data/` | Transcriptions as CSV: the Tableau complet, the Tome I observed angle sums, and the list of discrepancies found in the printed source |
| `scripts/` | Python that reproduces every number: `check.py` (transcription checks), `chain.py` (the chain and the Perpignan confirmation), `fitR.py` (radius from excess), `pendulum_and_degrees.py` (flattening) |

Run the scripts from `scripts/` with Python 3 and no dependencies: `python3 fitR.py`.

## Source

Delambre & Méchain, *Base du système métrique décimal, ou mesure de l'arc du méridien compris entre les parallèles de Dunkerque et Barcelone*, 4 vols, Paris 1806–1821. Scan: ETH-Bibliothek Zürich, Rar 10260, [doi:10.3931/e-rara-11803](https://doi.org/10.3931/e-rara-11803) (public domain). Gauss, *Disquisitiones generales circa superficies curvas* (1827), Arts. 12 and 20.

Transcription by hand from the scans, checked five ways per row. About 30 misprints remain in the printed toise and metre columns; none affect the logarithms, which Delambre states were the basis of every calculation (Tome II p. 703).
