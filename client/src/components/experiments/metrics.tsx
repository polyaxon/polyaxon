import * as React from 'react';
import { Dropdown, MenuItem, Modal } from 'react-bootstrap';

import * as actions from '../../actions/metrics';
import { ChartModel } from '../../models/chart';
import { ChartViewModel } from '../../models/chartView';
import { MetricModel } from '../../models/metric';
import AutocompleteDropdown from '../autocomplete/autocomplteDorpdown';
import AutocompleteLabel from '../autocompleteLabel';
import ChartView from '../charts/chartView';

export interface Props {
  metrics: MetricModel[];
  count: number;
  fetchData: () => actions.MetricsAction;
  deleteView?: (view: string) => actions.MetricsAction;
  createView?: (view: string) => actions.MetricsAction;
}

export interface State {
  isGrid: boolean;
  metricNames: string[];
  view: ChartViewModel;
  showViewModal: boolean;
  chartForm: { chart: ChartModel, metricNames: string[] };
}

export default class Metrics extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    const metricNames = this.getMetricNames();
    this.state = {
      isGrid: true,
      showViewModal: false,
      metricNames,
      view: this.getDefaultView(metricNames),
      chartForm: this.getEmptyChartForm(metricNames)
    };
  }

  public componentDidMount() {
    this.props.fetchData();
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (this.props.metrics !== prevProps.metrics) {
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
          name: '',
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
      this.props.createView('');
    }
    this.handleClose();
  };

  public deleteView = (event: any, view: string) => {
    event.preventDefault();
    if (this.props.deleteView) {
      this.props.deleteView(view);
    }
  };

  public selectView = (view: string) => {
    const state = {};

    this.setState((prevState, prevProps) => ({
      ...prevState, ...state
    }));
  };

  public handleClose = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{showViewModal: false}
    }));
  };

  public handleShow = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState, ...{showViewModal: true}
    }));
  };

  public addChart = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      view: {...prevState.view, charts: [...prevState.view.charts, prevState.chartForm.chart]},
      chartForm: this.getEmptyChartForm(this.state.metricNames)
    }));
  };

  public updateChartForm = (key: string, value: string) => {
    const chartForm = {...this.state.chartForm};
    if (key === 'name') {
      chartForm.chart.name = value;
    }
    this.setState((prevState, prevProps) => ({
      ...prevState, chartForm
    }));
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
          chart: {...prevState.chartForm.chart, metricNames: selectedMetrics}}
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
          chart: {...prevState.chartForm.chart, metricNames: chartMetricNames}}
      }
    }));
  };

  public getDefaultView = (metricNames: string[]) => {
    const charts: ChartModel[] = [];
    for (const metricName of metricNames) {
      charts.push({
        name: metricName,
        metricNames: [metricName],
        mode: 'lines',
        type: 'scatter'
      } as ChartModel);
    }
    return {charts, name: 'default'} as ChartViewModel;
  };

  public getMetricNames = () => {
    return [...Array.from(
      new Set(([] as string[]).concat(
        ...this.props.metrics.map((metric) => Object.keys(metric.values)))
      )
    )].sort();
  };

  public render() {

    const views: string[] = [];

    const viewsList = (
      <Dropdown id="dropdown-views">
        <Dropdown.Toggle
          bsStyle="default"
          bsSize="small"
        >
          <i className="fa fa-clone icon" aria-hidden="true"/> Views
        </Dropdown.Toggle>
        <Dropdown.Menu>
          {views.map(
            (view, idx: number) =>
              <MenuItem
                key={idx}
                className="search-saved-query"
                onClick={() => this.selectView(view)}
              >
                <button
                  type="button"
                  className="close pull-right"
                  aria-label="Close"
                  onClick={(event) => this.deleteView(event, view)}
                >
                  <span aria-hidden="true">&times;</span>
                </button>
                <span>
                      {view || 'untitled'}:
                    </span>
                <p className="query-desc">
                    <span className="label label-search">
                      Query:
                    </span> {view}
                </p>
              </MenuItem>
          )}
          {views.length === 0 &&
          <MenuItem className="search-saved-query">
            No saved views
          </MenuItem>
          }
        </Dropdown.Menu>
      </Dropdown>
    );

    const chartModal = (
      <Modal show={this.state.showViewModal} onHide={this.handleClose}>
        <Modal.Header closeButton={true}>
          <Modal.Title>Add chart</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form className="form-horizontal" onSubmit={this.saveView}>
            <div className="form-group">
              <label className="col-sm-2 control-label">Name</label>
              <div className="col-sm-10">
                <input
                  type="text"
                  className="form-control"
                  placeholder="untitled"
                  value={this.state.chartForm.chart.name}
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

    return (
      <div className="metrics">
        <div className="row">
          <div className="col-md-12">
            <div className="btn-group pull-left">
              {viewsList}
              <button className="btn btn-sm btn-default">
                <i className="fa fa-download icon" aria-hidden="true"/> Save view
              </button>
            </div>
            <div className="btn-toolbar pull-right">
              <button className="btn btn-sm btn-default" onClick={() => this.handleShow()}>
                <i className="fa fa-plus icon" aria-hidden="true"/> Add chart
              </button>
              <button className="btn btn-sm btn-default" onClick={this.setLayout}>
                {this.state.isGrid
                  ? <span><i className="fa fa-bars icon" aria-hidden="true"/> List</span>
                  : <span><i className="fa fa-th-large icon" aria-hidden="true"/> Grid</span>
                }
              </button>
            </div>
          </div>
          <ChartView
            className={this.state.isGrid ? 'col-md-6' : 'col-md-11 col-md-offset-1'}
            metrics={this.props.metrics}
            view={this.state.view}
          />
        </div>
        {chartModal}
      </div>
    );
  }
}
