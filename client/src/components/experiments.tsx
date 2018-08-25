import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../actions/experiment';
import { ExperimentModel } from '../models/experiment';
import { EmptyBookmarks } from './empty/emptyBookmarks';
import { EmptyList } from './empty/emptyList';
import Experiment from './experiment';
import { EXPERIMENT_FILTERS } from './filters/constants';
import PaginatedTable from './paginatedTable';

export interface Props {
  isCurrentUser: boolean;
  experiments: ExperimentModel[];
  count: number;
  useFilters: boolean;
  bookmarks: boolean;
  onCreate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onUpdate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onDelete: (experimentName: string) => actions.ExperimentAction;
  onStop: (experimentName: string) => actions.ExperimentAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.ExperimentAction;
}

interface State {
  metrics: string[];
  declarations: string[];
  columns: string;
}

export default class Experiments extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      metrics: [],
      declarations: [],
      columns: '',
    };
  }

  public shouldComponentUpdate(nextProps: Props, nextState: State) {
    const baseUrl = location.hash.split('?')[0];
    return baseUrl === '#experiments';
  }

  public setColumns(columns: string) {
    this.setState((prevState, prevProps) => ({
      ...prevState, columns
    }));
  }

  public updateColumns = (event: any) => {
    event.preventDefault();
    const metrics: string[] = [];
    const declarations: string[] = [];

    for (const column of this.state.columns.split(',')) {
      const columnValues = _.trim(column).split('.');
      if (columnValues.length > 1 && columnValues[0] === 'metric') {
        metrics.push(columnValues[1]);
      } else if (columnValues.length > 1 && columnValues[0] === 'declarations') {
        declarations.push(columnValues[1]);
      }
    }

    this.setState((prevState, prevProps) => ({
      ...prevState, ...{metrics, declarations}
    }));
  };

  public render() {
    const filters = this.props.useFilters ? EXPERIMENT_FILTERS : false;
    const experiments = this.props.experiments;
    const listExperiments = () => {
      return (
        <div>
          <form className="form-horizontal" onSubmit={this.updateColumns}>
            <input
              type="text"
              value={this.state.columns}
              onChange={(event) => this.setColumns(event.target.value)}
            />
          </form>
          <table className="table table-hover table-responsive">
            <colgroup span={4}/>
            <colgroup span={1}/>
            <colgroup span={1}/>
            {this.state.metrics.length > 0 && <colgroup span={this.state.metrics.length}/>}
            {this.state.declarations.length > 0 && <colgroup span={this.state.declarations.length}/>}
            <colgroup span={1}/>
            <tbody>
            {(this.state.metrics.length > 0 || this.state.declarations.length > 0) &&
            <tr>
              <th className="top-row" scope="colgroup" colSpan={4}/>
              {this.state.declarations.length > 0 &&
              <th
                className="top-row left-border"
                scope="colgroup"
                colSpan={this.state.declarations.length}
              > Declarations
              </th>}
              {this.state.metrics.length > 0 &&
              <th
                className="top-row left-border"
                scope="colgroup"
                colSpan={this.state.metrics.length}
              > Metrics
              </th>}
              <th className="top-row" scope="colgroup" colSpan={1}/>
            </tr>}
            <tr className="list-header">
              <th className="block">
                Status
              </th>
              <th className="block">
                Name
              </th>
              <th className="block">
                Info
              </th>
              <th className="block">
                Run
              </th>
              {this.state.declarations.map((declaration: string, idx: number) =>
                <th key={idx} className="block">
                  {declaration}
                </th>
              )}
              {this.state.metrics.map((metric: string, idx: number) =>
                <th key={idx} className="block">
                  {metric}
                </th>
              )}
              <th className="block pull-right">
                Actions
              </th>
            </tr>
            {experiments.map(
              (xp: ExperimentModel) =>
                <Experiment
                  key={xp.unique_name}
                  experiment={xp}
                  declarations={this.state.declarations}
                  metrics={this.state.metrics}
                  onDelete={() => this.props.onDelete(xp.unique_name)}
                  onStop={() => this.props.onStop(xp.unique_name)}
                />)}
            </tbody>
          </table>
        </div>
      );
    };

    const empty = this.props.bookmarks ?
      EmptyBookmarks(
        this.props.isCurrentUser,
        'experiment',
        'experiment')
      : EmptyList(
        this.props.isCurrentUser,
        'experiment',
        'experiment',
        'polyaxon run --help');
    return (
      <PaginatedTable
        count={this.props.count}
        componentList={listExperiments()}
        componentEmpty={empty}
        filters={filters}
        fetchData={this.props.fetchData}
      />
    );
  }
}
