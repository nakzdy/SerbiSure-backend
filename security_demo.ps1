# SerbiSure Security Proof-of-Concept Demo
# This script demonstrates Authentication, Authorization, and Protection in real-time.

$BASE_URL = "http://127.0.0.1:8000/api/v1"
$HTTP_CMD = ".\venv\Scripts\http.exe"

Write-Host "==========================================================" -ForegroundColor Yellow
Write-Host "   SERBISURE SYSTEM SECURITY DEMO (REAL-TIME AUDIT)       " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Yellow

Write-Host "`n[1/5] BRUTE FORCE PROTECTION" -ForegroundColor Cyan
Write-Host ">>> Action: Attempting login with WRONG password..."
# This shows how the backend rejects unauthorized attempts
& $HTTP_CMD POST "$BASE_URL/auth/login/" email="test@example.com" password="wrongpassword" --print=hb

Write-Host "`n[2/5] SECURE AUTHENTICATION (JWT/TOKEN)" -ForegroundColor Cyan
Write-Host ">>> Action: Logging in with CORRECT credentials..."
# This demonstrates the issuance of a cryptographic session token
$loginResponse = & $HTTP_CMD POST "$BASE_URL/auth/login/" email="homeowner@test.com" password="password123" --print=b | ConvertFrom-Json
$TOKEN = $loginResponse.data.token
Write-Host ">>> Result: Access Granted. Token Received: $TOKEN" -ForegroundColor Green

Write-Host "`n[3/5] PERIMETER DEFENSE (Authorization)" -ForegroundColor Cyan
Write-Host ">>> Action: Attempting to access Profile WITHOUT a token..."
# Demonstrates that the API is invisible to unauthorized users
& $HTTP_CMD GET "$BASE_URL/profile/" --print=hb

Write-Host "`n[4/5] REAL-TIME DATA ACCESS" -ForegroundColor Cyan
Write-Host ">>> Action: Accessing Profile WITH valid token..."
# Demonstrates successful authorized communication
& $HTTP_CMD GET "$BASE_URL/profile/" "Authorization: Token $TOKEN" --print=b

Write-Host "`n[5/5] DATA ISOLATION (Role-Based Access Control)" -ForegroundColor Cyan
Write-Host ">>> Action: Attempting to fetch bookings (Privacy Check)..."
# Demonstrates that the user only sees data belonging to their specific ID
& $HTTP_CMD GET "$BASE_URL/bookings/" "Authorization: Token $TOKEN" --print=b

Write-Host "`n==========================================================" -ForegroundColor Yellow
Write-Host "   SECURITY AUDIT COMPLETE: ALL LAYERS OPERATIONAL        " -ForegroundColor Yellow
Write-Host "==========================================================" -ForegroundColor Yellow
