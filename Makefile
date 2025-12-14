# Variables
PYTHON = python3
PYTEST = pytest
COVERAGE = coverage
RUFF = ruff
PDOC = pdoc3

# Dossiers
SRC_DIR = TP/Code
TEST_DIR = TP/testes

# Targets obligatoires selon le sujet

.PHONY: all test unit_test perf_test coverage lint doc clean

all: test lint

# Lance tous les tests (unitaires + performance)
test:
	$(PYTEST) $(TEST_DIR)

# Lance uniquement les tests unitaires (exclut ceux marqués @pytest.mark.perf)
unit_test:
	$(PYTEST) -m "not perf" $(TEST_DIR)

# Lance uniquement les tests de performance
perf_test:
	$(PYTEST) -m "perf" $(TEST_DIR)

# Génère un rapport de couverture de code
coverage:
	$(COVERAGE) run --source $(SRC_DIR) -m pytest -m "not perf" $(TEST_DIR)
	$(COVERAGE) report -m
	$(COVERAGE) html
	@echo "Rapport HTML généré dans htmlcov/index.html"

# Valide la qualité de code avec ruff
lint:
	$(RUFF) check $(SRC_DIR) $(TEST_DIR)

# Génère la documentation HTML avec pdoc3
doc:
	$(PDOC) --html --output-dir docs --force $(SRC_DIR)
	@echo "Documentation générée dans docs/"

# Nettoyage des fichiers temporaires
clean:
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf docs
	rm -f .coverage
	find . -type d -name "__pycache__" -exec rm -rf {} +