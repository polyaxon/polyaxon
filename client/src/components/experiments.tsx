import * as React from "react";

import Experiment from "./experiment";
import {ExperimentModel} from "../models/experiment";

export interface Props {
  experiments: ExperimentModel[];
  onCreate?: (experiment: ExperimentModel) => any;
  onUpdate?: (experiment: ExperimentModel) => any;
  onDelete?: (experimentId: number) => any;
  fetchData: () => any
}


export default class Experiments extends React.Component<Props, Object> {
  componentDidMount() {
    const {experiments, onCreate, onUpdate, onDelete, fetchData} = this.props;
    fetchData();
  }

  public render() {
    const {experiments, onCreate, onUpdate, onDelete, fetchData} = this.props;
    return (
      <div className="row">
        <div className="col-md-12 ">
          <ul>
            {experiments.map(xp => <li className="list-item" key={xp.id}><Experiment experiment={xp} onDelete={() => onDelete(xp.id)}/></li>)}
          </ul>
        </div>
      </div>
    );
  }
}
