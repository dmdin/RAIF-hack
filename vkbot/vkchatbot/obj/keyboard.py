from typing import Tuple
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


class Keyboard(VkKeyboard):
    def __init__(self, *buttons, one_time=False):
        """
        Обертка для VkKeyboard с добавлением всех кнопок в __init__()
        :type buttons: Tuple[str] or str
        :type one_time: bool
        """
        super().__init__(one_time)
        for btn in buttons:
            if btn == '\n':
                self.add_line()
            else:
                label, color = btn
                self.add_button(label, color)


if __name__ == '__main__':
    prim = VkKeyboardColor.PRIMARY
    deft = VkKeyboardColor.DEFAULT
    posv = VkKeyboardColor.POSITIVE
    negv = VkKeyboardColor.NEGATIVE

    kb = Keyboard(('Button 1', prim), ('Button 2', prim), '\n', ('Line 2', posv), ('Line 2', negv))
