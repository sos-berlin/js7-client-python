# Starts the development environment using Docker Compose
compose:
	docker compose -p dev-js7-client-python -f ./docker/dev/compose.yml up -d

# Builds the project into a package
build:
	python -m build

# Uploads the package to PyPI
upload:
	python -m twine upload dist/*