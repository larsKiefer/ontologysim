import time

import numpy as np
import matplotlib.pyplot as plt

from matplotlib.figure import Figure


class Window:
    """
    depreciated, only used for setting up the Plot class

    """
    def __init__(self):


        self.fig = Figure(figsize=(5,4), dpi=100)
        self.axes = self.fig.add_subplot(111)
        self.axes.grid()
        self.xdata = [0]
        self.ydata = [0]
        self.entry_limit = 50
        self.line, = self.axes.plot([], [], 'r', lw=3)

        self.axes2 = self.axes.twinx()
        self.y2data = [0]
        self.line2, = self.axes2.plot([], [], 'b')

        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()

        self.nav = NavigationToolbar(self.canvas, self.widget)
        self.widget.layout().addWidget(self.nav)
        self.widget.layout().addWidget(self.canvas)

        self.show()

        self.ctimer = QtCore.QTimer()
        self.ctimer.timeout.connect(self.update)
        self.ctimer.start(150)


    def update(self):
        y = np.random.rand(1)
        self.update_figure_with_new_value(self.xdata[-1]+1,y)

    def update_figure_with_new_value(self, xval,yval):
        self.xdata.append(xval)
        self.ydata.append(yval)

        if len(self.xdata) > self.entry_limit:
            self.xdata.pop(0)
            self.ydata.pop(0)
            self.y2data.pop(0)

        self.line.set_data(self.xdata, self.ydata)
        self.axes.relim()
        self.axes.autoscale_view()

        self.y2data.append(yval+np.random.rand(1)*0.17)

        self.line2.set_data(self.xdata, self.y2data)
        self.axes2.relim()
        self.axes2.autoscale_view()

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


if __name__ == "__main__":

    a = Window()
    for i in range(1000):
        a.update()
        time.sleep(0.5)