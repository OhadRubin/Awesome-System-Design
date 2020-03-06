import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class DepthImageParser:

    field = 'depth_image'

    def parse(self, context, snapshot):
        path = context.path('depth_image.jpg')
        data = np.array(list(snapshot.depth_image.data)).reshape([snapshot.depth_image.height,
                                                                  snapshot.depth_image.width])
        plt.figure()
        ax = sns.heatmap(data)
        ax.get_figure().savefig(path)

        return dict(path=path, height=snapshot.depth_image.height,
                               width=snapshot.depth_image.width)
