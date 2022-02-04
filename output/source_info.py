from pydantic import BaseModel

from typing import List


class D2SourceInfo(BaseModel):
    itemHashes: List[int]
    sourceHashes: List[int]
    searchString: List[str]

D2SourcesJson: dict[str, dict] = {
    "30周年": {
        "itemHashes": [],
        "sourceHashes": [
            675740011,
            860688654,
            1102533392,
            443340273,
            1394793197,
            2763252588,
            269962496,
            2882367429
        ],
        "searchString": []
    },
    "VEX进攻": {
        "itemHashes": [
            351285766,
            377757362,
            509561140,
            509561142,
            509561143,
            695795213,
            844110491,
            1137424312,
            1137424314,
            1137424315,
            1348357884,
            1584183805,
            1721943440,
            1721943441,
            1721943442,
            1855720513,
            1855720514,
            1855720515,
            2096778461,
            2096778462,
            2096778463,
            2468603405,
            2468603406,
            2468603407,
            2657028416,
            2687273800,
            2690973101,
            2690973102,
            2690973103,
            2742760292,
            2761292744,
            2815379657,
            2815379658,
            2815379659,
            2903026872,
            2903026873,
            2903026874,
            2942269704,
            2942269705,
            2942269707,
            3166926328,
            3166926330,
            3166926331,
            3192738009,
            3192738010,
            3192738011,
            3364258850,
            3680920565,
            3757338780,
            3757338782,
            3757338783,
            3911047865,
            4013678605,
            4026120124,
            4026120125,
            4026120127,
            4070722289,
            4078925540,
            4078925541,
            4078925542
        ],
        "sourceHashes": [
            4122810030
        ],
        "searchString": []
    },
    "世界吞噬者": {
        "itemHashes": [],
        "sourceHashes": [
            2937902448,
            4066007318
        ],
        "searchString": []
    },
    "传说记忆水晶": {
        "itemHashes": [],
        "sourceHashes": [
            3334812276
        ],
        "searchString": []
    },
    "先知": {
        "itemHashes": [],
        "sourceHashes": [
            2856954949
        ],
        "searchString": []
    },
    "全盛智谋": {
        "itemHashes": [
            2868525740,
            2868525741,
            2868525742,
            2868525743,
            3346345957,
            3382391785,
            3735277403,
            3808901541
        ],
        "sourceHashes": [
            1952675042
        ],
        "searchString": []
    },
    "凯德-6": {
        "itemHashes": [],
        "sourceHashes": [
            2206233229
        ],
        "searchString": []
    },
    "利维坦": {
        "itemHashes": [
            3580904580
        ],
        "sourceHashes": [
            2653618435,
            2937902448,
            2765304727,
            4066007318,
            4009509410
        ],
        "searchString": []
    },
    "前兆": {
        "itemHashes": [],
        "sourceHashes": [
            2745272818,
            3597879858,
            210885364
        ],
        "searchString": []
    },
    "卡鲁斯": {
        "itemHashes": [
            1661191192,
            2816212794,
            3580904580
        ],
        "sourceHashes": [
            4130543671
        ],
        "searchString": []
    },
    "命运内容保险库": {
        "itemHashes": [
            417164956,
            947448544,
            1661191192,
            1661191193,
            1661191194,
            1661191195,
            2027598066,
            2027598067,
            2557722678,
            2816212794,
            3176509806,
            3211806999,
            3580904580,
            3588934839,
            3650581584,
            3650581585,
            3650581586,
            3650581587,
            3650581588,
            3650581589,
            3841416152,
            3841416153,
            3841416154,
            3841416155,
            3875444086
        ],
        "sourceHashes": [
            4130543671
        ],
        "searchString": [
            "水星",
            "火星",
            "土卫六",
            "木卫一",
            "利维坦",
            "恶化规程",
            "黑色军火库",
            "奇珍异兽园",
            "世界吞噬者",
            "星之塔",
            "往日之苦",
            "忧愁王冠"
        ]
    },
    "土卫六": {
        "itemHashes": [],
        "sourceHashes": [
            194661944,
            354493557,
            3534706087,
            482012099,
            636474187
        ],
        "searchString": []
    },
    "圣人-14": {
        "itemHashes": [],
        "sourceHashes": [
            2607739079,
            4046490681,
            3404977524,
            4267157320
        ],
        "searchString": []
    },
    "地牢": {
        "itemHashes": [
            185321778,
            814876684,
            2844014413
        ],
        "sourceHashes": [
            506073192,
            2856954949,
            2745272818,
            3597879858,
            210885364,
            1745960977
        ],
        "searchString": [
            "破碎王座",
            "深渊",
            "预言",
            "前兆",
            "先知"
        ]
    },
    "地窖": {
        "itemHashes": [],
        "sourceHashes": [
            1405897559,
            1692165595,
            866530798
        ],
        "searchString": []
    },
    "奇珍异兽园": {
        "itemHashes": [
            1661191194,
            1661191195,
            3176509806,
            3841416152,
            3841416153,
            3841416154,
            3841416155,
            3875444086
        ],
        "sourceHashes": [
            4130543671,
            2511152325
        ],
        "searchString": []
    },
    "季票": {
        "itemHashes": [],
        "sourceHashes": [
            1593696611,
            2379344669,
            1763998430,
            1838401392
        ],
        "searchString": []
    },
    "密码": {
        "itemHashes": [],
        "sourceHashes": [
            4155903822
        ],
        "searchString": []
    },
    "巅峰": {
        "itemHashes": [],
        "sourceHashes": [
            2765304727,
            4066007318,
            2812190367
        ],
        "searchString": []
    },
    "幽梦": {
        "itemHashes": [
            185321779,
            3352019292
        ],
        "sourceHashes": [
            2559145507,
            3874934421
        ],
        "searchString": []
    },
    "异域密码": {
        "itemHashes": [],
        "sourceHashes": [
            4155903822
        ],
        "searchString": []
    },
    "往日之苦": {
        "itemHashes": [
            2557722678
        ],
        "sourceHashes": [
            4246883461,
            1483048674,
            2085016678
        ],
        "searchString": []
    },
    "忧愁王冠": {
        "itemHashes": [
            947448544,
            1661191193,
            2027598066,
            2027598067
        ],
        "sourceHashes": [
            2399751101,
            3147603678
        ],
        "searchString": []
    },
    "忽略": {
        "itemHashes": [],
        "sourceHashes": [
            3389857033,
            506073192,
            2353223954,
            1723452413,
            508245276,
            1995616326,
            1563875874,
            1957611613,
            1373504223,
            594760007,
            3528789901,
            1402439016
        ],
        "searchString": []
    },
    "恶化规程": {
        "itemHashes": [],
        "sourceHashes": [
            4137108180,
            3353456375
        ],
        "searchString": []
    },
    "战争圆桌": {
        "itemHashes": [],
        "sourceHashes": [
            4079816474
        ],
        "searchString": []
    },
    "战场": {
        "itemHashes": [],
        "sourceHashes": [
            3391325445
        ],
        "searchString": []
    },
    "战役": {
        "itemHashes": [],
        "sourceHashes": [
            2892963218,
            569214265,
            3532642391,
            918840100,
            2130345705,
            3083076965,
            1670837732,
            736336644,
            4290499613,
            3099553329,
            677167936,
            13912404,
            1281387702,
            2929562373,
            3704442923,
            1103518848,
            3126774631,
            4288102251,
            2308290458,
            2242939082,
            100617404,
            3936473457,
            3431853656,
            2744321951,
            1076222895,
            286427063,
            1118966764,
            2988465950,
            1701477406,
            2895784523
        ],
        "searchString": []
    },
    "打击": {
        "itemHashes": [
            274843196,
            1661191186,
            2523776412,
            2523776413,
            2588647361,
            2788911997,
            2788911998,
            2788911999,
            3215252549,
            4060882458
        ],
        "sourceHashes": [
            817015032,
            4263201695,
            2487203690,
            4208190159,
            2347293565,
            354493557,
            3067146211,
            1581680964,
            2717017239,
            1175566043,
            2926805810,
            1924238751,
            110159004,
            3874934421,
            3022766747,
            2851783112,
            2805208672,
            3964663093,
            2376909801
        ],
        "searchString": []
    },
    "拉斯普廷": {
        "itemHashes": [],
        "sourceHashes": [
            1497107113,
            1126234343,
            2230358252,
            3492941398,
            3937492340
        ],
        "searchString": []
    },
    "探险": {
        "itemHashes": [],
        "sourceHashes": [
            194661944,
            4214471686,
            1186140085,
            2392127416,
            2040548068,
            1527887247,
            80684972,
            790433146,
            482012099,
            1289998337,
            1067250718,
            3754173885,
            2096915131,
            783399508,
            3427537854,
            2553369674,
            1736997121,
            1861838843,
            2345202459,
            636474187
        ],
        "searchString": []
    },
    "接触": {
        "itemHashes": [],
        "sourceHashes": [
            2039343154
        ],
        "searchString": []
    },
    "新王": {
        "itemHashes": [],
        "sourceHashes": [
            1464399708
        ],
        "searchString": []
    },
    "日晷": {
        "itemHashes": [],
        "sourceHashes": [
            1618754228,
            2627087475
        ],
        "searchString": []
    },
    "日落": {
        "itemHashes": [],
        "sourceHashes": [
            817015032,
            4263201695,
            2487203690,
            4208190159,
            2347293565,
            354493557,
            3067146211,
            1581680964,
            2717017239,
            1175566043,
            2926805810,
            1924238751,
            110159004,
            3874934421,
            3022766747,
            2851783112,
            2805208672,
            3964663093,
            2376909801,
            1850609592,
            277706045,
            860666126,
            1618699950,
            1749037998,
            3528789901
        ],
        "searchString": []
    },
    "星之塔": {
        "itemHashes": [],
        "sourceHashes": [
            1675483099,
            2812190367
        ],
        "searchString": []
    },
    "智谋": {
        "itemHashes": [
            180108390,
            180108391,
            1335424933,
            1335424934,
            1335424935,
            1661191187,
            2224920148,
            2224920149,
            2394866220,
            2588647363,
            3217477988,
            4060882457
        ],
        "sourceHashes": [
            1952675042
        ],
        "searchString": []
    },
    "暴怒之子": {
        "itemHashes": [
            197764097,
            238284968,
            251310542,
            317220729,
            1148770067,
            1276513983,
            1458739906,
            2025716654,
            2055947316,
            2279193565,
            2453357042,
            2545401128,
            2776503072,
            3180809346,
            3351935136,
            3887272785,
            4079117607
        ],
        "sourceHashes": [
            3107094548,
            841568343
        ],
        "searchString": []
    },
    "最后一愿": {
        "itemHashes": [
            3668669364
        ],
        "sourceHashes": [
            2455011338
        ],
        "searchString": []
    },
    "月球": {
        "itemHashes": [],
        "sourceHashes": [],
        "searchString": []
    },
    "木卫一": {
        "itemHashes": [],
        "sourceHashes": [
            2392127416,
            2717017239,
            315474873,
            1067250718,
            3427537854,
            1832642406
        ],
        "searchString": []
    },
    "木卫二": {
        "itemHashes": [],
        "sourceHashes": [
            1148859274,
            3965815470,
            1492981395,
            2171520631,
            286427063,
            3125456997
        ],
        "searchString": []
    },
    "未来战争狂热者": {
        "itemHashes": [],
        "sourceHashes": [
            3569603185
        ],
        "searchString": []
    },
    "本影": {
        "itemHashes": [],
        "sourceHashes": [
            287889699,
            1286883820
        ],
        "searchString": []
    },
    "枪匠": {
        "itemHashes": [],
        "sourceHashes": [
            1433518193
        ],
        "searchString": []
    },
    "梦魇": {
        "itemHashes": [],
        "sourceHashes": [
            2778435282,
            550270332
        ],
        "searchString": []
    },
    "欧洲无人区": {
        "itemHashes": [],
        "sourceHashes": [
            4214471686,
            1527887247,
            1373723300,
            790433146,
            3754173885,
            2096915131,
            783399508,
            4292996207,
            1736997121,
            1861838843
        ],
        "searchString": []
    },
    "死亡轨道": {
        "itemHashes": [],
        "sourceHashes": [
            146504277
        ],
        "searchString": []
    },
    "水星": {
        "itemHashes": [],
        "sourceHashes": [
            3079246067,
            1618754228,
            4263201695,
            2487203690,
            1581680964,
            1175566043,
            1654120320,
            1400219831,
            1411886787,
            148542898,
            80684972,
            3964663093
        ],
        "searchString": []
    },
    "永恒之诗": {
        "itemHashes": [],
        "sourceHashes": [
            4036739795,
            860688654,
            269962496,
            2882367429
        ],
        "searchString": []
    },
    "沙克斯": {
        "itemHashes": [
            769099721,
            1230660649,
            1661191197,
            2414564781,
            2420153991,
            2588739576,
            2588739578,
            2588739579,
            2632846356,
            3928440584,
            3928440585,
            4060882456
        ],
        "sourceHashes": [
            897576623,
            2641169841,
            2055470113,
            1145551111,
            2658055900,
            745186842,
            1217831333,
            2669524419,
            3656787928,
            3226099405,
            929025440,
            2915991372,
            3020288414,
            2537301256,
            2821852478,
            598662729,
            1223492644,
            454115234,
            3348906688
        ],
        "searchString": []
    },
    "活动": {
        "itemHashes": [],
        "sourceHashes": [
            4069355515,
            2723305286,
            2230358252
        ],
        "searchString": [
            "曙光节",
            "血色浪漫",
            "至日",
            "英灵日",
            "狂欢",
            "游戏"
        ]
    },
    "浪客": {
        "itemHashes": [
            180108390,
            180108391,
            1335424933,
            1335424934,
            1335424935,
            1661191187,
            2224920148,
            2224920149,
            2394866220,
            2588647363,
            3217477988,
            4060882457
        ],
        "sourceHashes": [
            1952675042
        ],
        "searchString": []
    },
    "涅索斯": {
        "itemHashes": [],
        "sourceHashes": [
            1186140085,
            2040548068,
            1906492169,
            817015032,
            3067146211,
            3022766747,
            1289998337,
            164571094,
            2553369674,
            2345202459
        ],
        "searchString": []
    },
    "深渊": {
        "itemHashes": [],
        "sourceHashes": [
            1745960977
        ],
        "searchString": []
    },
    "深石地窖": {
        "itemHashes": [],
        "sourceHashes": [
            1405897559,
            1692165595,
            866530798
        ],
        "searchString": []
    },
    "火星": {
        "itemHashes": [],
        "sourceHashes": [
            4137108180,
            1036506031,
            2926805810,
            1924238751,
            2310754348,
            1299614150
        ],
        "searchString": []
    },
    "熔炉竞技场": {
        "itemHashes": [
            769099721,
            1230660649,
            1661191197,
            2414564781,
            2420153991,
            2588739576,
            2588739578,
            2588739579,
            2632846356,
            3928440584,
            3928440585,
            4060882456
        ],
        "sourceHashes": [
            897576623,
            2641169841,
            2055470113,
            1145551111,
            2658055900,
            745186842,
            1217831333,
            2669524419,
            3656787928,
            3226099405,
            929025440,
            2915991372,
            3020288414,
            2537301256,
            2821852478,
            598662729,
            1223492644,
            454115234,
            3348906688
        ],
        "searchString": []
    },
    "玻璃拱顶": {
        "itemHashes": [],
        "sourceHashes": [
            2065138144
        ],
        "searchString": []
    },
    "班西": {
        "itemHashes": [],
        "sourceHashes": [
            1433518193
        ],
        "searchString": []
    },
    "破碎王座": {
        "itemHashes": [
            185321778,
            814876684,
            2844014413
        ],
        "sourceHashes": [
            897576623,
            3389857033,
            3072862693,
            1607607347,
            3390015730,
            2653618435,
            2937902448,
            1675483099,
            2455011338,
            4246883461,
            2399751101,
            1491707941,
            506073192,
            1405897559,
            2065138144,
            675740011,
            4054646289,
            641018908,
            2187511136,
            3724111213,
            611838069,
            151416041,
            2011810450,
            2170269026,
            3845969330,
            1952675042,
            2892963218,
            569214265,
            194661944,
            4214471686,
            1186140085,
            2392127416,
            2040548068,
            1527887247,
            146504277,
            3569603185,
            1464399708,
            4036739795,
            860688654,
            2527168932,
            3075817319,
            1593696611,
            1600754038,
            3094114967,
            1373723300,
            1906492169,
            2559145507,
            1771326504,
            4130543671,
            1999000205,
            1148859274,
            3334812276,
            4140654910,
            3532642391,
            1102533392,
            443340273,
            2607739079,
            2353223954,
            1723452413,
            508245276,
            1995616326,
            139160732,
            1563875874,
            918840100,
            2203185162,
            1957611613,
            4155903822,
            2379344669,
            1866448829,
            2856954949,
            2745272818,
            164083100,
            1394793197,
            3147603678,
            3965815470,
            1483048674,
            3388021959,
            1492981395,
            2171520631,
            2763252588,
            2502262376,
            4166998204,
            2765304727,
            2641169841,
            817015032,
            3079246067,
            4137108180,
            1036506031,
            639650067,
            3212282221,
            269962496,
            4101102010,
            1286332045,
            3390164851,
            1373504223,
            2985242208,
            2968206374,
            2055470113,
            3589340943,
            4046490681,
            3471208558,
            1919933822,
            32323943,
            1692165595,
            3597879858,
            2040801502,
            3173463761,
            2797674516,
            2130345705,
            1788267693,
            1546689276,
            4079816474,
            1828592460,
            2939318890,
            2778435282,
            752988954,
            1145551111,
            2000002391,
            1593570812,
            3083076965,
            1670837732,
            736336644,
            4290499613,
            3099553329,
            677167936,
            13912404,
            1281387702,
            2929562373,
            3704442923,
            1103518848,
            681989555,
            3126774631,
            4288102251,
            2308290458,
            2242939082,
            100617404,
            3936473457,
            139599745,
            3543690049,
            2658055900,
            745186842,
            3966667255,
            1217831333,
            1027607603,
            2669524419,
            1312894505,
            594760007,
            3656787928,
            3226099405,
            1127923611,
            3494247523,
            2601524261,
            3422985544,
            3522070610,
            887452441,
            2364933290,
            2206233229,
            1397119901,
            3112857249,
            1360005982,
            772619302,
            3736521079,
            1462687159,
            3431853656,
            1412777465,
            1358645302,
            4069355515,
            2648408612,
            929025440,
            3390269646,
            3098906085,
            707740602,
            654652973,
            4066007318,
            4009509410,
            2085016678,
            2723305286,
            1618754228,
            3404977524,
            4290227252,
            2541753910,
            1596507419,
            4247521481,
            3764925750,
            1457456824,
            925197669,
            3257722699,
            266896577,
            2384327872,
            1465990789,
            2966694626,
            3047033583,
            1677921161,
            3952847349,
            930411416,
            4122810030,
            3190938946,
            4267157320,
            1497107113,
            1126234343,
            2039343154,
            2230358252,
            210885364,
            287889699,
            2694738712,
            1763998430,
            1054169368,
            557146120,
            4263201695,
            2487203690,
            4208190159,
            2347293565,
            354493557,
            3067146211,
            1581680964,
            2717017239,
            1175566043,
            2926805810,
            1924238751,
            110159004,
            3874934421,
            3022766747,
            2851783112,
            2805208672,
            351235593,
            1216155659,
            1564061133,
            539840256,
            2335095658,
            1433518193,
            2967385539,
            3534706087,
            315474873,
            1654120320,
            2744321951,
            1400219831,
            1411886787,
            148542898,
            1076222895,
            80684972,
            2310754348,
            3353456375,
            550270332,
            1253026984,
            1745960977,
            286427063,
            1838401392,
            3693722471,
            1118966764,
            2915991372,
            3020288414,
            2843045413,
            186854335,
            561111210,
            2520862847,
            2812190367,
            1743434737,
            2882367429,
            412991783,
            2988465950,
            798957490,
            96303009,
            3964663093,
            439994003,
            2376909801,
            1828622510,
            1286883820,
            3107094548,
            3125456997,
            510530151,
            1299614150,
            948753311,
            866530798,
            2653840925,
            3100439379,
            1244908294,
            2511152325,
            3512613235,
            1850609592,
            277706045,
            2537301256,
            841568343,
            2986841134,
            1701477406,
            2062058385,
            860666126,
            1618699950,
            2627087475,
            571102497,
            3492941398,
            790433146,
            2857787138,
            2821852478,
            3391325445,
            2883838366,
            3937492340,
            1749037998,
            3528789901,
            482012099,
            1289998337,
            594786771,
            598662729,
            1067250718,
            3754173885,
            2096915131,
            1223492644,
            1144274899,
            783399508,
            3427537854,
            2895784523,
            164571094,
            288436121,
            1162859311,
            4292996207,
            2553369674,
            1736997121,
            1861838843,
            1832642406,
            454115234,
            2345202459,
            2317365255,
            3348906688,
            636474187,
            1402439016
        ],
        "searchString": []
    },
    "突袭": {
        "itemHashes": [
            947448544,
            1661191193,
            2027598066,
            2557722678,
            3580904580,
            3668669364,
            4103414242
        ],
        "sourceHashes": [
            2653618435,
            2937902448,
            1675483099,
            2455011338,
            4246883461,
            2399751101,
            1491707941,
            1405897559,
            2065138144,
            3147603678,
            1483048674,
            2765304727,
            1692165595,
            3390269646,
            3098906085,
            707740602,
            654652973,
            4066007318,
            4009509410,
            2085016678,
            2723305286,
            557146120,
            2812190367,
            2882367429,
            866530798
        ],
        "searchString": [
            "忧愁王冠",
            "深石地窖",
            "世界吞噬者",
            "花园",
            "最后一愿",
            "利维坦",
            "往日之苦",
            "星之塔",
            "玻璃拱顶"
        ]
    },
    "纷争": {
        "itemHashes": [
            1226584228,
            1226584229,
            4085986809
        ],
        "sourceHashes": [
            1771326504,
            4140654910,
            110159004,
            2805208672,
            798957490
        ],
        "searchString": []
    },
    "罗盘": {
        "itemHashes": [],
        "sourceHashes": [
            2939318890
        ],
        "searchString": []
    },
    "船匠": {
        "itemHashes": [],
        "sourceHashes": [
            96303009
        ],
        "searchString": []
    },
    "艾可拉": {
        "itemHashes": [],
        "sourceHashes": [
            3075817319
        ],
        "searchString": []
    },
    "艾达": {
        "itemHashes": [
            417164956,
            3211806999,
            3588934839,
            3650581584,
            3650581585,
            3650581586,
            3650581587,
            3650581588,
            3650581589
        ],
        "sourceHashes": [
            4101102010,
            1286332045,
            3390164851,
            1546689276,
            4290227252,
            2541753910,
            1596507419,
            4247521481,
            3764925750,
            1457456824,
            925197669,
            3257722699,
            266896577,
            2384327872,
            1465990789,
            2966694626,
            3047033583,
            439994003,
            948753311,
            2062058385
        ],
        "searchString": []
    },
    "花园": {
        "itemHashes": [
            4103414242
        ],
        "sourceHashes": [
            1491707941
        ],
        "searchString": []
    },
    "萨瓦拉": {
        "itemHashes": [
            274843196,
            1661191186,
            2523776412,
            2523776413,
            2588647361,
            2788911997,
            2788911998,
            2788911999,
            3215252549,
            4060882458
        ],
        "sourceHashes": [
            817015032,
            4263201695,
            2487203690,
            4208190159,
            2347293565,
            354493557,
            3067146211,
            1581680964,
            2717017239,
            1175566043,
            2926805810,
            1924238751,
            110159004,
            3874934421,
            3022766747,
            2851783112,
            2805208672,
            3964663093,
            2376909801
        ],
        "searchString": []
    },
    "试炼": {
        "itemHashes": [
            1983519830,
            2071635914,
            2071635915
        ],
        "sourceHashes": [
            1607607347,
            3390015730,
            3471208558,
            752988954,
            139599745,
            3543690049,
            550270332,
            2653840925,
            2857787138
        ],
        "searchString": []
    },
    "豪华": {
        "itemHashes": [],
        "sourceHashes": [
            1866448829,
            4166998204,
            639650067,
            3212282221,
            2985242208,
            2968206374,
            3173463761,
            1412777465,
            1358645302,
            4069355515,
            1743434737
        ],
        "searchString": []
    },
    "遗失区域": {
        "itemHashes": [],
        "sourceHashes": [
            2203185162
        ],
        "searchString": []
    },
    "铁旗": {
        "itemHashes": [
            231533811,
            1162929425,
            1448664466,
            1448664467,
            1661191199,
            1987234560,
            2298896093,
            2448092902
        ],
        "sourceHashes": [
            3072862693,
            3966667255,
            1027607603,
            1312894505,
            2648408612,
            561111210,
            2520862847,
            1828622510
        ],
        "searchString": []
    },
    "限定": {
        "itemHashes": [],
        "sourceHashes": [
            1866448829,
            4166998204,
            639650067,
            3212282221,
            2985242208,
            2968206374,
            3173463761,
            1412777465,
            1358645302,
            4069355515,
            1743434737
        ],
        "searchString": []
    },
    "预言": {
        "itemHashes": [],
        "sourceHashes": [
            506073192
        ],
        "searchString": []
    },
    "魔眼": {
        "itemHashes": [],
        "sourceHashes": [
            1600754038,
            139160732,
            2040801502,
            1828592460,
            2694738712,
            2967385539,
            277706045
        ],
        "searchString": []
    },
    "黑色军火库": {
        "itemHashes": [
            417164956,
            3211806999,
            3588934839,
            3650581584,
            3650581585,
            3650581586,
            3650581587,
            3650581588,
            3650581589
        ],
        "sourceHashes": [
            4101102010,
            1286332045,
            3390164851,
            1546689276,
            4290227252,
            2541753910,
            1596507419,
            4247521481,
            3764925750,
            1457456824,
            925197669,
            3257722699,
            266896577,
            2384327872,
            1465990789,
            2966694626,
            3047033583,
            439994003,
            948753311,
            2062058385
        ],
        "searchString": []
    }
}

D2Sources: dict[str, D2SourceInfo] = {
k: D2SourceInfo.parse_obj(v) for k, v in D2SourcesJson.items()
}