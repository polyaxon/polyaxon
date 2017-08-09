import * as React from "react";
import * as _ from "lodash";
import {Button, ButtonToolbar} from "react-bootstrap";

import {ProjectModel} from "../models/project";
import Experiments from "../containers/experiments";


export interface Props {
  project: ProjectModel;
  onDelete: () => any;
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
        <div className="col-md-12 project">
          <h4 className="title"><a>{ project.name }</a></h4>
          <div>{ project.description }</div>
          <div className="meta">{ project.createdAt.toLocaleTimeString() }</div>
          <ButtonToolbar className="pull-right">
            <Button bsStyle="danger" className="pull-right" onClick={() => onDelete()}>delete</Button>
          </ButtonToolbar>
          <Experiments fetchData={() => null} projectId={project.id}></Experiments>
        </div>
      </div>
    );
  }
}
