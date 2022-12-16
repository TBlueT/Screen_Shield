from PyQt6.QtCore import QThread
import timeit, time

class UiUpdate(QThread):
    def __init__(self, parent):
        super(UiUpdate, self).__init__(parent)
        self.daemon = True
        self.run_stop = True

        self.paint = parent
        self.prev_time = 0
        self.FPS = 20
    def run(self):
        while self.run_stop:

            current_time = timeit.default_timer() - self.prev_time
            if (current_time > 1. / self.FPS):

                self.paint.update()
                #FPS = int(1. / current_time)
                #print(FPS)
                self.prev_time = timeit.default_timer()

            time.sleep(0.0001)