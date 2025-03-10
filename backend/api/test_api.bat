#backend/api/test_api.bat
@echo off
echo Testing Device Registration...
curl -X POST "http://localhost:8000/api/register-device?device_name=test_device&ip_address=192.168.1.100&location=Office"
echo.

echo Testing Metrics Upload...
curl -X POST "http://localhost:8000/api/upload" -H "Content-Type: application/json" -d "{\"device_name\": \"test_device\", \"cpu_usage\": 45.2, \"ram_usage\": 68.7}"
echo.

echo Testing Device Metrics Upload...
curl -X POST "http://localhost:8000/api/metrics/upload" -H "Content-Type: application/json" -d "{\"device_name\": \"test_device\", \"cpu_usage\": 45.2, \"ram_usage\": 68.7}"
echo.

echo Fetching All Metrics...
curl -X GET "http://localhost:8000/api/metrics"
echo.

echo Fetching Limited Metrics (10)...
curl -X GET "http://localhost:8000/api/metrics?limit=10"
echo.

echo Fetching Third-Party Metrics...
curl -X GET "http://localhost:8000/api/third-party"
echo.

echo Fetching and Storing External Metrics...
curl -X POST "http://localhost:8000/api/fetch-external-metrics"
echo.

echo Testing complete!