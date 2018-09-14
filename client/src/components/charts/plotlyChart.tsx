import * as Plotly from 'plotly.js';
import * as React from 'react';

interface Frame {
    name: string;
    data: [{ x: Plotly.Datum, y: Plotly.Datum }];
    group: 'lower' | 'upper';
  }

interface Figure {
    data: Plotly.Data[];
    layout: Partial<Plotly.Layout>;
  }

interface PlotParams {
    data: Plotly.Data[];
    layout: Partial<Plotly.Layout>;
    frames?: Frame[];
    config?: Partial<Plotly.Config>;
    revision?: number;
    onInitialized?: (figure: Readonly<Figure>, graphDiv: Readonly<HTMLElement>) => void;
    onUpdate?: (figure: Readonly<Figure>, graphDiv: Readonly<HTMLElement>) => void;
    onPurge?: (figure: Readonly<Figure>, graphDiv: Readonly<HTMLElement>) => void;
    onError?: (err: Readonly<Error>) => void;
    divId?: string;
    className?: string;
    style?: React.CSSProperties;
    debug?: boolean;
    useResizeHandler?: boolean;

    onAfterExport?: () => void;
    onAfterPlot?: () => void;
    onAnimated?: () => void;
    onAnimatingFrame?: (event: Readonly<Plotly.FrameAnimationEvent>) => void;
    onAnimationInterrupted?: () => void;
    onAutoSize?: () => void;
    onBeforeExport?: () => void;
    onButtonClicked?: (event: Readonly<Plotly.ButtonClickEvent>) => void;
    onClick?: (event: Readonly<Plotly.PlotMouseEvent>) => void;
    onClickAnnotation?: (event: Readonly<Plotly.ClickAnnotationEvent>) => void;
    onDeselect?: () => void;
    onDoubleClick?: () => void;
    onFramework?: () => void;
    onHover?: (event: Readonly<Plotly.PlotMouseEvent>) => void;
    onLegendClick?: (event: Readonly<Plotly.LegendClickEvent>) => boolean;
    onLegendDoubleClick?: (event: Readonly<Plotly.LegendClickEvent>) => boolean;
    onRelayout?: (event: Readonly<Plotly.PlotRelayoutEvent>) => void;
    onRestyle?: (event: Readonly<Plotly.PlotRestyleEvent>) => void;
    onRedraw?: () => void;
    onSelected?: (event: Readonly<Plotly.PlotSelectionEvent>) => void;
    onSelecting?: (event: Readonly<Plotly.PlotSelectionEvent>) => void;
    onSliderChange?: (event: Readonly<Plotly.SliderChangeEvent>) => void;
    onSliderEnd?: (event: Readonly<Plotly.SliderEndEvent>) => void;
    onSliderStart?: (event: Readonly<Plotly.SliderStartEvent>) => void;
    onTransitioning?: () => void;
    onTransitionInterrupted?: () => void;
    onUnhover?: (event: Readonly<Plotly.PlotMouseEvent>) => void;
  }

class PlotlyChart extends React.Component<PlotParams, {}> {
  public container: Plotly.PlotlyHTMLElement | null = null;

  public attachListeners() {
    if (this.props.onClick) {
      this.container!.on('plotly_click', this.props.onClick);
    }
    if (this.props.onHover) {
      this.container!.on('plotly_hover', this.props.onHover);
    }
    if (this.props.onSelected) {
      this.container!.on('plotly_selected', this.props.onSelected);
    }
    window.addEventListener('resize', this.resize);
  }

  public resize = () => {
    if (this.container) {
      Plotly.Plots.resize(this.container);
    }
  };

  public draw = async (props: PlotParams) => {
    const { data, layout, config } = props;
    if (this.container) {
      // plotly.react will not destroy the old plot: https://plot.ly/javascript/plotlyjs-function-reference/#plotlyreact
      this.container = await Plotly.react(this.container, data, Object.assign({}, layout), config);
      this.attachListeners();
    }
  };

  public componentWillReceiveProps(nextProps: PlotParams) {
    this.draw(nextProps);
  }

  public componentDidMount() {
    this.draw(this.props);
  }

  public componentWillUnmount() {
    if (this.container) {
      Plotly.purge(this.container);
    }
    window.removeEventListener('resize', this.resize);
  }

  public render() {
    const { data, layout, config, onClick, onHover, onSelected, ...other } = this.props;
    return (
      <div
        ref={async (node) => {
          if (node && !this.container) {
            this.container = await Plotly.newPlot(node, data as Plotly.Data[], Object.assign({}, layout), config);
            this.attachListeners();
          }
        }}
      />
    );
  }
}

export default PlotlyChart;
