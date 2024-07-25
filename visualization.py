import matplotlib.animation as animation
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from tqdm import tqdm


def PlotShow(plot=None):
    # special magic for avoiding a blocking call
    if plot:
        plt.show(plot, block=False)
    else:
        plt.show(block=False)
    # Pause to allow the input call to run:
    plt.pause(0.001)
    input("hit [enter] to end.")
    plt.close("all")

def PlotTotals(totals):
    plt.bar(totals.keys(), totals.values())
    PlotShow()

def Video(snapshots, maxh, fps=1, cmap='Blues', filename='video.mp4'):
    FFMpegWriter = animation.writers['ffmpeg']
    writer = FFMpegWriter(fps)

    fig = plt.figure()
    cnorm = colors.Normalize(vmin=0, vmax=maxh)

    with writer.saving(fig, filename, dpi=100):
        for shot in tqdm(snapshots):
            img = plt.imshow(
                shot, interpolation='nearest', cmap=cmap, norm=cnorm
            )
            writer.grab_frame()
            img.remove()
    plt.close('all')
