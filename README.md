# Theorema Egregium: Dunkerque–Barcelona

The Delambre–Méchain meridian survey (1792–1798) re-read from inside the surface only, as Gauss's Theorema Egregium allows. Lengths come from the measured Melun base; curvature comes from the observed angles. No latitudes, azimuths or stars go into the curvature result.

## 📄 [Read the report](https://rooster-ninja.github.io/TheoremaEgregium_Dunkerque-Barcelona/)

Hosted on GitHub Pages from `index.html`. It links directly to the spreadsheets in [`supplemental/`](supplemental) and the page extracts in [`sources/`](sources).

## Results

| Result | Value | Uncertainty |
| --- | --- | --- |
| Rulers laid: four 2-toise (3.898 m) platinum bars, end to end | 3 021 at Melun, 2 987 at Perpignan | gaps read to 1/100 000 toise |
| Melun base, measured on the ground | 6 075.8973 toises = 11 842.146 m | ≈ 1 pouce (2.7 cm), per Delambre |
| Perpignan base: measured − carried through 115 triangles from Melun | 0.1485 toise = 28.9 cm | 25 ppm over ≈ 900 km |
| Radius from spherical excess of observed angles (91 triangles) | **5 360 km** | 1σ 5 160–5 590 km; 0.66″/triangle systematic bias |
| Same, constant bias per triangle fitted | 5 700 km | 1σ 5 200–6 300 km |
| Gauss's measure of curvature k = Σ(A·ε)/Σ(A²) | 3.48 × 10⁻⁸ km⁻² | 1σ 3.19–3.76 × 10⁻⁸; modern 2.46 × 10⁻⁸ |
| Regional R: north / centre / south | 5 880 / 5 550 / 4 930 km | ± 710 / 400 / 190 km |

From the triangles alone the survey shows the strip is, on average, positively curved, but with a large deviation in the radius: 1 010 km (16%) short of 6 371 km, and a 950 km spread between regions. The theorem cannot show constant curvature, a closed sphere or the flattening (35× below its resolution here); those need the astronomical reference. Modern geodesy relies on the sky even more: the reference frame comes from satellites (GNSS, SLR, DORIS) and VLBI, oriented to distant quasars, and triangulation chains like this one are no longer used to determine the figure. The volumes also record corrections made toward the expected figure (angles adjusted, series chosen, a latitude changed), so their own results are not an independent test. All results are fallible, inductive measurements, good to the sigma stated.

## Contents

| Folder | What's in it |
| --- | --- |
| `index.html` | The report, including a 3D view of each triangle's curvature (three.js) |
| `images/` | Tome II Planche I, the platinum ruler on its supports |
| `supplemental/` | `Melun_base_reduction.xlsx` (the base reduction, every step a formula) and `Triangle_chain_Dunkerque_Barcelona.xlsx` (115-triangle chain, Perpignan check, curvature fit, source discrepancies) |
| `sources/` | Page extracts from the scanned volumes. `*_annotated.pdf` carry the checks as PDF notes: yellow = a step, green = verified, red = misprint or open question |
| `data/` | Transcriptions as CSV: the Tableau complet, the Tome I observed angle sums, and the list of discrepancies found in the printed source |
| `scripts/` | Python that reproduces every number: `check.py` (transcription checks), `chain.py` (the chain and the Perpignan confirmation), `fitR.py` (radius and k from excess), `layout.py` (flat layout and per-triangle k for the 3D view) |

Run the scripts from `scripts/` with Python 3 and no dependencies: `python3 fitR.py`.

## Source

Delambre & Méchain, *Base du système métrique décimal, ou mesure de l'arc du méridien compris entre les parallèles de Dunkerque et Barcelone*, 4 vols, Paris 1806–1821. Scan: ETH-Bibliothek Zürich, Rar 10260, [doi:10.3931/e-rara-11803](https://doi.org/10.3931/e-rara-11803) (public domain). Gauss, *Disquisitiones generales circa superficies curvas* (1827), Arts. 12 and 20.

Transcription by hand from the scans, checked five ways per row. About 30 misprints remain in the printed toise and metre columns; none affect the logarithms, which Delambre states were the basis of every calculation (Tome II p. 703).
