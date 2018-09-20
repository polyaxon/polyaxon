import * as _ from 'lodash';
import * as React from 'react';
import { Dropdown, MenuItem, Modal } from 'react-bootstrap';

import * as actions from '../../actions/metrics';
import { ChartModel } from '../../models/chart';
import { ChartViewModel } from '../../models/chartView';
import { MetricModel } from '../../models/metric';
import AutocompleteLabel from '../autocomplete/autocompleteLabel';
import AutocompleteDropdown from '../autocomplete/autocomplteDorpdown';
import ChartView from '../charts/chartView';

import '../dropdowns.less';
import './metrics.less';

export interface Props {
  metrics: MetricModel[];
  views: ChartViewModel[];
  resource: string;
  count: number;
  fetchData: () => actions.MetricsAction;
  fetchViews: () => actions.MetricsAction;
  createView?: (data: ChartViewModel) => actions.MetricsAction;
  deleteView?: (viewId: number) => actions.MetricsAction;
}

export interface State {
  isGrid: boolean;
  metricNames: string[];
  view: ChartViewModel;
  showChartModal: boolean;
  showViewModal: boolean;
  chartForm: { chart: ChartModel, metricNames: string[] };
}

export default class Metrics extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    const metricNames = this.getMetricNames();
    this.state = {
      isGrid: true,
      showChartModal: false,
      showViewModal: false,
      metricNames,
      view: this.getDefaultView(metricNames),
      chartForm: this.getEmptyChartForm(metricNames)
    };
  }

  public componentDidMount() {
    this.props.fetchData();
    this.props.fetchViews();
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (!_.isEqual(this.props.metrics, prevProps.metrics)) {
      const metricNames = this.getMetricNames();
      this.setState({
        ...prevState,
        metricNames,
        view: this.getDefaultView(metricNames),
        chartForm: {...prevState.chartForm, metricNames}
      });
    }
  }

  public getEmptyChartForm = (metricNames: string[]) => {
    return {
      metricNames,
      chart: {
        name: 'untitled',
        metricNames: [] as string[],
        mode: 'lines',
        type: 'scatter'
      } as ChartModel
    };
  };

  public setLayout = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      ...{
        isGrid: !this.state.isGrid,
      }
    }));
  };

  public saveView = (event: any) => {
    event.preventDefault();
    if (this.props.createView) {
      this.props.createView(this.state.view);
    }
    this.handleClose();
  };

  public updateViewForm = (key: string, value: string) => {
    let updated = false;
    const view = {...this.state.view};
    if (key === 'name') {
      view.name = value;
      updated = true;
    } else if (key === 'smoothing') {
      view.meta.smoothing = parseFloat(value);
      updated = true;
    } else if (key === 'xAxis') {
      if (value === 'time') {
        view.meta.xAxis = 'time';
        updated = true;
      } else if (value === 'step') {
        view.meta.xAxis = 'step';
        updated = true;
      }
    }
    if (updated) {
      this.setState((prevState, prevProps) => ({
        ...prevState, view
      }));
    }
  };

  public deleteView = (event: any, viewId: number) => {
    event.preventDefault();
    if (this.props.deleteView) {
      this.props.deleteView(viewId);
    }
  };

  public selectView = (chartView: ChartViewModel) => {
    this.setState((prevState, prevProps) => ({
      ...prevState, view: chartView
    }));
  };

  public handleClose = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{showViewModal: false, showChartModal: false}
    }));
  };

  public handleShow = (type: 'showViewModal' | 'showChartModal') => {
    const updateState = {showViewModal: false, showChartModal: false};
    updateState[type] = true;
    this.setState((prevState, prevProps) => ({
      ...prevState, ...updateState
    }));
  };

  public addChart = (event: any) => {
    event.preventDefault();
    this.setState((prevState, prevProps) => ({
      ...prevState,
      view: {
        ...prevState.view,
        charts: [...prevState.view.charts, prevState.chartForm.chart]
      },
      chartForm: this.getEmptyChartForm(this.state.metricNames)
    }));
    this.handleClose();
  };

  public removeChart = (chartIdx: number) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      view: {
        ...prevState.view,
        charts: [...prevState.view.charts.filter((chart, idx) => idx !== chartIdx)]
      },
      chartForm: this.getEmptyChartForm(this.state.metricNames)
    }));
    this.handleClose();
  };

  public updateChartForm = (key: string, value: string) => {
    let updated = false;
    const chartForm = {...this.state.chartForm};
    if (key === 'name') {
      chartForm.chart.name = value;
      updated = true;
    }
    if (updated) {
      this.setState((prevState, prevProps) => ({
        ...prevState, chartForm
      }));
    }
  };

  public addMetricChartForm = (metricName: string) => {
    const selectedMetrics = [...this.state.chartForm.chart.metricNames, metricName].sort();
    const chartMetricNames = this.state.chartForm.metricNames
      .filter((m) => m !== metricName);

    this.setState((prevState, prevProps) => ({
      ...prevState,
      chartForm: {
        ...prevState.chartForm,
        ...{
          metricNames: chartMetricNames,
          chart: {...prevState.chartForm.chart, metricNames: selectedMetrics}
        }
      }
    }));
  };

  public removeMetricChartForm = (value: string) => {
    const chartMetricNames = this.state.chartForm.chart.metricNames.filter((
      item: string) => item !== value);
    const metricNames = [...this.state.chartForm.metricNames, value].sort();
    this.setState((prevState, prevProps) => ({
      ...prevState,
      chartForm: {
        ...prevState.chartForm,
        ...{
          metricNames,
          chart: {...prevState.chartForm.chart, metricNames: chartMetricNames}
        }
      }
    }));
  };

  public getDefaultView = (metricNames: string[]) => {
    const charts: ChartModel[] = [];
    for (const metricName of metricNames) {
      if (metricName === 'step') {
        continue;
      }
      charts.push({
        name: metricName,
        metricNames: [metricName],
        mode: 'lines',
        type: 'scatter'
      } as ChartModel);
    }
    return {charts, name: 'untitled', meta: {smoothing: 0.1, xAxis: 'time'}} as ChartViewModel;
  };

  public getMetricNames = () => {
    return [...Array.from(
      new Set(([] as string[]).concat(
        ...this.props.metrics.map((metric) => Object.keys(metric.values)))
      )
    )].sort();
  };

  public render() {
    const viewsList = (
      <Dropdown id="dropdown-views">
        <Dropdown.Toggle
          bsStyle="default"
          bsSize="small"
        >
          <i className="fa fa-clone icon" aria-hidden="true"/> Views
        </Dropdown.Toggle>
        <Dropdown.Menu className="dropdown-menu-large">
          {this.props.views.map(
            (view, idx: number) =>
              <MenuItem
                key={idx}
                className="dropdown-select-menu"
                onClick={() => this.selectView(view)}
              >
                <button
                  type="button"
                  className="close pull-right"
                  aria-label="Close"
                  onClick={(event) => this.deleteView(event, view.id)}
                >
                  <span aria-hidden="true">&times;</span>
                </button>
                <span>
                  {view.name || 'untitled'}:
                </span>
                <p className="dropdown-meta">
                  <span className="label dropdown-label">
                    number charts:
                  </span> {view.charts.length}
                </p>
              </MenuItem>
          )}
          {this.props.views.length === 0 &&
          <MenuItem className="dropdown-select-menu">
            No saved views
          </MenuItem>
          }
        </Dropdown.Menu>
      </Dropdown>
    );

    const chartModal = (
      <Modal show={this.state.showChartModal} onHide={this.handleClose}>
        <Modal.Header closeButton={true}>
          <Modal.Title>Add chart</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form className="form-horizontal" onSubmit={this.addChart}>
            <div className="form-group">
              <label className="col-sm-2 control-label">Name</label>
              <div className="col-sm-10">
                <input
                  type="text"
                  className="form-control"
                  onChange={(event) => this.updateChartForm('name', event.target.value)}
                />
              </div>
            </div>
            <div className="form-group">
              <div className="col-sm-10 col-sm-offset-2">
                {this.state.chartForm.chart.metricNames.map(
                  (value: string, idx: number) =>
                    <AutocompleteLabel
                      key={idx}
                      value={value}
                      onClick={this.removeMetricChartForm}
                    />
                )}
                <AutocompleteDropdown
                  title="Add column"
                  possibleValues={this.state.chartForm.metricNames}
                  selectedValues={this.state.chartForm.chart.metricNames}
                  onClick={this.addMetricChartForm}
                />
              </div>
            </div>
            <div className="form-group">
              <div className="col-sm-offset-2 col-sm-10">
                <button type="submit" className="btn btn-default" onClick={this.addChart}>Add</button>
              </div>
            </div>
          </form>
        </Modal.Body>
      </Modal>
    );

    const viewModal = (
      <Modal show={this.state.showViewModal} onHide={this.handleClose}>
        <Modal.Header closeButton={true}>
          <Modal.Title>Save View</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form className="form-horizontal" onSubmit={this.saveView}>
            <div className="form-group">
              <label className="col-sm-2 control-label">Name</label>
              <div className="col-sm-10">
                <input
                  type="text"
                  className="form-control"
                  onChange={(event) => this.updateViewForm('name', event.target.value)}
                />
              </div>
            </div>
            <div className="form-group">
              <div className="col-sm-offset-2 col-sm-10">
                <button type="submit" className="btn btn-default" onClick={this.saveView}>Save</button>
              </div>
            </div>
          </form>
        </Modal.Body>
      </Modal>
    );

    return (
      <div className="metrics">
        <div className="row">
          <div className="col-md-12">
            <div className="btn-group pull-left">
              {viewsList}
              <button className="btn btn-sm btn-default" onClick={() => this.handleShow('showViewModal')}>
                <i className="fa fa-download icon" aria-hidden="true"/> Save view
              </button>
            </div>
            <div className="input-group pull-right chart-view-tools">
              <span>
                <button className="btn btn-sm btn-default add-chart" onClick={() => this.handleShow('showChartModal')}>
                  <i className="fa fa-plus icon" aria-hidden="true"/> Add chart
                </button>
              </span>
              <span>
                <span className="input-group">
                    <span className="input-group-addon" id="sizing-addon1">Smoothing</span>
                    <input
                      type="number"
                      className="form-control input-sm"
                      min="0"
                      max="1"
                      step="0.1"
                      onChange={(event) => this.updateViewForm('smoothing', event.target.value)}
                    />
                </span>
              </span>
              <span>
                <button
                  className="btn btn-sm btn-default chart-axis"
                  onClick={(e) => this.updateViewForm('xAxis', this.state.view.meta.xAxis === 'time' ? 'step' : 'time')}
                >
                  {this.state.view.meta.xAxis === 'time'
                    ? 'x-axis: Step'
                    : 'x-axis: Time'
                  }
                </button>
              </span>
              <span>
                <button className="btn btn-sm btn-default chart-display" onClick={this.setLayout}>
                  {this.state.isGrid
                    ? <span><i className="fa fa-bars icon" aria-hidden="true"/> List</span>
                    : <span><i className="fa fa-th-large icon" aria-hidden="true"/> Grid</span>
                  }
                </button>
              </span>
            </div>
          </div>
          <ChartView
            className={this.state.isGrid ? 'col-md-6' : 'col-md-10 col-md-offset-1'}
            metrics={this.props.metrics}
            view={this.state.view}
            resource={this.props.resource}
            onRemoveChart={this.removeChart}
          />
        </div>
        {chartModal}
        {viewModal}
      </div>
    );
  }
}
