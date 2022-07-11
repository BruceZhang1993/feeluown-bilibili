from typing import List, Optional

from feeluown.library import AbstractProvider, ProviderV2, ProviderFlags as Pf
from feeluown.media import Quality, Media
from feeluown.models import SearchType as FuoSearchType, ModelType

from fuo_bilibili import __identifier__, __alias__
from fuo_bilibili.api import BilibiliApi, SearchRequest, SearchType as BilibiliSearchType, VideoInfoRequest, \
    PlayUrlRequest, VideoQualityNum
from fuo_bilibili.api.schema.enums import VideoFnval
from fuo_bilibili.model import BSearchModel, BSongModel

SEARCH_TYPE_MAP = {
    FuoSearchType.vi: BilibiliSearchType.VIDEO,
    FuoSearchType.ar: BilibiliSearchType.BILI_USER,
    FuoSearchType.so: BilibiliSearchType.VIDEO,
}


class BilibiliProvider(AbstractProvider, ProviderV2):
    # noinspection PyPep8Naming
    class meta:
        identifier: str = __identifier__
        name: str = __alias__
        flags: dict = {
            ModelType.song: (Pf.model_v2 | Pf.get | Pf.multi_quality | Pf.lyric | Pf.mv),
        }

    def __init__(self):
        super(BilibiliProvider, self).__init__()
        self._api = BilibiliApi()

    def _format_search_request(self, keyword, type_) -> SearchRequest:
        btype = SEARCH_TYPE_MAP.get(type_)
        if btype is None:
            raise NotImplementedError
        return SearchRequest(search_type=btype, keyword=keyword)

    def search(self, keyword, type_, *args, **kwargs) -> Optional[BSearchModel]:
        request = self._format_search_request(keyword, type_)
        response = self._api.search(request)
        return BSearchModel.create_model(request, response)

    def song_get(self, identifier) -> BSongModel:
        response = self._api.video_get_info(VideoInfoRequest(bvid=identifier))
        return BSongModel.create_info_model(response)

    def song_get_lyric(self, song) -> None:
        return None

    def song_get_mv(self, song) -> None:
        return None

    def song_list_quality(self, song) -> List[Quality.Audio]:
        return [Quality.Audio.lq]

    def song_get_media(self, song, quality) -> Optional[Media]:
        info = self._api.video_get_info(VideoInfoRequest(bvid=song.identifier))
        response = self._api.video_get_url(PlayUrlRequest(
            bvid=song.identifier,
            qn=VideoQualityNum.q720,
            cid=info.data.cid,
            fnval=VideoFnval.DASH
        ))
        print(len(response.data.dash.audio))
        return Media(response.data.dash.audio[0].base_url, bitrate=320, format='mp3',
                     http_headers={'Referer': 'https://www.bilibili.com/'})

    @property
    def identifier(self):
        return __identifier__

    @property
    def name(self):
        return __alias__
