#!/bin/bash
# DataDistiller 2.0 - Quick Start Script

echo "╔════════════════════════════════════════════════════════════╗"
echo "║        DataDistiller 2.0 - Infrastructure Setup           ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install kafka-python==2.0.2 fastapi uvicorn boto3 redis psycopg2-binary rank-bm25 prometheus-client
echo "✅ Dependencies installed"
echo ""

# Start infrastructure
echo "🚀 Starting infrastructure services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy (30 seconds)..."
sleep 30

# Check service health
echo ""
echo "🔍 Checking service health..."
echo ""

services=(
    "datadistiller-zookeeper:2181"
    "datadistiller-kafka:9092"
    "datadistiller-postgres:5432"
    "datadistiller-redis:6379"
)

for service in "${services[@]}"; do
    name="${service%%:*}"
    port="${service##*:}"
    
    if docker ps | grep -q "$name"; then
        echo "  ✅ $name is running"
    else
        echo "  ❌ $name is not running"
    fi
done

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    Services Ready!                         ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🌐 Web UIs:"
echo "  • Kafka UI:      http://localhost:9000"
echo "  • MinIO Console: http://localhost:9001 (minioadmin/minioadmin123)"
echo "  • Grafana:       http://localhost:3000 (admin/admin123)"
echo "  • Prometheus:    http://localhost:9090"
echo ""
echo "🧪 Run Tests:"
echo "  • Producer:  python workers/test_kafka_producer.py"
echo "  • Consumer:  python workers/test_kafka_consumer.py"
echo ""
echo "📖 Documentation:"
echo "  • Setup Guide:  cat PHASE1_KAFKA_SETUP.md"
echo "  • Full Roadmap: cat DATADISTILLER_2.0_ROADMAP.md"
echo ""
echo "🛑 Stop Services:"
echo "  • docker-compose down"
echo ""
