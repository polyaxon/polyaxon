import * as React from "react";
import * as _ from "lodash";

import {ProjectModel} from "../models/project";
import Experiments from "../containers/experiments";
import Groups from "../containers/groups";


export interface Props {
  project: ProjectModel;
  onDelete: (project: ProjectModel) => any;
  fetchData: () => any;
}


export default class ProjectDetail extends React.Component<Props, Object> {
  componentDidMount() {
    const {project, onDelete, fetchData} = this.props;
    fetchData();
  }

  public render() {
    const {project, onDelete, fetchData} = this.props;
    if (_.isNil(project)) {
      return (<div>Nothing</div>);
    }
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <a className="back-button" onClick={() => {window.history.back()}}>&#060;</a>
            <span className="title">
              <i className="fa fa-cubes icon" aria-hidden="true"></i>
              {project.name}
            </span>
            <span className="results-info">({project.num_experiments} experiments found)</span>
            <span className="description">
              {project.description}
            </span>
          </div>
          <h4 className="polyaxon-header">Experiment groups</h4>
          <Groups fetchData={() => null} user={project.user} projectName={project.unique_name}></Groups>
          <h4 className="polyaxon-header">Independent Experiments</h4>
          <Experiments fetchData={() => null} user={project.user} projectName={project.unique_name} groupUuid={null}></Experiments>
        </div>
      </div>
    );
  }
}
