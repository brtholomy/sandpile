import matplotlib.animation as animation
import matplotlib.colors as colors
import matplotlib.pyplot as plt
from tqdm import tqdm


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
