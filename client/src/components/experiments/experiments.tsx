import * as _ from 'lodash';
import * as React from 'react';
import { Modal } from 'react-bootstrap';

import * as actions from '../../actions/experiment';
import * as groupActions from '../../actions/group';
import * as searchActions from '../../actions/search';
import { FILTER_EXAMPLES, JOB_FILTER_OPTIONS } from '../../constants/filtering';
import { DEFAULT_SORT_OPTIONS } from '../../constants/sorting';
import { isDone } from '../../constants/statuses';
import { FilterOption } from '../../interfaces/filterOptions';
import { ExperimentModel } from '../../models/experiment';
import { GroupModel } from '../../models/group';
import { SearchModel } from '../../models/search';
import { ARCHIVES, BOOKMARKS } from '../../utils/endpointList';
import { isLive } from '../../utils/isLive';
import AutocompleteLabel from '../autocomplete/autocompleteLabel';
import AutocompleteDropdown from '../autocomplete/autocomplteDorpdown';
import { EmptyArchives } from '../empty/emptyArchives';
import { EmptyBookmarks } from '../empty/emptyBookmarks';
import { EmptyList } from '../empty/emptyList';
import { DEFAULT_FILTERS } from '../filters/constants';
import PaginatedTable from '../tables/paginatedTable';
import Experiment from './experiment';
import ExperimentActions from './experimentActions';

import './experiments.less';

export interface Props {
  isCurrentUser: boolean;
  experiments: ExperimentModel[];
  groupId?: number;
  isSelection?: boolean;
  count: number;
  useFilters: boolean;
  showBookmarks: boolean;
  showDeleted: boolean;
  useCheckbox: boolean;
  endpointList?: string;
  onCreate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onUpdate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onDelete: (experimentName: string) => actions.ExperimentAction;
  onDeleteMany: (experimentIds: number[]) => actions.ExperimentAction;
  onStop: (experimentName: string) => actions.ExperimentAction;
  onArchive: (experimentName: string) => actions.ExperimentAction;
  onRestore: (experimentName: string) => actions.ExperimentAction;
  onStopMany: (experimentIds: number[]) => actions.ExperimentAction;
  bookmark: (experimentName: string) => actions.ExperimentAction;
  unbookmark: (experimentName: string) => actions.ExperimentAction;
  fetchData: (offset?: number, query?: string, sort?: string) => actions.ExperimentAction;
  fetchSearches: () => searchActions.SearchAction;
  createSearch: (data: SearchModel) => searchActions.SearchAction;
  deleteSearch: (searchId: number) => searchActions.SearchAction;
  createSelection: (data: GroupModel) => groupActions.GroupAction;
  addToSelection: (selectionId: number, items: number[]) => groupActions.GroupAction;
  removeFromSelection: (selectionId: number, items: number[]) => groupActions.GroupAction;
}

interface State {
  metrics: string[];
  declarations: string[];
  selectedValues: string[];
  items: number[];
  allItems: boolean;
  showCreateSelectionModal: boolean;
  showAddSelectionModal: boolean;
  group: GroupModel;
  selectionId: number;
}

