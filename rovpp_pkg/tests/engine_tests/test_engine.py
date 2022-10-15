from pathlib import Path

import pytest

from bgp_simulator_pkg import EngineTester
from bgp_simulator_pkg import EngineTestConfig

from .engine_test_configs import Config035
from .engine_test_configs import Config036
from .engine_test_configs import Config037
from .engine_test_configs import Config038
from .engine_test_configs import Config039
from .engine_test_configs import Config040
from .engine_test_configs import Config041
from .engine_test_configs import Config042
from .engine_test_configs import Config043
from .engine_test_configs import Config044
from .engine_test_configs import Config045
from .engine_test_configs import Config046
from .engine_test_configs import Config047
from .engine_test_configs import Config048
from .engine_test_configs import Config049
from .engine_test_configs import Config050
from .engine_test_configs import Config051
from .engine_test_configs import Config052
from .engine_test_configs import Config053
from .engine_test_configs import Config054
from .engine_test_configs import Config055
from .engine_test_configs import Config056
from .engine_test_configs import Config057
from .engine_test_configs import Config058
from .engine_test_configs import Config059
from .engine_test_configs import Config060
from .engine_test_configs import Config061
from .engine_test_configs import Config062
from .engine_test_configs import Config063
from .engine_test_configs import Config064
from .engine_test_configs import Config065
from .engine_test_configs import Config066
from .engine_test_configs import Config067
from .engine_test_configs import Config068
from .engine_test_configs import Config069
from .engine_test_configs import Config070
from .engine_test_configs import Config071
from .engine_test_configs import Config072
from .engine_test_configs import Config073
from .engine_test_configs import Config074
from .engine_test_configs import Config075
from .engine_test_configs import Config076
from .engine_test_configs import Config077
from .engine_test_configs import Config078
from .engine_test_configs import Config079
from .engine_test_configs import Config080
from .engine_test_configs import Config081
from .engine_test_configs import Config082
from .engine_test_configs import Config083
from .engine_test_configs import Config084
from .engine_test_configs import Config085
from .engine_test_configs import Config086
from .engine_test_configs import Config087
from .engine_test_configs import Config088
from .engine_test_configs import Config089
from .engine_test_configs import Config090
from .engine_test_configs import Config091
from .engine_test_configs import Config092
from .engine_test_configs import Config093
from .engine_test_configs import Config094
from .engine_test_configs import Config095
from .engine_test_configs import Config096
from .engine_test_configs import Config097
from .engine_test_configs import Config098
from .engine_test_configs import Config099
from .engine_test_configs import Config100
from .engine_test_configs import Config101
from .engine_test_configs import Config102
from .engine_test_configs import Config103
from .engine_test_configs import Config104
from .engine_test_configs import Config105
from .engine_test_configs import Config106
from .engine_test_configs import Config107
from .engine_test_configs import Config108
from .engine_test_configs import Config109
from .engine_test_configs import Config110
# from .engine_test_configs import Config111
# from .engine_test_configs import Config112
# from .engine_test_configs import Config113
# from .engine_test_configs import Config114
# from .engine_test_configs import Config115
# from .engine_test_configs import Config116
# from .engine_test_configs import Config117
# from .engine_test_configs import Config118
# from .engine_test_configs import Config119
# from .engine_test_configs import Config120
# from .engine_test_configs import Config121
# from .engine_test_configs import Config122
# from .engine_test_configs import Config123
# from .engine_test_configs import Config124
# from .engine_test_configs import Config125
# from .engine_test_configs import Config126
from .engine_test_configs import Config127
from .engine_test_configs import Config128
from .engine_test_configs import Config129
from .engine_test_configs import Config130
# from .engine_test_configs import Config131
# from .engine_test_configs import Config132
# from .engine_test_configs import Config133
# from .engine_test_configs import Config134
from .engine_test_configs import Config135
from .engine_test_configs import Config136
from .engine_test_configs import Config137
from .engine_test_configs import Config138
# from .engine_test_configs import Config139
# from .engine_test_configs import Config140
# from .engine_test_configs import Config141
# from .engine_test_configs import Config142
# from .engine_test_configs import Config143
# from .engine_test_configs import Config144
# from .engine_test_configs import Config145
# from .engine_test_configs import Config146
# from .engine_test_configs import Config147
# from .engine_test_configs import Config148
# from .engine_test_configs import Config149
# from .engine_test_configs import Config150
# from .engine_test_configs import Config151
# from .engine_test_configs import Config152
# from .engine_test_configs import Config153
# from .engine_test_configs import Config154
# from .engine_test_configs import Config155
# from .engine_test_configs import Config156
# from .engine_test_configs import Config157
# from .engine_test_configs import Config158
from .engine_test_configs import Config159
from .engine_test_configs import Config160
from .engine_test_configs import Config161
from .engine_test_configs import Config162
# from .engine_test_configs import Config163
# from .engine_test_configs import Config164
# from .engine_test_configs import Config165
# from .engine_test_configs import Config166
# from .engine_test_configs import Config167
# from .engine_test_configs import Config168
# from .engine_test_configs import Config169
# from .engine_test_configs import Config170
# from .engine_test_configs import Config171
# from .engine_test_configs import Config172
# from .engine_test_configs import Config173
# from .engine_test_configs import Config174
# from .engine_test_configs import Config175
# from .engine_test_configs import Config176
# from .engine_test_configs import Config177
# from .engine_test_configs import Config178
# from .engine_test_configs import Config179
# from .engine_test_configs import Config180
# from .engine_test_configs import Config181
# from .engine_test_configs import Config182
# from .engine_test_configs import Config183
# from .engine_test_configs import Config184
# from .engine_test_configs import Config185
# from .engine_test_configs import Config186
# from .engine_test_configs import Config187
# from .engine_test_configs import Config188
# from .engine_test_configs import Config189
# from .engine_test_configs import Config190
# from .engine_test_configs import Config191
# from .engine_test_configs import Config192
# from .engine_test_configs import Config193
# from .engine_test_configs import Config194
from .engine_test_configs import Config195
from .engine_test_configs import Config196
from .engine_test_configs import Config197
from .engine_test_configs import Config198
from .engine_test_configs import Config199
from .engine_test_configs import Config200
from .engine_test_configs import Config201
from .engine_test_configs import Config202
from .engine_test_configs import Config203
from .engine_test_configs import Config204
from .engine_test_configs import Config205
from .engine_test_configs import Config206
from .engine_test_configs import Config207
from .engine_test_configs import Config208
from .engine_test_configs import Config209
from .engine_test_configs import Config210
from .engine_test_configs import Config211
from .engine_test_configs import Config212
from .engine_test_configs import Config213
from .engine_test_configs import Config214
from .engine_test_configs import Config215
from .engine_test_configs import Config216
from .engine_test_configs import Config217
from .engine_test_configs import Config218


