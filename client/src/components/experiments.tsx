import * as React from 'react';

import * as actions from '../actions/experiment';
import { ExperimentModel } from '../models/experiment';
import { EmptyBookmarks } from './empty/emptyBookmarks';
import { EmptyList } from './empty/emptyList';
import Experiment from './experiment';
import ExperimentHeader from './experimentHeader';
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

export default class Experiments extends React.Component<Props, Object> {
  public shouldComponentUpdate(nextProps: Props, nextState: Object) {
    const baseUrl = location.hash.split('?')[0];
    return baseUrl === '#experiments';
  }

  public render() {
    const filters = this.props.useFilters ? EXPERIMENT_FILTERS : false;
    const experiments = this.props.experiments;
    const listExperiments = () => {
      return (
          <tbody>
          {ExperimentHeader()}
          {experiments.map(
            (xp: ExperimentModel) =>
              <Experiment
                key={xp.unique_name}
                experiment={xp}
                onDelete={() => this.props.onDelete(xp.unique_name)}
                onStop={() => this.props.onStop(xp.unique_name)}
              />)}
          </tbody>
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
