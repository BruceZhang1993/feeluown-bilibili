from typing import List, Union

from feeluown.library import SongModel, BriefArtistModel, SongProtocol
from feeluown.models import SearchModel, ModelExistence

from fuo_bilibili import __identifier__
from fuo_bilibili.api import SearchType
from fuo_bilibili.api.schema.requests import SearchRequest
from fuo_bilibili.api.schema.responses import SearchResponse, SearchResultVideo, VideoInfoResponse

PROVIDER_ID = __identifier__


class BSongModel(SongModel):
    source: str = PROVIDER_ID

    @classmethod
    def create_model(cls, result: SearchResultVideo) -> 'BSongModel':
        return cls(
            identifier=result.bvid,
            album=None,
            title=result.title,
            artists=[BriefArtistModel(
                source=PROVIDER_ID,
                identifier=result.mid,
                name=result.author,
            )],
            duration=result.duration.total_seconds() * 1000,
        )

    @classmethod
    def create_info_model(cls, response: VideoInfoResponse) -> 'BSongModel':
        result = response.data
        return cls(
            identifier=result.bvid,
            album=None,
            title=result.title,
            artists=[BriefArtistModel(
                source=PROVIDER_ID,
                identifier=result.owner.mid,
                name=result.owner.name,
            )],
            duration=result.duration.total_seconds() * 1000,
            exists=ModelExistence.yes
        )


class BSearchModel(SearchModel):
    PROVIDER_ID = __identifier__

    # ['q', 'songs', 'playlists', 'artists', 'albums', 'videos']
    q: str
    songs = List[BSongModel]

    @classmethod
    def create_model(cls, request: SearchRequest, response: SearchResponse):
        songs = None
        match request.search_type:
            case SearchType.VIDEO:
                songs = list(map(lambda r: BSongModel.create_model(r), response.data.result))
        return cls(
            source=PROVIDER_ID,
            q=request.keyword,
            songs=songs
        )