import PySimpleGUI as sg
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
matplotlib.use('TkAgg')

from zoom import ZoomPan


def draw_figure(canvas, figure):
    '''
    draw matplotlib figure on pySimplegui
    :param canvas: canvas element
    :param figure: matplotlib figure
    :return: agg figure
    '''
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def gui_window():
    '''
    Gui layout definition
    :return:
    '''
    sg.ChangeLookAndFeel('GreenTan')

    frame1 = [
        [sg.Input('Browse Subject Directory', do_not_clear=True, size=(57, 20), tooltip='Input', key="main_dir",enable_events=True), sg.FolderBrowse()],
        [sg.Combo([''], default_value='subject', size=(20,35), key='subject', disabled=True, enable_events=True),
        sg.Combo([''], default_value='day', size=(20, 35), key='day', disabled=True, enable_events=True),
        sg.Combo([''], default_value='session', size=(20, 35), key='session', disabled=True, enable_events=True)]
                ]

    fig = matplotlib.figure.Figure(figsize=(15, 8), dpi=100)

    ax = fig.add_subplot(111)

    frame2 = [
        [sg.Canvas(key='-CANVAS-')]
                ]
    # stats frame
    frame3 = [
        [sg.Text('', size=(20, 20), key='stats')],
    ]

    layout = [
        [sg.Frame('Select Session:', frame1, title_color='green')],
        [sg.Frame('', frame2, title_color='black'), sg.Frame('Stats:', frame3, title_color='black')],
        [sg.Button('Play', key='play', disabled=True, enable_events=True), sg.Button('Export', key='export', enable_events=True, disabled=True), sg.Button('Exit')],
             ]

    window = sg.Window('Piano Visualization Gui - © Ella, Rotem, Goni, Hackthon 2021', layout, finalize=True,
                       element_justification='center', font='Helvetica 18')
    window.Maximize()

    fig_canvas_agg = draw_figure(window.find_element('-CANVAS-').TKCanvas, fig)

    return window, ax, fig_canvas_agg

def draw_graph(canvas, ax, df):
    '''
    update graph with new data according to interactive gui
    :param canvas: canvas element in gui
    :param ax: axis object of matplotlib
    :param df: DataFrame data to plot
    :return: None
    '''
    df = df[df.action == 1]
    t = df.time
    ax.cla()
    ax.scatter(t, df.note)
    ax.set_xticks(t[0:-1:int(len(t)/10)])
    zp = ZoomPan()
    figZoom = zp.zoom_factory(ax, base_scale=1.1)
    figPan = zp.pan_factory(ax)
    canvas.draw()

