from .renderer import PlotlyRenderer
from .mplexporter import Exporter


def mpl_to_plotly(fig, resize=False, strip_style=False, verbose=False):
    """Convert a matplotlib figure to plotly dictionary and send.
    All available information about matplotlib visualizations are stored
    within a matplotlib.figure.Figure object. You can create a plot in python
    using matplotlib, store the figure object, and then pass this object to
    the fig_to_plotly function. In the background, mplexporter is used to
    crawl through the mpl figure object for appropriate information. This
    information is then systematically sent to the PlotlyRenderer which
    creates the JSON structure used to make plotly visualizations. Finally,
    these dictionaries are sent to plotly and your browser should open up a
    new tab for viewing! Optionally, if you're working in IPython, you can
    set notebook=True and the PlotlyRenderer will call plotly.iplot instead
    of plotly.plot to have the graph appear directly in the IPython notebook.
    Note, this function gives the user access to a simple, one-line way to
    render an mpl figure in plotly. If you need to trouble shoot, you can do
    this step manually by NOT running this fuction and entereing the following:
    ===========================================================================
    from plotly.matplotlylib import mplexporter, PlotlyRenderer
    # create an mpl figure and store it under a varialble 'fig'
    renderer = PlotlyRenderer()
    exporter = mplexporter.Exporter(renderer)
    exporter.run(fig)
    ===========================================================================
    You can then inspect the JSON structures by accessing these:
    renderer.layout -- a plotly layout dictionary
    renderer.data -- a list of plotly data dictionaries
    """

    # Update vendor
    # This code was taken from:
    # https://github.com/matplotlib/matplotlib/pull/16772/files#diff-506cc6d736a0593e8bb820981b2c12ae # noqa
    # Removed in https://github.com/matplotlib/matplotlib/pull/16772
    from matplotlib.spines import Spine

    def is_frame_like(self):
        """return True if directly on axes frame
        This is useful for determining if a spine is the edge of an
        old style MPL plot. If so, this function will return True.
        """
        self._ensure_position_is_set()
        position = self._position
        if isinstance(position, str):
            if position == "center":
                position = ("axes", 0.5)
            elif position == "zero":
                position = ("data", 0)
        if len(position) != 2:
            raise ValueError("position should be 2-tuple")
        position_type, amount = position
        if position_type == "outward" and amount == 0:
            return True
        else:
            return False

    Spine.is_frame_like = is_frame_like

    renderer = PlotlyRenderer()
    Exporter(renderer).run(fig)
    if resize:
        renderer.resize()
    if strip_style:
        renderer.strip_style()
    if verbose:
        print(renderer.msg)
    return renderer.plotly_fig
