$resp = Invoke-RestMethod -Method Post -Uri 'http://127.0.0.1:6868/api/auth/login' -Body (ConvertTo-Json @{user_name='kc1015'; password='58997'}) -ContentType 'application/json'
$token = $resp.token
Write-Output "TOKEN: $token"
Invoke-RestMethod -Method Get -Uri 'http://127.0.0.1:6868/api/owner/customers/' -Headers @{Authorization="Bearer $token"} | ConvertTo-Json -Depth 5
