# 新闻资讯头条（toutiao_backend）

一个前后端分离的新闻资讯类应用。后端基于 **FastAPI**，前端基于 **Vue 3 + Vite**，提供新闻浏览、分类、用户注册登录、收藏、浏览历史、AI 问答等功能。

## 技术栈

**后端**

| 技术 | 用途 |
| --- | --- |
| FastAPI | Web 框架 |
| SQLAlchemy 2.0（async） | 异步 ORM |
| aiomysql | MySQL 异步驱动 |
| Pydantic v2 | 数据校验与序列化 |
| passlib[bcrypt] | 密码加密 |
| Uvicorn | ASGI 服务器 |

**前端**（`xwzx-news/`）

| 技术 | 用途 |
| --- | --- |
| Vue 3（Composition API） | 前端框架 |
| Vite | 构建工具 |
| Vant 4 | 移动端 UI 组件库 |
| Pinia | 状态管理 |
| Vue Router | 路由 |
| vue-i18n | 国际化（中/英） |
| marked + DOMPurify | Markdown 渲染与 XSS 防护 |
| axios | HTTP 请求 |

## 项目结构

```
toutiao_backend/
├── main.py                 # FastAPI 入口，注册路由与 CORS
├── confjg/
│   └── config.py           # 数据库连接、异步引擎、会话工厂
├── models/                 # SQLAlchemy ORM 模型
│   ├── newsmodel.py        # 新闻分类、新闻
│   ├── user.py             # 用户、用户令牌
│   ├── favorite.py         # 收藏
│   └── history.py          # 浏览历史
├── schemas/                # Pydantic 请求/响应模型
├── crud/                   # 数据访问层
├── routers/                # API 路由层
├── utils/                  # 认证、密码加密、统一响应、异常处理
└── xwzx-news/              # 前端项目（Vue 3）
    └── src/
        ├── views/          # 页面组件
        ├── components/     # 公共组件
        ├── router/         # 路由配置
        ├── store/          # Pinia 状态
        ├── config/         # API 配置
        └── i18n/           # 多语言
```

## 数据库设计

数据库：`news_app`（MySQL）

| 表 | 说明 |
| --- | --- |
| `news_category` | 新闻分类（id、name、sort_order） |
| `news` | 新闻（标题、简介、内容、封面图、作者、分类、浏览量、发布时间） |
| `user` | 用户（用户名、密码加密存储、昵称、头像、性别、简介、手机号） |
| `user_token` | 用户令牌（UUID token、过期时间），用于接口鉴权 |
| `favorite` | 收藏（用户 + 新闻唯一约束，防止重复收藏） |
| `history` | 浏览历史（用户、新闻、浏览时间） |

## API 接口

统一前缀 `/api`，鉴权接口需在请求头携带 `Authorization: Bearer <token>`。

| 模块 | 方法 | 路径 | 说明 | 鉴权 |
| --- | --- | --- | --- | --- |
| 新闻 | GET | `/api/news/categories` | 获取分类列表 | 否 |
| 新闻 | GET | `/api/news/list` | 分页获取新闻列表 | 否 |
| 新闻 | GET | `/api/news/detail` | 获取新闻详情 | 否 |
| 用户 | POST | `/api/user/register` | 注册 | 否 |
| 用户 | POST | `/api/user/login` | 登录（返回 token） | 否 |
| 用户 | GET | `/api/user/info` | 获取用户信息 | 是 |
| 用户 | PUT | `/api/user/update` | 修改用户信息 | 是 |
| 用户 | PUT | `/api/user/password` | 修改密码 | 是 |
| 收藏 | GET | `/api/favorite/check` | 查询是否已收藏 | 是 |
| 收藏 | POST | `/api/favorite/add` | 添加收藏 | 是 |
| 收藏 | DELETE | `/api/favorite/remove` | 取消收藏 | 是 |
| 收藏 | GET | `/api/favorite/list` | 收藏列表 | 是 |
| 收藏 | DELETE | `/api/favorite/clear` | 清空收藏 | 是 |
| 历史 | POST | `/api/history/add` | 添加浏览记录 | 是 |
| 历史 | GET | `/api/history/list` | 浏览历史列表 | 是 |
| 历史 | DELETE | `/api/history/delete/{history_id}` | 删除单条历史 | 是 |
| 历史 | DELETE | `/api/history/clear` | 清空历史 | 是 |

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+

### 1. 后端启动

```bash
# 创建并激活虚拟环境
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
# source .venv/bin/activate

# 安装依赖
pip install fastapi "uvicorn[standard]" "sqlalchemy[asyncio]" aiomysql pydantic "passlib[bcrypt]"

# 修改数据库连接（confjg/config.py）
# ASYNC_DATABASE_URL = "mysql+aiomysql://<用户名>:<密码>@localhost:3306/news_app?charset=utf8mb4"

# 启动服务（默认 http://127.0.0.1:8000）
uvicorn main:app --reload
```

> 启动前请先在 MySQL 中创建 `news_app` 数据库，并按 `models/` 中的模型定义建表。

### 2. 前端启动

```bash
cd xwzx-news

# 安装依赖
npm install

# 启动开发服务器（默认 http://localhost:5173）
npm run dev
```

前端通过 `src/config/api.js` 中的 `baseURL`（默认 `http://127.0.0.1:8000`）访问后端。

## 注意事项

- **数据库密码**：`confjg/config.py` 中当前明文写入了数据库密码，建议改用环境变量或 `.env` 文件管理。
- **AI API Key**：`xwzx-news/src/config/api.js` 中硬编码了阿里云 DashScope 的 API Key，任何人从前端源码即可提取。生产环境应将 AI 请求改为后端代理，并把密钥放在服务端环境变量中。
- **CORS**：`main.py` 中开发阶段 `allow_origins=["*"]`，生产环境应指定具体域名。
