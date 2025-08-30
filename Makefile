# Các biến
PROTO_DIR = proto
GEN_DIR = generated
PROTOC = python -m grpc_tools.protoc

# File proto
PROTO_FILES = $(wildcard $(PROTO_DIR)/*.proto)

# Lệnh sinh code
generate:
	@mkdir -p $(GEN_DIR)
	$(PROTOC) -I=$(PROTO_DIR) --python_out=$(GEN_DIR) --grpc_python_out=$(GEN_DIR) $(PROTO_FILES)

# Chạy server
run-server:
	python server/server.py

# Chạy client
run-client:
	python client/client.py

# Dọn build
clean:
	rm -rf $(GEN_DIR)/*.py
