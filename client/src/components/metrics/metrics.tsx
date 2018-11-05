import * as _ from 'lodash';
import * as React from 'react';
import { Dropdown, MenuItem, Modal } from 'react-bootstrap';

import * as experimentActions from '../../actions/experiment';
import * as actions from '../../actions/metrics';
import { ChartModel, ChartTypes } from '../../models/chart';
import { ChartViewModel } from '../../models/chartView';
import { MetricModel } from '../../models/metric';
import AutocompleteLabel from '../autocomplete/autocompleteLabel';
import AutocompleteDropdown from '../autocomplete/autocomplteDorpdown';
import ChartView from '../charts/chartView';
import Refresh from '../refresh';

import '../dropdowns.less';
import './metrics.less';

export interface Props {
  metrics: MetricModel[];
  params: { [id: number]: { [key: string]: any } };
  views: ChartViewModel[];
  resource: string;
  count: number;
  chartTypes: string[];
  fetchData: () => actions.MetricsAction;
  fetchParamsData?: () => experimentActions.ExperimentAction;
  fetchViews: () => actions.MetricsAction;
  createView?: (data: ChartViewModel) => actions.MetricsAction;
  deleteView?: (viewId: number) => actions.MetricsAction;
}

export interface State {
  isGrid: boolean;
  showChartModal: boolean;
  showViewModal: boolean;
  metricNames: string[];
  paramNames: string[];
  experiments: string[];
  view: ChartViewModel;
  chartForm: {
    chart: ChartModel,
    metricNames: string[],
    paramNames: string[],
    experiments: string[],
    index: number;
  };
}

