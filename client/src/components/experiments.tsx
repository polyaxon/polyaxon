import * as React from 'react';
import * as _ from 'lodash';

import Experiment from './experiment';
import { ExperimentModel } from '../models/experiment';
import * as actions from '../actions/experiment';
import PaginatedList from '../components/paginatedList';

export interface Props {
  experiments: ExperimentModel[];
  count: number;
  onCreate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onUpdate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onDelete: (experiment: ExperimentModel) => actions.ExperimentAction;
  fetchData: (currentPage: number) => actions.ExperimentAction;
}

export default class Experiments extends React.Component<Props, Object> {

  public render() {
    const experiments = this.props.experiments;
    const listExperiments = () => {
      if (experiments.length === 0) {
        return (
          <div className="row">
            <div className="col-md-offset-2 col-md-8">
              <div className="jumbotron jumbotron-action text-center">
                <h3>You don't have any experiment</h3>
                <img src="/static/images/experiment.svg" alt="experiment" className="empty-icon"/>
                <div>
                  You can start new experiment by using CLI: <b>polyaxon run --help</b>
                </div>
              </div>
            </div>
          </div>
        );
      }
      return (
        <div className="col-md-12">
          <ul>
            {experiments.filter(
              (xp: ExperimentModel) => _.isNil(xp.deleted) || !xp.deleted
            ).map(
              (xp: ExperimentModel) =>
                <li className="list-item" key={xp.unique_name}>
                  <Experiment experiment={xp} onDelete={() => this.props.onDelete(xp)}/>
                </li>)}
          </ul>
        </div>
      );
    };
    return (
      <PaginatedList
        count={this.props.count}
        componentList={listExperiments()}
        fetchData={this.props.fetchData}
      />
    );
  }
}
