from enum import Enum


class UpdateStrategy(Enum):
    FULL = 'full'    # 全量更新
    INCREMENTAL = 'incremental'  # 增量更新
