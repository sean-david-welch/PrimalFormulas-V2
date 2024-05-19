# List of resources
RESOURCES := products about assets

# Default target
build: $(RESOURCES)

# Build target for each resource
$(RESOURCES):
	@echo "Building $@..."
	@mkdir -p bin/$@
	@GOOS=linux GOARCH=amd64 go build -o bin/$@/bootstrap src/$@/main.go
	@cd bin/$@ && zip function.zip bootstrap

# Clean target to remove build artifacts
clean:
	@rm -rf bin

# Phony targets
.PHONY: build clean $(RESOURCES)