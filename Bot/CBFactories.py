from aiogram.filters.callback_data import CallbackData
from typing import Optional
class CBF_Pieces(CallbackData, prefix='pieces'):
    action: str
    value: Optional[str]
    back_value: Optional[str]
    id: Optional[str]

