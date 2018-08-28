import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../actions/experiment';
import * as search_actions from '../actions/search';
import { FILTER_EXAMPLES, JOB_FILTER_OPTIONS } from '../constants/filtering';
import { DEFAULT_SORT_OPTIONS } from '../constants/sorting';
import { FilterOption } from '../interfaces/filterOptions';
import { ExperimentModel } from '../models/experiment';
import { SearchModel } from '../models/search';
import AutocompleteDropdown from './autocomplete/autocomplteDorpdown';
import { EmptyBookmarks } from './empty/emptyBookmarks';
import { EmptyList } from './empty/emptyList';
import Experiment from './experiment';
import './experiments.less';
import { DEFAULT_FILTERS } from './filters/constants';
import PaginatedTable from './paginatedTable';

interface TableColumnProps {
  type: string;
  value: string;
  onClick: (type: string, value: string) => any;
}

function TableColumn({type, value, onClick}: TableColumnProps) {
  return (
    <span className="label-autocomplete-container">
      <span className="label label-autocomplete ">{type}:</span>
      <span className="label label-autocomplete label-autocomplete-value">
        <span>{value}</span>
        <span className="remove" onClick={() => onClick(type, value)}>
          <i className="fa fa-close icon" aria-hidden="true"/>
        </span>
      </span>
    </span>
  );
}

export interface Props {
  isCurrentUser: boolean;
  experiments: ExperimentModel[];
  groupId?: string | number;
  count: number;
  useFilters: boolean;
  bookmarks: boolean;
  onCreate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onUpdate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onDelete: (experimentName: string) => actions.ExperimentAction;
  onStop: (experimentName: string) => actions.ExperimentAction;
  bookmark: (experimentName: string) => actions.ExperimentAction;
  unbookmark: (experimentName: string) => actions.ExperimentAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.ExperimentAction;
  fetchSearches?: () => search_actions.SearchAction;
  createSearch?: (data: SearchModel) => search_actions.SearchAction;
  deleteSearch?: (searchId: number) => search_actions.SearchAction;
}

interface State {
  metrics: string[];
  declarations: string[];
  selectedValues: string[];
}

