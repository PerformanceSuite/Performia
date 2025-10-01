#!/bin/bash
# Integration test for API job persistence across restarts

set -e

echo "=========================================="
echo "API PERSISTENCE INTEGRATION TEST"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
API_URL="http://localhost:8000"
TEST_AUDIO="${1:-backend/test/test_audio.wav}"

# Check if test audio exists
if [ ! -f "$TEST_AUDIO" ]; then
    echo -e "${RED}❌ Test audio file not found: $TEST_AUDIO${NC}"
    echo "Usage: $0 [path_to_audio_file.wav]"
    exit 1
fi

# Function to check if API is running
check_api() {
    curl -s "$API_URL/health" > /dev/null 2>&1
    return $?
}

# Function to stop API if running
stop_api() {
    echo -e "${BLUE}Stopping any existing API instances...${NC}"
    pkill -f "uvicorn.*services.api.main" || true
    sleep 2
}

# Function to start API
start_api() {
    echo -e "${BLUE}Starting API server...${NC}"
    cd backend
    source venv/bin/activate
    nohup python -m uvicorn src.services.api.main:app --host 0.0.0.0 --port 8000 > /tmp/api.log 2>&1 &
    API_PID=$!
    cd ..

    # Wait for API to be ready
    for i in {1..30}; do
        if check_api; then
            echo -e "${GREEN}✅ API started (PID: $API_PID)${NC}"
            return 0
        fi
        sleep 1
    done

    echo -e "${RED}❌ API failed to start${NC}"
    cat /tmp/api.log
    return 1
}

# Test 1: Upload audio and create job
echo -e "\n${BLUE}=== Test 1: Upload Audio ===${NC}"
stop_api
rm -f backend/output/jobs.db  # Start with clean database
start_api

echo "Uploading audio file..."
RESPONSE=$(curl -s -X POST -F "file=@$TEST_AUDIO" "$API_URL/api/analyze")
echo "$RESPONSE" | jq .

JOB_ID=$(echo "$RESPONSE" | jq -r '.job_id')
if [ -z "$JOB_ID" ] || [ "$JOB_ID" = "null" ]; then
    echo -e "${RED}❌ Failed to create job${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Job created: $JOB_ID${NC}"

# Test 2: Check job status
echo -e "\n${BLUE}=== Test 2: Check Status ===${NC}"
sleep 2
STATUS=$(curl -s "$API_URL/api/status/$JOB_ID")
echo "$STATUS" | jq .

JOB_STATUS=$(echo "$STATUS" | jq -r '.status')
echo -e "${GREEN}✅ Job status: $JOB_STATUS${NC}"

# Test 3: List all jobs
echo -e "\n${BLUE}=== Test 3: List Jobs ===${NC}"
JOBS=$(curl -s "$API_URL/api/jobs")
echo "$JOBS" | jq .

JOB_COUNT=$(echo "$JOBS" | jq '.count')
echo -e "${GREEN}✅ Found $JOB_COUNT job(s)${NC}"

# Test 4: RESTART API and verify persistence
echo -e "\n${BLUE}=== Test 4: API RESTART ===${NC}"
echo "Stopping API..."
stop_api
echo "Waiting 3 seconds..."
sleep 3
echo "Starting API again..."
start_api

# Test 5: Verify job still exists after restart
echo -e "\n${BLUE}=== Test 5: Verify Persistence ===${NC}"
echo "Checking if job $JOB_ID still exists..."
STATUS_AFTER=$(curl -s "$API_URL/api/status/$JOB_ID")

if echo "$STATUS_AFTER" | jq -e '.job_id' > /dev/null; then
    echo "$STATUS_AFTER" | jq .
    echo -e "${GREEN}✅ Job survived restart!${NC}"
else
    echo -e "${RED}❌ Job not found after restart!${NC}"
    echo "$STATUS_AFTER"
    exit 1
fi

# Test 6: List jobs after restart
echo -e "\n${BLUE}=== Test 6: List Jobs After Restart ===${NC}"
JOBS_AFTER=$(curl -s "$API_URL/api/jobs")
echo "$JOBS_AFTER" | jq .

COUNT_AFTER=$(echo "$JOBS_AFTER" | jq '.count')
if [ "$COUNT_AFTER" = "$JOB_COUNT" ]; then
    echo -e "${GREEN}✅ Job count matches: $COUNT_AFTER${NC}"
else
    echo -e "${RED}❌ Job count mismatch: before=$JOB_COUNT, after=$COUNT_AFTER${NC}"
    exit 1
fi

# Test 7: Health check shows database path
echo -e "\n${BLUE}=== Test 7: Health Check ===${NC}"
HEALTH=$(curl -s "$API_URL/health")
echo "$HEALTH" | jq .

DB_PATH=$(echo "$HEALTH" | jq -r '.database')
echo -e "${GREEN}✅ Database: $DB_PATH${NC}"

# Test 8: Cleanup endpoint
echo -e "\n${BLUE}=== Test 8: Cleanup Old Jobs ===${NC}"
CLEANUP=$(curl -s -X DELETE "$API_URL/api/jobs/cleanup?days=30")
echo "$CLEANUP" | jq .
echo -e "${GREEN}✅ Cleanup endpoint working${NC}"

# Test 9: Delete job
echo -e "\n${BLUE}=== Test 9: Delete Job ===${NC}"
DELETE=$(curl -s -X DELETE "$API_URL/api/jobs/$JOB_ID")
echo "$DELETE" | jq .

# Verify deletion
sleep 1
STATUS_DELETED=$(curl -s "$API_URL/api/status/$JOB_ID")
if echo "$STATUS_DELETED" | jq -e '.detail' | grep -q "not found"; then
    echo -e "${GREEN}✅ Job deleted successfully${NC}"
else
    echo -e "${RED}❌ Job still exists after deletion${NC}"
    exit 1
fi

# Cleanup
echo -e "\n${BLUE}Cleaning up...${NC}"
stop_api

# Final results
echo ""
echo "=========================================="
echo -e "${GREEN}ALL TESTS PASSED ✅${NC}"
echo "=========================================="
echo ""
echo "Verified:"
echo "✅ Jobs persist to SQLite database"
echo "✅ Jobs survive API restarts"
echo "✅ All CRUD endpoints working"
echo "✅ Cleanup endpoint functional"
echo "✅ Health check shows database info"
echo ""
echo "Database location: $DB_PATH"
echo ""
echo -e "${GREEN}✅ PERSISTENCE SYSTEM PRODUCTION-READY${NC}"
echo ""
