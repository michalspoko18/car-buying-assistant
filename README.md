# car-buying-assistant

Web application that helps users decide whether a specific car fits their needs. The system collects buyer priorities (e.g. fuel economy, reliability, performance) and car details, then generates an AI-based evaluation report including pros, cons, risks, and estimated ownership costs. Built with Django (server-side rendering) and OpenAI API.

## PDF report

PDF export uses `pdfkit` + `wkhtmltopdf`.

- Install Python deps: `pip install -r requirements.txt`
- Install `wkhtmltopdf`:
  - macOS (Homebrew): `brew install wkhtmltopdf`

If `wkhtmltopdf` is not on PATH, set `WKHTMLTOPDF_CMD` to the full path of the binary.
