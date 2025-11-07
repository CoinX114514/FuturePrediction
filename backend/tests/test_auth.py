"""用户认证功能测试。

测试用户注册、登录、登出、Token 验证等功能。
"""

import pytest
from fastapi import status


class TestUserRegistration:
    """用户注册测试类。"""

    def test_register_with_phone(self, client):
        """测试使用手机号注册。"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "phone_number": "13800138001",
                "password": "password123",
                "nickname": "新用户",
            }
        )
        if response.status_code != status.HTTP_201_CREATED:
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.json()}")
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "token" in data
        assert data["user"]["phone_number"] == "13800138001"
        assert data["user"]["user_role"] == 1  # 默认为普通用户

    def test_register_with_email(self, client):
        """测试使用邮箱注册。"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "phone_number": "13800138002",
                "password": "password123",
                "email": "newuser@example.com",
                "nickname": "邮箱用户",
            }
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["user"]["email"] == "newuser@example.com"

    def test_register_duplicate_phone(self, client, test_user_normal):
        """测试重复手机号注册。"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "phone_number": test_user_normal.phone_number,
                "password": "password123",
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "已被注册" in response.json()["detail"]

    def test_register_invalid_phone(self, client):
        """测试无效手机号格式。"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "phone_number": "12345",  # 不是11位
                "password": "password123",
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_short_password(self, client):
        """测试密码太短。"""
        response = client.post(
            "/api/v1/auth/register",
            json={
                "phone_number": "13800138003",
                "password": "12345",  # 少于6位
            }
        )
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUserLogin:
    """用户登录测试类。"""

    def test_login_with_phone(self, client, test_user_normal):
        """测试使用手机号登录。"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "phone_number": test_user_normal.phone_number,
                "password": "test123456",
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "token" in data
        assert data["user"]["user_id"] == test_user_normal.user_id

    def test_login_with_email(self, client, test_user_normal):
        """测试使用邮箱登录。"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "email": test_user_normal.email,
                "password": "test123456",
            }
        )
        assert response.status_code == status.HTTP_200_OK
        assert "token" in response.json()

    def test_login_wrong_password(self, client, test_user_normal):
        """测试错误密码登录。"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "phone_number": test_user_normal.phone_number,
                "password": "wrongpassword",
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "密码错误" in response.json()["detail"]

    def test_login_nonexistent_user(self, client):
        """测试不存在的用户登录。"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "phone_number": "19999999999",
                "password": "password123",
            }
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_missing_credentials(self, client):
        """测试缺少凭证的登录。"""
        response = client.post(
            "/api/v1/auth/login",
            json={
                "password": "password123",
            }
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST


class TestGetCurrentUser:
    """获取当前用户信息测试类。"""

    def test_get_current_user(self, client, auth_token_normal, test_user_normal):
        """测试获取当前用户信息。"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": f"Bearer {auth_token_normal}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["user_id"] == test_user_normal.user_id
        assert data["phone_number"] == test_user_normal.phone_number

    def test_get_current_user_no_token(self, client):
        """测试无 Token 获取用户信息。"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_get_current_user_invalid_token(self, client):
        """测试无效 Token 获取用户信息。"""
        response = client.get(
            "/api/v1/auth/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestLogout:
    """用户登出测试类。"""

    def test_logout(self, client, auth_token_normal):
        """测试用户登出。"""
        response = client.post(
            "/api/v1/auth/logout",
            headers={"Authorization": f"Bearer {auth_token_normal}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert "登出成功" in response.json()["message"]

    def test_logout_no_token(self, client):
        """测试无 Token 登出。"""
        response = client.post("/api/v1/auth/logout")
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestPredictionLimit:
    """预测次数限制测试类。"""

    def test_get_prediction_limit_normal(self, client, auth_token_normal, test_user_normal):
        """测试普通用户获取预测限制。"""
        response = client.get(
            "/api/v1/auth/prediction-limit",
            headers={"Authorization": f"Bearer {auth_token_normal}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["limit"] == 5
        assert data["is_member"] is False
        assert data["remaining"] >= 0

    def test_get_prediction_limit_member(self, client, auth_token_member):
        """测试会员获取预测限制。"""
        response = client.get(
            "/api/v1/auth/prediction-limit",
            headers={"Authorization": f"Bearer {auth_token_member}"}
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["is_member"] is True
        assert data["limit"] == -1  # 无限
        assert data["remaining"] == -1  # 无限

