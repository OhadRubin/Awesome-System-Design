import numpy as np
import seaborn as sns

def parse_depth_image(context, snapshot):
    path = context.path('depth_image.jpg')
    data = np.array(list(snapshot.depth_image.data)).reshape([snapshot.depth_image.height,
                                                              snapshot.depth_image.width])
    ax = sns.heatmap(data)
    ax.get_figure().savefig(path)

parse_depth_image.field = "depth_image"
