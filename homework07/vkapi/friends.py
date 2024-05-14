import dataclasses
import time
import typing as tp

from vkapi.config import VK_CONFIG
from vkapi.session import Session

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
    user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    s = Session(VK_CONFIG["domain"])

    if fields is not None:
        answer = FriendsResponse(0, [])
        for field in fields:
            resp = s.get(
                "friends.get",
                access_token=VK_CONFIG["access_token"],
                user_id=user_id,
                fields=field,
                count=count,
                offset=offset,
                v=VK_CONFIG["version"],
            ).json()

            if resp.get("response") == None:
                continue

            resp = resp["response"]
            count = resp["count"]
            items = resp["items"]
            if answer.count == 0:
                answer = FriendsResponse(count, [{} for i in range(count)])
            for i in range(count):
                answer.items[i][field] = items[i].get(field)
    else:
        resp = s.get(
            "friends.get",
            access_token=VK_CONFIG["access_token"],
            user_id=user_id,
            count=count,
            offset=offset,
            v=VK_CONFIG["version"],
        ).json()

        if resp.get("response") == None:
            return FriendsResponse(0, [])

        resp = resp["response"]
        count = resp["count"]
        items = resp["items"]
        answer = FriendsResponse(count, items)

    return answer


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
    source_uid: tp.Optional[int] = None,
    target_uid: tp.Optional[int] = None,
    target_uids: tp.Optional[tp.List[int]] = None,
    order: str = "",
    count: tp.Optional[int] = None,
    offset: int = 0,
    progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    if target_uids is None and target_uid is None:
        return []

    s = Session(VK_CONFIG["domain"])

    if target_uids is None:
        resp = s.get(
            "friends.getMutual",
            access_token=VK_CONFIG["access_token"],
            source_uid=source_uid,
            target_uid=target_uid,
            v=VK_CONFIG["version"],
        ).json()
        if resp.get("response") is None:
            print("Error in getting friends: ", resp["error"]["error_msg"])
            return []
        return resp["response"]
    else:
        if target_uid is not None:
            assert target_uids is not None
            target_uids.append(target_uid)
        n = len(target_uids)

        answer: list[MutualFriends] = []
        for offset in range(0, n, 100):
            if offset != 0 and offset % 300 == 0:
                time.sleep(1)
            resp = s.get(
                "friends.getMutual",
                access_token=VK_CONFIG["access_token"],
                source_uid=source_uid,
                offset=offset,  
                target_uids=str(target_uids[offset : min(offset + 100, n)])[1:-1].replace(" ", ""),
                v=VK_CONFIG["version"],
            ).json()
            if resp.get("response") is None:
                print("Error in getting friends: ", resp["error"]["error_msg"])
                return []
            answer += resp["response"]
        return answer

    # if source_uid != None:
    #     srcfrnds = set(get_friends(source_uid).items)
    # if target_uids == None:
    #     trgfrnds = set(get_friends(target_uid).items)
    #     mutual = srcfrnds.intersection(trgfrnds)
    #     return list(mutual)
    # else:
    #     ans = []
    #     for target in target_uids:
    #         trgfrnds = set(get_friends(target_uid).items)
    #         mutual = srcfrnds.intersection(trgfrnds)
    #         mt = MutualFriends(id=target, common_friends=list(mutual), common_count=len(mutual))
    #         ans.append(mt)
    #     return ans
