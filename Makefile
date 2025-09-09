PROTO_DIR = proto
GEN_DIR = generated
PROTOC = python -m grpc_tools.protoc
PROTO_FILES = $(wildcard $(PROTO_DIR)/*.proto)

generate:
	@mkdir -p $(GEN_DIR)
	$(PROTOC) -I=$(PROTO_DIR) --python_out=$(GEN_DIR) --grpc_python_out=$(GEN_DIR) $(PROTO_FILES)

run-server:
	python -m server.server

run-client:
	python -m client.client

clean:
	rm -rf $(GEN_DIR)/*.py
