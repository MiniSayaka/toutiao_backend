from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from schemas.base import NewsItemBase


class HistoryAddRequest(BaseModel):
    """
    添加历史记录请求
    """
    news_id: int = Field(..., alias="newsId")


class HistoryAddResponse(BaseModel):
    """
    添加历史记录响应
    """
    id: int
    news_id: int = Field(..., alias="newsId")
    view_time: datetime = Field(..., alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )

class HistoryNewsItemResponse(NewsItemBase):
    """
    浏览历史列表中的新闻项响应
    """
    history_id: int = Field(alias="historyId")
    view_time: datetime = Field(alias="viewTime")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True)


class HistoryListResponse(BaseModel):
    list: list[HistoryNewsItemResponse]
    total: int
    has_more: bool = Field(alias="hasMore")

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True
    )