export default class Experiments extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      metrics: [],
      declarations: [],
      selectedValues: [],
      items: [],
      allItems: false,
      showAddSelectionModal: false,
      showCreateSelectionModal: false,
      group: {} as GroupModel,
      selectionId: -1,
    };
  }

  public componentWillReceiveProps(nextProps: Props) {
    const experimentIds = nextProps.experiments.map((xp: ExperimentModel) => xp.id);
    this.setState((prevState, prevProps) => ({
      ...prevState,
      ...{
        items: prevState.items.filter((item: number) => experimentIds.indexOf(item) !== -1),
        allItems: false,
      }
    }));
  }

  public shouldComponentUpdate(nextProps: Props, nextState: State) {
    const baseUrl = location.hash.split('?')[0];
    return baseUrl === '#experiments' || (this.props.endpointList !== '' && baseUrl === '');
  }

  public selectAll = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      ...{
        items: prevState.allItems
          ? []
          : this.props.experiments.map((xp: ExperimentModel) => xp.id),
        allItems: !prevState.allItems,
      }
    }));
  };

  public selectHandler = (itemId: number) => {
    const items = (this.state.items.indexOf(itemId) > -1)
      ? this.state.items.filter((id: number) => id !== itemId)
      : [...this.state.items, itemId];
    this.setState((prevState, prevProps) => ({
      ...prevState,
      ...{
        items,
        allItems: false,
      }
    }));
  };

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

  public removeColumn = (value: string, type: string) => {
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

  public selectSearch = (search: SearchModel) => {
    const selectedValues = (_.isNil(search.meta) || _.isNil(search.meta.columns)) ? [] : search.meta.columns;
    const metrics: string[] = [];
    const declarations: string[] = [];
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

  public handleClose = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState, showAddSelectionModal: false, showCreateSelectionModal: false
    }));
  };

  public handleShow = (type: 'showAddSelectionModal' | 'showCreateSelectionModal') => {
    const updateState = {showAddSelectionModal: false, showCreateSelectionModal: false};
    updateState[type] = true;
    this.setState((prevState, prevProps) => ({
      ...prevState, ...updateState
    }));
  };

  public createSelection = (event: any) => {
    event.preventDefault();
    if (this.props.createSelection) {
      const group = {...this.state.group, experiment_ids: this.state.items};
      this.props.createSelection(group);
    }
    this.handleClose();
  };

  public addToSelection = (event: any) => {
    event.preventDefault();
    if (this.props.addToSelection) {
      this.props.addToSelection(this.state.selectionId, this.state.items);
    }
    this.handleClose();
  };

  public removeFromSelection = (items: number[]) => {
    if (this.props.removeFromSelection && this.props.groupId) {
      this.props.removeFromSelection(this.props.groupId, items);
    }
    this.handleClose();
  };

  public setSelectionGroup = (selectionId: string) => {
    this.setState((prevState, prevProps) => ({
      ...prevState, selectionId: parseInt(selectionId, 10)
    }));
  };

  public updateSelectionForm = (key: string, value: string) => {
    let updated = false;
    const group = {...this.state.group};
    if (key === 'name') {
      group.name = value;
      updated = true;
    } else if (key === 'description') {
      group.description = value;
      updated = true;
    }
    if (updated) {
      this.setState((prevState, prevProps) => ({
        ...prevState, group
      }));
    }
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
    const experimentActions = [
      {
        name: 'Create selection',
        icon: 'download',
        callback: () => this.handleShow('showCreateSelectionModal')
      },
      {
        name: 'Add to selection',
        icon: 'plus',
        callback: () => this.handleShow('showAddSelectionModal')
      },
    ];
    if (this.props.groupId && this.props.isSelection) {
      experimentActions.push({
        name: 'Remove from selection',
        icon: 'minus',
        callback: () => this.removeFromSelection(this.state.items)
      });
    }
    const filters = this.props.useFilters ? DEFAULT_FILTERS : false;
    const listExperiments = () => {
      return (
        <div>
          <form className="form-horizontal form-columns">
            {this.state.declarations.map(
              (value: string, idx: number) =>
                <AutocompleteLabel
                  key={idx}
                  type="param"
                  value={value}
                  onClick={this.removeColumn}
                />
            )}
            {this.state.metrics.map(
              (value: string, idx: number) =>
                <AutocompleteLabel
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
            <colgroup span={this.props.useCheckbox ? 5 : 4}/>
            <colgroup span={1}/>
            <colgroup span={1}/>
            {this.state.metrics.length > 0 && <colgroup span={this.state.metrics.length}/>}
            {this.state.declarations.length > 0 && <colgroup span={this.state.declarations.length}/>}
            <colgroup span={1}/>
            <tbody>
            {(this.state.metrics.length > 0 || this.state.declarations.length > 0) &&
            <tr className="list-header">
              <th className="top-header block" scope="colgroup" colSpan={5}/>
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
              {this.props.useCheckbox &&
              <th className="block">
                <input type="checkbox" checked={this.state.allItems} onClick={this.selectAll}/>
              </th>
              }
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
                {this.props.useCheckbox && this.state.items.length > 0
                  ? <ExperimentActions
                    onDelete={() => this.props.onDeleteMany(this.state.items)}
                    onStop={() => this.props.onStopMany(this.state.items)}
                    isRunning={this.props.experiments.filter(
                      (xp: ExperimentModel) => this.state.items.indexOf(xp.id) > -1
                    ).filter(
                      (xp: ExperimentModel) => !isDone(xp.last_status)
                    ).length > 0
                    }
                    pullRight={false}
                    isSelection={true}
                    actions={experimentActions}
                  />
                  : 'actions'
                }
              </th>
            </tr>
            {this.props.experiments
              .filter(
                (xp: ExperimentModel) =>
                  (!this.props.showDeleted && isLive(xp)) || (this.props.showDeleted && !isLive(xp)))
              .map(
                (xp: ExperimentModel) =>
                <Experiment
                  key={xp.unique_name}
                  experiment={xp}
                  declarations={this.state.declarations}
                  metrics={this.state.metrics}
                  onDelete={() => this.props.onDelete(xp.unique_name)}
                  onStop={() => this.props.onStop(xp.unique_name)}
                  onArchive={() => this.props.onArchive(xp.unique_name)}
                  onRestore={() => this.props.onRestore((xp.unique_name))}
                  showBookmarks={this.props.showBookmarks}
                  useCheckbox={this.props.useCheckbox}
                  bookmark={() => this.props.bookmark(xp.unique_name)}
                  unbookmark={() => this.props.unbookmark(xp.unique_name)}
                  selectHandler={() => this.selectHandler(xp.id)}
                  selected={this.state.items.indexOf(xp.id) > -1}
                  reducedForm={(this.state.metrics.length + this.state.declarations.length) > 4}
                  removeFromSelection={
                    this.props.groupId && this.props.isSelection
                      ? () => this.removeFromSelection([xp.id])
                      : undefined
                  }
                />)}
            </tbody>
          </table>
          {createSelectionModal}
          {addToSelectionModal}
        </div>
      );
    };

    const addToSelectionModal = (
      <Modal show={this.state.showAddSelectionModal} onHide={this.handleClose}>
        <Modal.Header closeButton={true}>
          <Modal.Title>Save Selection</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form className="form-horizontal" onSubmit={this.addToSelection}>
            <div className="form-group">
              <label className="col-sm-2 control-label">Selection (group_id)</label>
              <div className="col-sm-10">
                <input
                  type="text"
                  className="form-control"
                  onChange={(event) => this.setSelectionGroup(event.target.value)}
                />
              </div>
            </div>
            <div className="form-group">
              <div className="col-sm-offset-2 col-sm-10">
                <button type="submit" className="btn btn-default" onClick={this.addToSelection}>Save</button>
              </div>
            </div>
          </form>
        </Modal.Body>
      </Modal>
    );

    const createSelectionModal = (
      <Modal show={this.state.showCreateSelectionModal} onHide={this.handleClose}>
        <Modal.Header closeButton={true}>
          <Modal.Title>Save Selection</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <form className="form-horizontal" onSubmit={this.createSelection}>
            <div className="form-group">
              <label className="col-sm-2 control-label">Name</label>
              <div className="col-sm-10">
                <input
                  type="text"
                  className="form-control"
                  onChange={(event) => this.updateSelectionForm('name', event.target.value)}
                />
                <span id="helpBlock" className="help-block">The name must be a slug.</span>
              </div>
            </div>
            <div className="form-group">
              <label className="col-sm-2 control-label">Description</label>
              <div className="col-sm-10">
                <input
                  type="text"
                  className="form-control"
                  onChange={(event) => this.updateSelectionForm('description', event.target.value)}
                />
              </div>
            </div>
            <div className="form-group">
              <div className="col-sm-offset-2 col-sm-10">
                <button type="submit" className="btn btn-default" onClick={this.createSelection}>Save</button>
              </div>
            </div>
          </form>
        </Modal.Body>
      </Modal>
    );

    let empty: any;
    if (this.props.endpointList === BOOKMARKS) {
      empty = EmptyBookmarks(
        this.props.isCurrentUser,
        'experiment',
        'experiment');
    } else if (this.props.endpointList === ARCHIVES) {
       empty = EmptyArchives(
        this.props.isCurrentUser,
        'experiment',
        'experiment');
    } else {
      empty = EmptyList(
        this.props.isCurrentUser,
        'experiment',
        'experiment',
        'polyaxon run --help');
    }
    return (
      <PaginatedTable
        count={this.props.count}
        componentList={listExperiments()}
        componentEmpty={empty}
        filters={filters}
        fetchData={this.props.fetchData}
        fetchSearches={this.props.fetchSearches}
        createSearch={(data: SearchModel) => {
          data.meta = {columns: this.state.selectedValues};
          return this.props.createSearch(data);
        }}
        deleteSearch={this.props.deleteSearch}
        selectSearch={this.selectSearch}
        sortOptions={sortOptions}
        filterOptions={filterOptions}
      />
    );
  }
}