export default class Experiments extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      metrics: [],
      declarations: [],
      selectedValues: [],
    };
  }

  public shouldComponentUpdate(nextProps: Props, nextState: State) {
    const baseUrl = location.hash.split('?')[0];
    return baseUrl === '#experiments';
  }

  public addColumn = (column: string) => {
    const metrics: string[] = [];
    const declarations: string[] = [];
    const selectedValues = [...this.state.selectedValues, column];
    for (const value of selectedValues) {
      const columnValues = _.trim(value).split(':');
      if (columnValues.length > 1 && columnValues[0] === 'metric') {
        metrics.push(columnValues[1]);
      } else if (columnValues.length > 1 && columnValues[0] === 'param') {
        declarations.push(columnValues[1]);
      }
    }

    this.setState((prevState, prevProps) => ({
      ...prevState,
      ...{
        metrics,
        declarations,
        selectedValues
      }
    }));
  };

  public removeColumn = (type: string, value: string) => {
    const metrics = this.state.metrics.filter((
      item: string) => item !== value);
    const declarations = this.state.declarations.filter((
      item: string) => item !== value);
    const selectedValues = this.state.selectedValues.filter((
      item: string) => item !== `${type}:${value}`);
    this.setState((prevState, prevProps) => ({
      ...prevState,
      ...{
        metrics,
        declarations,
        selectedValues
      }
    }));
  };

  public possibleValues = () => {
    const possibleColumns: string[] = [];
    for (const experiment of this.props.experiments) {
      if (!_.isNil(experiment.last_metric)) {
        Object.keys(experiment.last_metric)
          .filter((key: string) =>
            possibleColumns.indexOf(`metric:${key}`) === -1 &&
            this.state.selectedValues.indexOf(`metric:${key}`) === -1)
          .map((key: string) => possibleColumns.push(`metric:${key}`));
      }
      if (!_.isNil(experiment.declarations)) {
        Object.keys(experiment.declarations)
          .filter((key: string) =>
            possibleColumns.indexOf(`param:${key}`) === -1 &&
            this.state.selectedValues.indexOf(`param:${key}`) === -1)
          .map((key: string) => possibleColumns.push(`param:${key}`));
      }
    }
    return possibleColumns;
  };

  public render() {
    let additionalFilters: FilterOption[] = this.props.groupId ?
      [] :
      [{filter: 'independent', type: 'scalar', desc: 'independent: true, default is false', icon: 'minus'}];
    additionalFilters = [
      ...additionalFilters,
      ...[{
        filter: 'declarations.*',
        type: 'value',
        desc: 'declarations.activation: sigmoid or declarations.activation: sigmoid|relu',
        icon: 'gear'
      },
        {
          filter: 'metric.*',
          type: 'scalar',
          desc: FILTER_EXAMPLES.scalar('metric.loss'),
          icon: 'area-chart',
        },
        {
          filter: 'group.id',
          type: 'value',
          desc: FILTER_EXAMPLES.id('group.id'),
          icon: 'cubes',
        },
        {
          filter: 'group.name',
          type: 'value',
          desc: FILTER_EXAMPLES.name('group.name'),
          icon: 'cubes',
        },
      ]] as FilterOption[];
    const filterOptions = [
      ...JOB_FILTER_OPTIONS,
      ...additionalFilters
    ] as FilterOption[];
    const sortOptions = [
      ...DEFAULT_SORT_OPTIONS,
      ...this.state.metrics.map((metric) => `metric.${metric}`),
    ];
    const filters = this.props.useFilters ? DEFAULT_FILTERS : false;
    const experiments = this.props.experiments;
    const listExperiments = () => {
      return (
        <div>
          <form className="form-horizontal form-columns">
            {this.state.declarations.map(
              (value: string, idx: number) =>
                <TableColumn
                  key={idx}
                  type="param"
                  value={value}
                  onClick={this.removeColumn}
                />
            )}
            {this.state.metrics.map(
              (value: string, idx: number) =>
                <TableColumn
                  key={idx}
                  type="metric"
                  value={value}
                  onClick={this.removeColumn}
                />
            )}
            <AutocompleteDropdown
              title="Add column"
              possibleValues={this.possibleValues()}
              selectedValues={this.state.selectedValues}
              onClick={this.addColumn}
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
            <tr className="list-header">
              <th className="top-header block" scope="colgroup" colSpan={4}/>
              {this.state.declarations.length > 0 &&
              <th
                className="top-header border-left border-right block"
                scope="colgroup"
                colSpan={this.state.declarations.length}
              > Params
              </th>}
              {this.state.metrics.length > 0 &&
              <th
                className="top-header border-left border-right block"
                scope="colgroup"
                colSpan={this.state.metrics.length}
              > Metrics
              </th>}
              <th className="top-header block" scope="colgroup" colSpan={1}/>
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
                <th
                  key={idx}
                  className={
                    'block ' +
                    (idx === 0 ? 'border-left ' : ' ') +
                    (idx === this.state.declarations.length - 1 ? 'border-right ' : ' ')}
                >
                  {declaration}
                </th>
              )}
              {this.state.metrics.map((metric: string, idx: number) =>
                <th
                  key={idx}
                  className={
                    'block ' +
                    (idx === 0 ? 'border-left ' : ' ') +
                    (idx === this.state.metrics.length - 1 ? 'border-right ' : ' ')}
                >
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
                  bookmark={() => this.props.bookmark(xp.unique_name)}
                  unbookmark={() => this.props.unbookmark(xp.unique_name)}
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
        fetchSearches={this.props.fetchSearches}
        createSearch={this.props.createSearch}
        deleteSearch={this.props.deleteSearch}
        sortOptions={sortOptions}
        filterOptions={filterOptions}
      />
    );
  }
}
