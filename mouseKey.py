from enum import Enum

class MouseKey(Enum):
    """Hexadecimal values useed in ydotool click"""
    LEFT = 0x00
    RIGHT = 0x01
    MIDDLE = 0x02
    SIDE = 0x03
    EXTR = 0x04
    FOWARD = 0x05
    BACK = 0x06
    TASK = 0x07

class MouseKeyMask(Enum):
    DOWN_MASK = 0x04
    UP_MASK = 0x08
    UP_DOWN_MASK = DOWN_MASK | UP_MASK

def mask_button(button : MouseKey, action : MouseKeyMask):
    return button.value | action.value

def get_hex_from_string(buttonStr : str):
    try: #By default every mouse button is interpred as a click if the user want to hold the button an integer as to be used
        return mask_button(MouseKey(buttonStr.upper()), MouseKeyMask.UP_DOWN_MASK)
    except ValueError:
        try:
            return MouseKeyMask(buttonStr.upper)
        except ValueError:
            print("This {} button does not exist".format(buttonStr))