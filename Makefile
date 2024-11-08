# Makefile for setting up the templated project

# Default repository information (replace with your actual repo URL if needed)
REPO_URL := $(shell git config --get remote.origin.url)
AUTHOR := $(shell git config --get user.name)
PROJECT_NAME ?= my_project  # Default project name if none is provided
PROJECT_SLUG := $(shell echo $(PROJECT_NAME) | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9_]/_/g')

.PHONY: setup
setup:
	@echo "Setting up the project..."
	@echo "Project Name: $(PROJECT_NAME)"
	@echo "Project Slug: $(PROJECT_SLUG)"
	@echo "Repository URL: $(REPO_URL)"
	@echo "Author: $(AUTHOR)"

	# Install cookiecutter if not available
	@which cookiecutter > /dev/null || pip install cookiecutter

	# Run cookiecutter with pre-defined values
	@cookiecutter --no-input \
		--output-dir ./prefect_project_template \
		./prefect_project_template/ \
		project_name="$(PROJECT_NAME)" \
		project_slug="$(PROJECT_SLUG)" \
		self_repository_url="$(REPO_URL)" \
		author="$(AUTHOR)" \
		env_file=".env"

	# Copy generated files to the root of the repository
	@rsync -a ./prefect_project_template/$(PROJECT_SLUG)/ ./
	@rm -rf ./prefect_project_template/$(PROJECT_SLUG)

	# Commit the changes
	@git add .
	@git commit -m "Generate project using cookiecutter template"
	@echo "Setup complete. Don't forget to push your changes!"
