#!/bin/bash
echo "=== 测试登录接口 ==="
echo ""
echo "1. 测试通过 vite 代理 (localhost:5175/api):"
curl -s -X POST http://localhost:5175/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"13800000001","password":"123456"}' | python3 -m json.tool
echo ""
echo "2. 测试直接访问后端 (localhost:8000/api):"
curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:5175" \
  -d '{"phone_number":"13800000001","password":"123456"}' | python3 -m json.tool
echo ""
echo "3. 测试错误的密码:"
curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"13800000001","password":"wrong"}' | python3 -m json.tool
echo ""
echo "4. 测试不存在的用户:"
curl -s -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"99999999999","password":"123456"}' | python3 -m json.tool
