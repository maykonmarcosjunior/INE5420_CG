from src.window import Window

class DisplayFile:
    def __init__(self):
        self.__objects = []

    def run(self, title="Window", width=960, height=720):
        window = Window(title, width, height)
        print("Window created")
        while window.is_active():
            new_obj = window.get_object()
            print(new_obj)
            self.__objects.append(new_obj)
            # window.draw(self.__objects)
