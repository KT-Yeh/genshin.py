"""Hoyolab component."""
import typing

from genshin import types
from genshin.client import manager
from genshin.client.components import base
from genshin.models import hoyolab as models
from genshin.utility import genshin as genshin_utility

__all__ = ["HoyolabClient"]


class HoyolabClient(base.BaseClient):
    """Hoyolab component."""

    async def search_users(
        self,
        keyword: str,
        *,
        lang: typing.Optional[str] = None,
    ) -> typing.Sequence[models.SearchUser]:
        """Search hoyolab users."""
        data = await self.request_hoyolab(
            "community/search/wapi/search/user",
            lang=lang,
            params=dict(keyword=keyword, page_size=20),
        )
        return [models.SearchUser(**i["user"]) for i in data["list"]]

    async def get_recommended_users(self, *, limit: int = 200) -> typing.Sequence[models.SearchUser]:
        """Get a list of recommended active users."""
        data = await self.request_hoyolab(
            "community/user/wapi/recommendActive",
            params=dict(page_size=limit),
        )
        return [models.SearchUser(**i["user"]) for i in data["list"]]

    async def redeem_code(
        self,
        code: str,
        *,
        lang: typing.Optional[str] = None,
    ) -> None:
        """Redeems a gift code for the current genshin user."""
        if isinstance(self.cookie_manager, manager.RotatingCookieManager):
            raise RuntimeError("Cannot claim rewards with a multi-cookie manager.")

        uid = await self._get_uid(types.Game.GENSHIN)

        await self.request(
            "https://hk4e-api-os.mihoyo.com/common/apicdkey/api/webExchangeCdkey",
            params=dict(
                uid=uid,
                region=genshin_utility.recognize_genshin_server(uid),
                cdkey=code,
                game_biz="hk4e_global",
                lang=genshin_utility.create_short_lang_code(lang or self.lang),
            ),
        )