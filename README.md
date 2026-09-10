# Linjun Zhang — personal website

The site is a static website hosted by GitHub Pages. Existing page addresses are preserved.

## Update content

- `data/profile.json`: recruitment year and update date.
- `data/publications.json`: paper titles, full author lists, years, venues, and links. `sources` records verification references; it is not shown on the page.
- `data/people.json`: students, alumni, and research interns.
- `data/teaching.json`: course history and available materials.
- `data/software.json`: research software.
- `scripts/build_site.py`: shared page layout, biography, and home-page text.
- `assets/site.css`: shared colors, typography, and responsive layout.

After editing, run:

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
```

Both commands use Python's standard library; no package installation is needed. Commit the generated HTML together with the data and source changes. GitHub Pages serves the generated files directly using the existing repository configuration.

Preview with `python3 -m http.server 8765 --bind 127.0.0.1`. All content is readable without JavaScript. JavaScript only enhances the mobile navigation and preserves the existing production-only StatCounter integration.

## Content conventions

- Use the final conference year for conference papers, even if Google Scholar uses a later proceedings indexing year.
- Clearly label preprints; do not infer acceptance from an arXiv listing.
- Consolidate preprint and published versions into one entry when they represent the same paper.
- Preserve `*` and `**` authorship notes from verified sources.
- Keep full author lists, and verify identity when importing records from Google Scholar.
- Retain the existing image, PDF, and HTML paths to avoid breaking old links.
