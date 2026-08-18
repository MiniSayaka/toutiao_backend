from fastapi import APIRouter, Depends, Query, HTTPException,status
from crud import user
from sqlalchemy.ext.asyncio import AsyncSession
from confjg.config import get_db
from schemas.user import UserRequest, UserAuthResponse, UserInfoResponse,UserUpdateRequest,UserChangePasswordRequest
from utils.response import success_response
from utils.auth import get_current_user
from models.user import User

router = APIRouter(prefix="/api/user", tags=["user"])

@router.post("/register")
async def register(user_data: UserRequest, db: AsyncSession = Depends(get_db)):  # 用户信息 和 db
    # 注册逻辑：验证用户是否存在 -> 创建用户 → 生成 Token  → 响应结果
    existing_user = await user.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="用户已存在")
    new_user = await user.create_user(db, user_data)
    token = await user.create_token(db, new_user.id)
    # return {
    #   "code": 200,
    #   "message": "注册成功",
    #   "data": {
    #     "token": token,
    #     "userInfo": {
    #       "id": user.id,
    #       "username": user.username,
    #       "bio": user.bio,
    #       "avatar": user.avatar
    #     }
    #   }
    # }
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(new_user))
    return success_response(message="注册成功", data=response_data)


@router.post("/login")
async def login(user_data: UserRequest, db: AsyncSession = Depends(get_db)):
    # 登录逻辑：验证用户是否存在 -> 验证密码 -> 生成 Token  → 响应结果
    login_user = await user.authenticate_user(db, user_data.username, user_data.password)
    if not login_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
    token = await user.create_token(db, login_user.id)
    response_data = UserAuthResponse(token=token, user_info=UserInfoResponse.model_validate(login_user))
    return success_response(message="登录成功啦", data=response_data)


# 查Token查用户 → 封装crud → 功能整合成一个工具函数 → 路由导入使用: 依赖注入
@router.get("/info")
async def get_user_info(user: User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功", data=UserInfoResponse.model_validate(user))

# 修改用户信息：验证Token → 更新（用户输入数据 put 提交 → 请求体参数 → 定义Pydantic模型类） → 响应结果
# 参数：用户输入的 + 验证Token的 + db（调用更新的方法）
@router.put("/update")
async def update_user_info(user_data: UserUpdateRequest, current_user: User = Depends(get_current_user),
                           db: AsyncSession = Depends(get_db)):
    updated_user = await user.update_user(db, current_user.username, user_data)
    return success_response(message="更新用户信息成功", data=UserInfoResponse.model_validate(updated_user))


@router.put("/password")
async def update_password(
        password_data: UserChangePasswordRequest,
        current_user: User = Depends(get_current_user),
        db: AsyncSession = Depends(get_db)):
    success = await user.change_password(db, current_user, password_data.old_password, password_data.new_password)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="修改密码失败，请稍后再试")
    return success_response(message="修改密码成功")