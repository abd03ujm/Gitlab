```bash
curl -X POST "https://api.datadoghq.com/api/v2/services/definitions" \
-H "Content-Type: application/json" \
-H "DD-API-KEY: <YOUR_API_KEY>" \
-H "DD-APPLICATION-KEY: <YOUR_APP_KEY>" \
-d @data.json
```