@pytest.mark.engine
class TestEngine:
    """Performs a system test on the engine

    See README for in depth details
    """

    @pytest.mark.parametrize("conf",
                             [
                              Config035,
                              Config036,
                              Config037,
                              Config038,
                              Config039,
                              Config040,
                              Config041,
                              Config042,
                              Config043,
                              Config044,
                              Config045,
                              Config046,
                              Config047,
                              Config048,
                              Config049,
                              Config050,
                              Config051,
                              Config052,
                              Config053,
                              Config054,
                              Config055,
                              Config056,
                              Config057,
                              Config058,
                              Config059,
                              Config060,
                              Config061,
                              Config062,
                              Config063,
                              Config064,
                              Config065,
                              Config066,
                              Config067,
                              Config068,
                              Config069,
                              Config070,
                              Config071,
                              Config072,
                              Config073,
                              Config074,
                              Config075,
                              Config076,
                              Config077,
                              Config078,
                              Config079,
                              Config080,
                              Config081,
                              Config082,
                              Config083,
                              Config084,
                              Config085,
                              Config086,
                              Config087,
                              Config088,
                              Config089,
                              Config090,
                              Config091,
                              Config092,
                              Config093,
                              Config094,
                              Config095,
                              Config096,
                              Config097,
                              Config098,
                              Config099,
                              Config100,
                              Config101,
                              Config102,
                              Config103,
                              Config104,
                              Config105,
                              Config106,
                              Config107,
                              Config108,
                              Config109,
                              Config110,
                              # Config111,
                              # Config112,
                              # Config113,
                              # Config114,
                              # Config115,
                              # Config116,
                              # Config117,
                              # Config118,
                              # Config119,
                              # Config120,
                              # Config121,
                              # Config122,
                              # Config123,
                              # Config124,
                              # Config125,
                              # Config126,
                              Config127,
                              Config128,
                              Config129,
                              Config130,
                              # Config131,
                              # Config132,
                              # Config133,
                              # Config134,
                              Config135,
                              Config136,
                              Config137,
                              Config138,
                              # Config139,
                              # Config140,
                              # Config141,
                              # Config142,
                              # Config143,
                              # Config144,
                              # Config145,
                              # Config146,
                              # Config147,
                              # Config148,
                              # Config149,
                              # Config150,
                              # Config151,
                              # Config152,
                              # Config153,
                              # Config154,
                              # Config155,
                              # Config156,
                              # Config157,
                              # Config158,
                              Config159,
                              Config160,
                              Config161,
                              Config162,
                              # Config163,
                              # Config164,
                              # Config165,
                              # Config166,
                              # Config167,
                              # Config168,
                              # Config169,
                              # Config170,
                              # Config171,
                              # Config172,
                              # Config173,
                              # Config174,
                              # Config175,
                              # Config176,
                              # Config177,
                              # Config178,
                              # Config179,
                              # Config180,
                              # Config181,
                              # Config182,
                              # Config183,
                              # Config184,
                              # Config185,
                              # Config186,
                              # Config187,
                              # Config188,
                              # Config189,
                              # Config190,
                              # Config191,
                              # Config192,
                              # Config193,
                              # Config194,
                              Config195,
                              Config196,
                              Config197,
                              Config198,
                              Config199,
                              Config200,
                              Config201,
                              Config202,
                              Config203,
                              Config204,
                              Config205,
                              Config206,
                              Config207,
                              Config208,
                              Config209,
                              Config210,
                              Config211,
                              Config212,
                              Config213,
                              Config214,
                              Config215,
                              Config216,
                              Config217,
                              Config218,
                             ])
    def test_engine(self, conf: EngineTestConfig, overwrite: bool):
        """Performs a system test on the engine

        See README for in depth details
        """

        EngineTester(base_dir=self.base_dir,
                     conf=conf,
                     overwrite=overwrite).test_engine()

    @property
    def base_dir(self) -> Path:
        """Returns test output dir"""

        return Path(__file__).parent / "engine_test_outputs"
