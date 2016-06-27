import progressbar
from progressbar import widgets

def get_pbar(max_value):

    pbar = progressbar.ProgressBar(widgets=[
        widgets.Percentage(),
        ' (', widgets.SimpleProgress(), ')',
        ' ', widgets.Bar(),
        ' ', widgets.Timer(),
        ' ', widgets.AdaptiveETA(),
        ' ', widgets.DynamicMessage('Accuracy')
    ], max_value=max_value)
    return pbar
