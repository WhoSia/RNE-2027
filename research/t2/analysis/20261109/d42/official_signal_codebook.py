"""DLR UT v1.3.1 official categorical signal meanings.

Official publisher documentation: section 4.2.3, Table 4, PDF p. 14.
This is a decoder for historical observations, NOT a live controller.
"""
from enum import IntEnum

class DlrLightState(IntEnum):
    UNAVAILABLE = 0
    OFF = 1
    STOP_REQUIRED = 2
    RED = 3
    RED_YELLOW = 4
    GREEN = 5
    PROTECTED_GREEN = 6
    YELLOW = 7
    PROTECTED_YELLOW = 8
    FLASHING_YELLOW = 9

def summarize_head_states(raw_codes):
    """No implicit interpolation, no claim that head=movement."""
    from collections import Counter
    codes=Counter(DlrLightState(int(code)) for code in raw_codes)
    return {name.name:int(codes[name]) for name in DlrLightState}

def unavailable_or_nonstandard(code):
    state=DlrLightState(int(code))
    return state in {DlrLightState.UNAVAILABLE,
                     DlrLightState.OFF,
                     DlrLightState.FLASHING_YELLOW}

if __name__=="__main__":
    assert DlrLightState(3).name=="RED"
    assert DlrLightState(5).name=="GREEN"
    assert unavailable_or_nonstandard(9)
