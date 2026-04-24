.PHONY: openapi swift-codegen

SCHEMAS_ROOT := $(CURDIR)
OPENAPI_JSON := $(SCHEMAS_ROOT)/python/openapi.json
MOBILE_GEN_DIR ?= $(SCHEMAS_ROOT)/../lap-mobile/Generated

openapi:
	cd python && uv run python -m lap_schemas.generate_openapi openapi.json

swift-codegen: openapi
	mkdir -p "$(MOBILE_GEN_DIR)"
	cd swift && npx openapi-generator-cli generate \
		-i "$(OPENAPI_JSON)" \
		-g swift5 \
		-o "$(MOBILE_GEN_DIR)" \
		-c openapi-generator-config.yaml
