import * as React from 'react';
import * as _ from 'lodash';

import Experiment from './experiment';
import { ExperimentModel } from '../models/experiment';
import * as actions from '../actions/experiment';

export interface Props {
  experiments: ExperimentModel[];
  currentPage: number;
  onCreate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onUpdate: (experiment: ExperimentModel) => actions.ExperimentAction;
  onDelete: (experiment: ExperimentModel) => actions.ExperimentAction;
  fetchData: () => actions.ExperimentAction;
}

export default class Experiments extends React.Component<Props, Object> {
  componentDidMount() {
    const {experiments, currentPage, onCreate, onUpdate, onDelete, fetchData} = this.props;
    fetchData();
  }

  componentDidUpdate(prevProps: Props) {
    if (this.props.currentPage !== prevProps.currentPage) {
      this.props.fetchData();
    }
  }

  public render() {
    const {experiments, currentPage, onCreate, onUpdate, onDelete, fetchData} = this.props;
    return (
      <div className="row">
        <div className="col-md-12">
          <ul>
            {experiments.filter(
              (xp: ExperimentModel) => _.isNil(xp.deleted) || !xp.deleted
            ).map(
              (xp: ExperimentModel) =>
                <li className="list-item" key={xp.unique_name}>
                  <Experiment experiment={xp} onDelete={() => onDelete(xp)}/>
                </li>)}
          </ul>
        </div>
      </div>
    );
  }
}
