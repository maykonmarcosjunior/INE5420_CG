from src.window import Window


class DisplayFile:
    def __init__(self):
        self.__objects = []

    def run(self, title="Window", width=960, height=720):
        window = Window(title, width, height)

        # while window.is_active():
        #     new_obj = window.get_object()
        #     self.__objects.append(new_obj)
        #     window.draw(self.__objects)
