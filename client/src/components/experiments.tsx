import * as React from 'react';
import * as _ from 'lodash';

import Experiment from './experiment';
import { ExperimentModel } from '../models/experiment';
import * as actions from '../actions/experiment';
import PaginatedList from '../components/paginatedList';
import { EmptyList } from './emptyList';
import ExperimentHeader from './experimentHeader';

export interface Props {
  isCurrentUser: boolean;
  experiments: ExperimentModel[];
  count: number;
  onCreate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onUpdate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onDelete: (experiment: ExperimentModel) => actions.ExperimentAction;
  fetchData: (currentPage?: number, query?: string, sort?: string) => actions.ExperimentAction;
}

export default class Experiments extends React.Component<Props, Object> {

  public render() {
    const experiments = this.props.experiments;
    const listExperiments = () => {
      return (
        <ul>
          {experiments.filter(
            (xp: ExperimentModel) => _.isNil(xp.deleted) || !xp.deleted
          ).map(
            (xp: ExperimentModel) =>
              <li className="list-item" key={xp.unique_name}>
                <Experiment experiment={xp} onDelete={() => this.props.onDelete(xp)}/>
              </li>)}
        </ul>
      );
    };
    return (
      <PaginatedList
        count={this.props.count}
        componentList={listExperiments()}
        componentHeader={ExperimentHeader()}
        componentEmpty={EmptyList(
          this.props.isCurrentUser,
          'experiment',
          'experiment',
          'polyaxon run --help')
        }
        enableFilters={true}
        fetchData={this.props.fetchData}
      />
    )
      ;
  }
}
