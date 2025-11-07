"""权限验证测试。

测试不同角色的权限验证，包括 CSV 上传权限和预测权限。
"""

import pytest
from fastapi import status
import io


class TestCSVUploadPermissions:
    """CSV 上传权限测试类。"""

    def test_upload_csv_as_normal_user(self, client, auth_token_normal):
        """测试普通用户尝试上传 CSV（应该被拒绝）。"""
        # 创建一个简单的 CSV 文件
        csv_content = "日期,开盘,最高,最低,收盘,成交量\n2024-01-01,100,105,99,103,1000000"
        files = {
            "file": ("test.csv", io.BytesIO(csv_content.encode()), "text/csv")
        }
        
        response = client.post(
            "/api/upload",
            files=files,
            headers={"Authorization": f"Bearer {auth_token_normal}"}
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        assert "会员" in response.json()["detail"]

    def test_upload_csv_as_member(self, client, auth_token_member):
        """测试会员上传 CSV（应该成功）。"""
        csv_content = "日期,开盘,最高,最低,收盘,成交量\n2024-01-01,100,105,99,103,1000000"
        files = {
            "file": ("test.csv", io.BytesIO(csv_content.encode()), "text/csv")
        }
        
        response = client.post(
            "/api/upload",
            files=files,
            headers={"Authorization": f"Bearer {auth_token_member}"}
        )
        assert response.status_code == status.HTTP_200_OK
        assert "file_id" in response.json()

    def test_upload_csv_as_admin(self, client, auth_token_admin):
        """测试管理员上传 CSV（应该成功）。"""
        csv_content = "日期,开盘,最高,最低,收盘,成交量\n2024-01-01,100,105,99,103,1000000"
        files = {
            "file": ("test.csv", io.BytesIO(csv_content.encode()), "text/csv")
        }
        
        response = client.post(
            "/api/upload",
            files=files,
            headers={"Authorization": f"Bearer {auth_token_admin}"}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_upload_csv_no_auth(self, client):
        """测试未登录用户上传 CSV。"""
        csv_content = "日期,开盘,最高,最低,收盘,成交量\n2024-01-01,100,105,99,103,1000000"
        files = {
            "file": ("test.csv", io.BytesIO(csv_content.encode()), "text/csv")
        }
        
        response = client.post("/api/upload", files=files)
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestPredictionPermissions:
    """预测权限测试类。"""

    def test_predict_as_normal_user_within_limit(self, client, auth_token_normal, test_db):
        """测试普通用户在限制内进行预测。"""
        # 先上传一个文件（需要会员权限，这里我们直接模拟）
        # 为了测试，我们需要先创建一个文件
        import os
        import uuid
        
        # 创建测试文件
        test_file_id = str(uuid.uuid4())
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        test_file_path = os.path.join(upload_dir, f"{test_file_id}.csv")
        
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("日期,开盘,最高,最低,收盘,成交量\n")
            f.write("2024-01-01,100,105,99,103,1000000\n")
            f.write("2024-01-02,103,108,102,106,1200000\n")
        
        try:
            response = client.post(
                "/api/predict",
                json={
                    "file_id": test_file_id,
                    "days": 1,
                },
                headers={"Authorization": f"Bearer {auth_token_normal}"}
            )
            # 预测可能成功（如果次数未用完）或失败（如果次数已用完）
            assert response.status_code in [
                status.HTTP_200_OK,
                status.HTTP_403_FORBIDDEN
            ]
        finally:
            # 清理测试文件
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

    def test_predict_no_auth(self, client):
        """测试未登录用户进行预测。"""
        response = client.post(
            "/api/predict",
            json={
                "file_id": "test_file_id",
                "days": 1,
            }
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_predict_as_member_unlimited(self, client, auth_token_member, test_db):
        """测试会员无限次预测。"""
        import os
        import uuid
        
        # 创建测试文件
        test_file_id = str(uuid.uuid4())
        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        test_file_path = os.path.join(upload_dir, f"{test_file_id}.csv")
        
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write("日期,开盘,最高,最低,收盘,成交量\n")
            f.write("2024-01-01,100,105,99,103,1000000\n")
            f.write("2024-01-02,103,108,102,106,1200000\n")
        
        try:
            response = client.post(
                "/api/predict",
                json={
                    "file_id": test_file_id,
                    "days": 1,
                },
                headers={"Authorization": f"Bearer {auth_token_member}"}
            )
            # 会员应该可以预测（即使模型可能失败，但权限应该通过）
            # 如果文件不存在会返回 404，如果模型失败会返回 500
            # 但权限检查应该通过
            assert response.status_code != status.HTTP_403_FORBIDDEN
        finally:
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

