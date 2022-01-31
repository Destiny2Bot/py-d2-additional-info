from pydantic import BaseModel

from typing import List


class ModSocketMetadata(BaseModel):
    season: int
    """这允许我们按时间顺序对模组进行排序以达到 LO 的目的"""

    tag: str
    """我们使用这两个来匹配搜索过滤器"""

    compatibleTags: List[str]
    """我们使用这两个来匹配搜索过滤器"""

    socketTypeHash: int
    """# 一个道具插口的 socketTypeHash 用于查找 ModSocketMetadata"""

    plugCategoryHashes: List[int]
    """
    模组本身并不指向它们的兼容插槽，它们只是有一个plugCategoryHash。
    一个socket指向一个socketType，它指的是多个plugCategoryHashes
    所以这里是一种更直接的方法，如果你有一个plugCategoryHash，无需进行数据表查找就可以找到ModSocketMetadata
    """

    compatiblePlugCategoryHashes: List[int]
    """哈希用于在加载管理器中更快地查找，它们直接对应于在单个模块中找到的信息"""

    emptyModSocketHash: int
    """这有助于我们查找空白的模组内容，以获取其图标/名称"""
    

modMetadatasList = [
    {
        "season": 4,
        "tag": "最后一愿",
        "compatibleTags": [
            "最后一愿"
        ],
        "socketTypeHash": 1444083081,
        "plugCategoryHashes": [
            13646368
        ],
        "compatiblePlugCategoryHashes": [
            13646368
        ],
        "emptyModSocketHash": 1679876242
    },
    {
        "season": 4,
        "tag": "传承",
        "compatibleTags": [
            "战争思维",
            "充斥光能",
            "救赎花园",
            "最后一愿",
            "传承",
            "梦魇"
        ],
        "socketTypeHash": 1540673283,
        "plugCategoryHashes": [
            13646368,
            65589297,
            208760563,
            1081029832,
            2712224971
        ],
        "compatiblePlugCategoryHashes": [
            13646368,
            65589297,
            208760563,
            426869514,
            443647229,
            1081029832,
            1486918022,
            2149155760,
            2712224971
        ],
        "emptyModSocketHash": 3625698764
    },
    {
        "season": 5,
        "tag": "传承",
        "compatibleTags": [
            "战争思维",
            "充斥光能",
            "救赎花园",
            "最后一愿",
            "传承",
            "梦魇"
        ],
        "socketTypeHash": 3873071636,
        "plugCategoryHashes": [
            13646368,
            65589297,
            208760563,
            1081029832,
            2712224971
        ],
        "compatiblePlugCategoryHashes": [
            13646368,
            65589297,
            208760563,
            426869514,
            443647229,
            1081029832,
            1486918022,
            2712224971
        ],
        "emptyModSocketHash": 720857
    },
    {
        "season": 7,
        "tag": "传承",
        "compatibleTags": [
            "战争思维",
            "充斥光能",
            "救赎花园",
            "最后一愿",
            "传承",
            "梦魇"
        ],
        "socketTypeHash": 1430586844,
        "plugCategoryHashes": [
            13646368,
            65589297,
            208760563,
            1081029832,
            2712224971
        ],
        "compatiblePlugCategoryHashes": [
            13646368,
            65589297,
            208760563,
            426869514,
            443647229,
            1081029832,
            1486918022,
            2712224971
        ],
        "emptyModSocketHash": 4106547009
    },
    {
        "season": 8,
        "tag": "梦魇",
        "compatibleTags": [
            "梦魇"
        ],
        "socketTypeHash": 2701840022,
        "plugCategoryHashes": [
            1081029832
        ],
        "compatiblePlugCategoryHashes": [
            1081029832
        ],
        "emptyModSocketHash": 1180997867
    },
    {
        "season": 8,
        "tag": "传承",
        "compatibleTags": [
            "战争思维",
            "充斥光能",
            "救赎花园",
            "最后一愿",
            "传承",
            "梦魇"
        ],
        "socketTypeHash": 4127539203,
        "plugCategoryHashes": [
            13646368,
            65589297,
            208760563,
            1081029832,
            2712224971
        ],
        "compatiblePlugCategoryHashes": [
            13646368,
            65589297,
            208760563,
            426869514,
            443647229,
            1081029832,
            1486918022,
            2712224971
        ],
        "emptyModSocketHash": 2620967748
    },
    {
        "season": 9,
        "tag": "传承",
        "compatibleTags": [
            "战争思维",
            "充斥光能",
            "救赎花园",
            "最后一愿",
            "传承",
            "梦魇"
        ],
        "socketTypeHash": 1936582325,
        "plugCategoryHashes": [
            13646368,
            65589297,
            208760563,
            1081029832,
            2712224971
        ],
        "compatiblePlugCategoryHashes": [
            13646368,
            65589297,
            208760563,
            426869514,
            443647229,
            1081029832,
            1486918022,
            2712224971
        ],
        "emptyModSocketHash": 2357307006
    },
    {
        "season": 12,
        "tag": "战斗风格",
        "compatibleTags": [
            "元素井",
            "充斥光能",
            "战争思维",
            "战斗风格"
        ],
        "socketTypeHash": 2955889001,
        "plugCategoryHashes": [
            393461403
        ],
        "compatiblePlugCategoryHashes": [
            208760563,
            393461403,
            426869514,
            443647229,
            991069377
        ],
        "emptyModSocketHash": 2493100093
    }
]

modMetadatas = [ModSocketMetadata(**i) for i in modMetadatasList]