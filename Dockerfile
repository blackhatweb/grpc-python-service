# Sử dụng python slim
FROM python:3.11-slim

# Set workdir
WORKDIR /app

# Copy requirements trước để cache layer
COPY requirements.txt .

# Cài đặt thư viện
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code
COPY . .

# Generate proto khi build image (nếu cần)
RUN make generate

# Expose port cho gRPC
EXPOSE 50051

# Default chạy server
CMD ["make", "run-server"]
