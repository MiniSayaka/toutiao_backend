from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from confjg.config import get_db
from crud import user


# 整合 根据 Token 查询用户，返回用户
async def get_current_user(
        authorization: str = Header(..., alias="Authorization"),#从请求体里面获取"Authorization"这一栏的数据
        db: AsyncSession = Depends(get_db)
):
    # Bearer xxxxx
    # token = authorization.split(" ")[1]
    token = authorization.replace("Bearer ", "")
    current_user = await user.get_user_by_token(db, token)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="无效的令牌或已经过期的令牌")

    return current_user