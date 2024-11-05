from enum import Enum
import logging

logger = logging.getLogger(__name__)


class UpdateStrategy(Enum):
    FULL = 'full'    # 全量更新
    INCREMENTAL = 'incremental'  # 增量更新
