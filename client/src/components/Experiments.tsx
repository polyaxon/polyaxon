import * as React from "react";

import Experiment from "./Experiment";
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
      <ul>
        {experiments.map(xp => <li key={xp.id}><Experiment experiment={xp} onDelete={() => onDelete(xp.id)}/></li>)}
      </ul>
    );
  }
}
