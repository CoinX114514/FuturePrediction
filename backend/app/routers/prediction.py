"""预测路由模块。

处理价格趋势预测请求。
"""

from typing import Optional

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.model_inference import ModelInference
from app.services.csv_parser import CSVParser
from app.services.auth_service import AuthService
from app.middleware.auth import get_current_user
from app.database.connection import get_db
from app.database.models import User
from sqlalchemy.orm import Session

router = APIRouter()


class PredictionRequest(BaseModel):
    """预测请求数据模型。

    Attributes:
        file_id: 已上传文件的唯一标识符。
        days: 预测未来天数，默认为 1（预测明天的趋势）。
    """

    file_id: str
    days: Optional[int] = 1


@router.post("/predict")
async def predict_trend(
    request: PredictionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """执行价格趋势预测。

    使用预训练的 Kronos 模型对上传的 OHLCV 数据进行预测。

    注意：普通用户每日限制 5 次，会员无限次。

    Args:
        request: 预测请求对象，包含文件 ID 和预测天数。
        current_user: 当前登录用户（通过依赖注入获取）。
        db: 数据库会话。

    Returns:
        JSONResponse: 包含预测结果的响应。
            - predictions: 预测结果列表
            - confidence: 置信度
            - trend: 趋势方向（上涨/下跌/震荡）
            - metadata: 元数据信息

    Raises:
        HTTPException: 当权限不足、文件不存在或预测失败时抛出。
    """
    try:
        # 检查预测权限和次数限制
        auth_service = AuthService(db)
        limit_info = auth_service.check_prediction_limit(current_user.user_id)

        if not limit_info["allowed"]:
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "预测次数已达上限",
                    "message": f"您今日已使用 {current_user.prediction_count} 次预测，"
                              f"每日限制 {limit_info['limit']} 次。"
                              "升级为会员可享受无限次预测。",
                    "remaining": limit_info["remaining"],
                    "limit": limit_info["limit"],
                },
            )
        # 加载模型推理服务
        model_service = ModelInference()

        # 加载文件数据
        import os
        file_path = os.path.join("uploads", f"{request.file_id}.csv")
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail="文件不存在，请先上传文件",
            )

        # 读取并解析 CSV
        parser = CSVParser()
        with open(file_path, "rb") as f:
            contents = f.read()
        df = parser.parse_csv(contents)

        # 执行预测
        predictions = model_service.predict(
            data=df,
            days=request.days,
        )

        # 增加用户的预测次数计数
        auth_service.increment_prediction_count(current_user.user_id)

        # 更新限制信息
        limit_info = auth_service.check_prediction_limit(current_user.user_id)

        return JSONResponse(
            content={
                "predictions": predictions["predictions"],
                "confidence": predictions.get("confidence", 0.0),
                "trend": predictions.get("trend", "未知"),
                "metadata": {
                    "file_id": request.file_id,
                    "prediction_days": request.days,
                    "data_points": len(df),
                    "user_id": current_user.user_id,
                },
                "prediction_limit": {
                    "remaining": limit_info["remaining"],
                    "limit": limit_info["limit"],
                    "is_member": limit_info["is_member"],
                },
                "message": "预测完成",
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"预测失败: {str(e)}",
        )


@router.get("/predict/status")
async def get_prediction_status():
    """获取预测服务状态。

    Returns:
        dict: 包含模型加载状态和可用性的信息。
    """
    try:
        model_service = ModelInference()
        status = model_service.get_status()
        return {
            "status": "ready" if status["loaded"] else "not_ready",
            "model_name": "Kronos",
            "message": "模型已加载" if status["loaded"] else "模型未加载",
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"状态检查失败: {str(e)}",
        }