export default class Metrics extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    const metricNames = this.getMetricNames();
    const paramNames = this.getParamNames();
    const experiments = this.getExperiments();
    this.state = {
      isGrid: true,
      showChartModal: false,
      showViewModal: false,
      metricNames,
      paramNames,
      experiments,
      view: this.props.resource === 'groups'
        ? this.getDefaultView([])
        : this.getDefaultView(metricNames),
      chartForm: this.getChartForm(metricNames, paramNames, experiments)
    };
  }

  public componentDidMount() {
    this.props.fetchData();
    this.props.fetchViews();
    if (this.props.resource === 'groups' && this.props.fetchParamsData) {
      this.props.fetchParamsData();
    }
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (!_.isEqual(this.props.metrics, prevProps.metrics) ||
      !_.isEqual(this.props.params, prevProps.params)) {
      const metricNames = this.getMetricNames();
      const paramNames = this.getParamNames();
      const experiments = this.getExperiments();
      this.setState({
        ...prevState,
        metricNames,
        paramNames,
        experiments,
        // Do not set a default view for groups (could be too large)
        view: this.props.resource === 'groups'
          ? this.getDefaultView([])
          : this.getDefaultView(metricNames),
        chartForm: {...prevState.chartForm, metricNames, paramNames, experiments}
      });
    }
  }

  public refresh = () => {
    this.props.fetchData();
  };

  public getChartForm = (metricNames: string[],
                         paramNames: string[],
                         experiments: string[],
                         name: string = 'untitled',
                         chartMetricNames: string[] = [],
                         chartParamNames: string[] = [],
                         chartExperiments: string[] = [],
                         chartType: ChartTypes = 'line',
                         index: number = -1) => {
    return {
      metricNames,
      paramNames,
      experiments,
      index,
      chart: {
        name,
        metricNames: chartMetricNames,
        paramNames: chartParamNames,
        experiments: chartExperiments,
        type: chartType,
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
    const getChart = (chart: ChartModel): ChartModel => {
      if (chart.metricNames.length === 0) {
        chart.metricNames = [this.state.metricNames[0]];
      }
      if (chart.paramNames.length === 0 && (chart.type === 'scatter' || chart.type === 'histogram')) {
        chart.paramNames = [this.state.paramNames[0]];
      }
      if (
        (!chart.name || chart.name === 'untitled') &&
        chart.type === 'histogram' &&
        (chart.metricNames.length > 0 && chart.paramNames.length > 0)
      ) {
        chart.name = _.join([chart.metricNames[0], chart.paramNames[0]], ' / ');
      }
      if (
        (!chart.name || chart.name === 'untitled') &&
        chart.type === 'scatter' && chart.paramNames.length > 0
      ) {
        chart.name = chart.paramNames[0];
      }
      if (
        (!chart.name || chart.name === 'untitled') &&
        (chart.type === 'line' || chart.type === 'bar') &&
        (chart.experiments.length > 1)
      ) {
        chart.name = _.join(chart.metricNames, ', ');
      }
      return chart;
    };
    // const chart = prevState.chartForm.chart;
    this.setState((prevState, prevProps) => ({
      ...prevState,
      view: {
        ...prevState.view,
        charts: prevState.chartForm.index > -1
          ? [...prevState.view.charts.map(
            (chart, idx) => idx === prevState.chartForm.index ? getChart(prevState.chartForm.chart) : chart)]
          : [...prevState.view.charts, getChart(prevState.chartForm.chart)]
      },
      chartForm: this.getChartForm(
        this.state.metricNames, this.state.paramNames, this.state.experiments)
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
      chartForm: this.getChartForm(
        this.state.metricNames, this.state.paramNames, this.state.experiments)
    }));
    this.handleClose();
  };

  public updateChart = (chartIdx: number) => {
    const chart = this.state.view.charts[chartIdx];
    this.setState((prevState, prevProps) => ({
      ...prevState,
      chartForm: this.getChartForm(
        this.state.metricNames,
        this.state.paramNames,
        this.state.experiments,
        chart.name,
        chart.metricNames,
        chart.paramNames,
        chart.experiments,
        chart.type,
        chartIdx)
    }));
    this.handleShow('showChartModal');
  };

  public updateChartForm = (key: string, value: string) => {
    let updated = false;
    const chartForm = {...this.state.chartForm};
    if (key === 'name') {
      chartForm.chart.name = value;
      updated = true;
    } else if (key === 'type') {
      chartForm.chart.type = value as ChartTypes;
      updated = true;
    } else if (key === 'param') {
      chartForm.chart.paramNames = [value];
      updated = true;
    } else if (key === 'metric') {
      chartForm.chart.metricNames = [value];
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

  public addExperimentChartForm = (experiment: string) => {
    const selectedExperiments = [...this.state.chartForm.chart.experiments, experiment].sort();
    const chartExperiments = this.state.chartForm.experiments
      .filter((m) => m !== experiment);

    this.setState((prevState, prevProps) => ({
      ...prevState,
      chartForm: {
        ...prevState.chartForm,
        ...{
          experiments: chartExperiments,
          chart: {...prevState.chartForm.chart, experiments: selectedExperiments}
        }
      }
    }));
  };

  public removeExperimentChartForm = (value: string) => {
    const chartExperiments = this.state.chartForm.chart.experiments.filter((
      item: string) => item !== value);
    const experiments = [...this.state.chartForm.experiments, value].sort();
    this.setState((prevState, prevProps) => ({
      ...prevState,
      chartForm: {
        ...prevState.chartForm,
        ...{
          experiments,
          chart: {...prevState.chartForm.chart, experiments: chartExperiments}
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
        type: 'line'
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

  public getExperiments = () => {
    return [...Array.from(
      new Set(([] as string[]).concat(
        ...this.props.metrics.map((metric) => `${metric.experiment}`))
      )
    )].sort();
  };

  public getParamNames = () => {
    const params = [];
    for (const xp of Object.keys(this.props.params)) {
      const xpParams = this.props.params[parseInt(xp, 10)];
      if (!xpParams) {
        return params;
      }
      for (const param of Object.keys(xpParams)) {
        if (params.indexOf(param) === -1) {
          params.push(param);
        }
      }
    }
    return params;
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
                <span className="dropdown-title">
                  {view.name || 'untitled'}
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
              <label className="col-sm-2 control-label">Chart Type</label>
              <div className="col-sm-10">
                <select
                  onChange={(event) => this.updateChartForm('type', event.target.value)}
                  className="form-control"
                >
                  {
                    this.props.chartTypes.indexOf('line') > -1 &&
                    <option>line</option>
                  }
                  {
                    this.props.chartTypes.indexOf('bar') > -1 &&
                    <option>bar</option>
                  }
                  {
                    this.props.chartTypes.indexOf('scatter') > -1 &&
                    this.state.paramNames.length > 0 &&
                    <option>scatter</option>
                  }
                  {
                    this.props.chartTypes.indexOf('histogram') > -1 &&
                    this.state.paramNames.length > 0 &&
                    <option>histogram</option>
                  }
                </select>
              </div>
            </div>
            {this.state.paramNames.length > 0 &&
            (this.state.chartForm.chart.type === 'histogram' || this.state.chartForm.chart.type === 'scatter') &&
            <div className="form-group">
              <label className="col-sm-2 control-label">Param</label>
              <div className="col-sm-10">
                <select
                  onChange={(event) => this.updateChartForm('param', event.target.value)}
                  className="form-control"
                >
                  {this.state.paramNames.map((param) => <option key={param}>{param}</option>)}
                </select>
              </div>
            </div>
            }
            {((this.state.paramNames.length > 0 && this.state.chartForm.chart.type === 'histogram') ||
              (this.props.resource === 'groups' &&
                (this.state.chartForm.chart.type === 'line' || this.state.chartForm.chart.type === 'bar'))) &&
            <div className="form-group">
              <label className="col-sm-2 control-label">Metric</label>
              <div className="col-sm-10">
                <select
                  onChange={(event) => this.updateChartForm('metric', event.target.value)}
                  className="form-control"
                >
                  {this.state.metricNames.map((metric) => <option key={metric}>{metric}</option>)}
                </select>
              </div>
            </div>
            }
            {this.props.resource === 'groups' &&
            (this.state.chartForm.chart.type === 'line' || this.state.chartForm.chart.type === 'bar') &&
            <div className="form-group">
              <div className="col-sm-10 col-sm-offset-2">
                {this.state.chartForm.chart.experiments.map(
                  (value: string, idx: number) =>
                    <AutocompleteLabel
                      key={idx}
                      value={value}
                      onClick={this.removeExperimentChartForm}
                    />
                )}
                <AutocompleteDropdown
                  title="Add experiment"
                  possibleValues={this.state.chartForm.experiments}
                  selectedValues={this.state.chartForm.chart.experiments}
                  onClick={this.addExperimentChartForm}
                />
              </div>
            </div>
            }
            {(this.state.chartForm.chart.type !== 'histogram' &&
              !(this.props.resource === 'groups' &&
                (this.state.chartForm.chart.type === 'line' || this.state.chartForm.chart.type === 'bar'))) &&
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
                  title="Add metric"
                  possibleValues={this.state.chartForm.metricNames}
                  selectedValues={this.state.chartForm.chart.metricNames}
                  onClick={this.addMetricChartForm}
                />
              </div>
            </div>
            }
            <div className="form-group">
              <div className="col-sm-offset-2 col-sm-10">
                <button type="submit" className="btn btn-default" onClick={this.addChart}>
                  {this.state.chartForm.index > -1 ? 'Update' : 'Add'}
                </button>
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
                <span id="helpBlock" className="help-block">The name must be a slug.</span>
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
                <button className="btn btn-sm btn-default" onClick={() => this.handleShow('showChartModal')}>
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
              <Refresh callback={this.refresh} pullRight={false}/>
            </div>
          </div>
          <ChartView
            className={this.state.isGrid ? 'col-md-6' : 'col-md-10 col-md-offset-1'}
            metrics={this.props.metrics}
            params={this.props.params}
            view={this.state.view}
            resource={this.props.resource}
            onRemoveChart={this.removeChart}
            onUpdateChart={this.updateChart}
          />
        </div>
        {chartModal}
        {viewModal}
      </div>
    );
  }
}
