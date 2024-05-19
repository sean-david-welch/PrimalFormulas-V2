RESOURCES := products about assets

build: $(RESOURCES)

$(RESOURCES):
	@GOOS=linux GOARCH=amd64 go build -o bin/$@/bootstrap src/$@/main.go
	@cd bin/$@ && zip function.zip bootstrap