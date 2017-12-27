import * as React from "react";
import * as _ from "lodash";
import {Button, ButtonToolbar} from "react-bootstrap";
import {LinkContainer} from "react-router-bootstrap";

import Experiment from "./experiment";
import {ExperimentModel} from "../models/experiment";
import {ProjectModel} from "../models/project";


export interface Props {
  experiments: ExperimentModel[];
  project: ProjectModel;
  onCreate: (experiment: ExperimentModel) => any;
  onUpdate: (experiment: ExperimentModel) => any;
  onDelete: (experimentUuid: string) => any;
  fetchProjectsData: () => any
  fetchExperimentsData: () => any
}


export default class Experiments extends React.Component<Props, Object> {
  componentDidMount() {
    const {experiments, project, onCreate, onUpdate, onDelete, fetchProjectsData, fetchExperimentsData} = this.props;
    fetchProjectsData();
    fetchExperimentsData();
  }

  public render() {
    const {experiments, project, onCreate, onUpdate, onDelete, fetchProjectsData, fetchExperimentsData} = this.props;
    return (
      <div className="row">
        <div className="col-md-12">
          <h3>
            <Button bsStyle="primary" onClick={() => {window.history.back()}}>Back</Button>
            &nbsp;{project.name}: Experiments ({experiments.length} found)
          </h3>
          <ul>
            {experiments.filter(
              (xp: ExperimentModel) => _.isNil(xp.deleted) || !xp.deleted
            ).map(
              (xp: ExperimentModel) => <li className="list-item" key={xp.uuid}><Experiment experiment={xp} onDelete={() => onDelete(xp.uuid)}/></li>)}
          </ul>
        </div>
      </div>
    );
  }
}
