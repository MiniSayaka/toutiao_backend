from passlib.context import CryptContext
#创建密码加密上下⽂
pwd_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
    )
#加密
def get_password_hash(password:str)->str:
    return pwd_context.hash(password)
#密码校验
def verify_password(plain_password:str,hashed_password:str)->bool:
    return pwd_context.verify(plain_password,hashed_password)

# 密码验证: verify 返回值是布尔型
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)