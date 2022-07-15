from typing import Type, Any, Optional, Union

from pydantic import BaseModel

from fuo_bilibili.api.schema.requests import BaseRequest, FavoriteListRequest, FavoriteInfoRequest, \
    FavoriteResourceRequest
from fuo_bilibili.api.schema.responses import BaseResponse, FavoriteListResponse, FavoriteInfoResponse, \
    FavoriteResourceResponse


class PlaylistMixin:
    """收藏夹接口"""
    APIX_BASE = 'https://api.bilibili.com/x'

    def get(self, url: str, param: Optional[BaseRequest], clazz: Union[Type[BaseResponse], Type[BaseModel], None]) -> Any:
        pass

    def post(self, url: str, param: Optional[BaseRequest], clazz: Type[BaseResponse], is_json=False, **kwargs) -> Any:
        pass

    def _dump_cookie_to_file(self):
        pass

    def favorite_list(self, request: FavoriteListRequest) -> FavoriteListResponse:
        url = f'{self.APIX_BASE}/v3/fav/folder/created/list-all'
        return self.get(url, request, FavoriteListResponse)

    def favorite_info(self, request: FavoriteInfoRequest) -> FavoriteInfoResponse:
        url = f'{self.APIX_BASE}/v3/fav/folder/info'
        return self.get(url, request, FavoriteInfoResponse)

    def favorite_resource(self, request: FavoriteResourceRequest) -> FavoriteResourceResponse:
        url = f'{self.APIX_BASE}/v3/fav/resource/list'
        return self.get(url, request, FavoriteResourceResponse)