.PHONY: generate-commits create-commits serve help

help:
	@echo "Available commands:"
	@echo "  make generate-commits  - Generate commits.json with 30 commit timestamps"
	@echo "  make create-commits    - Create actual git commits from commits.json"
	@echo "  make serve             - Serve the webapp locally on http://localhost:8000"

generate-commits:
	@echo "Generating commits.json..."
	@python3 scripts/generate_commits.py

create-commits:
	@echo "Creating git commits from commits.json..."
	@python3 scripts/create_commits.py

serve:
	@echo "Serving webapp at http://localhost:8000"
	@echo "Open http://localhost:8000/webapp/index.html in your browser"
	@python3 -m http.server 8000

