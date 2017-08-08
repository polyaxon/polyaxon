import * as React from "react";
import {Button, ButtonToolbar} from "react-bootstrap";

import {ProjectModel} from "../models/project";


export interface Props {
  project: ProjectModel;
  onDelete?: (projectId: number) => any;
  fetchData?: (projectId: number) => any;
}


export default class ProjectDetail extends React.Component<Props, Object> {
  componentDidMount() {
    const {project, onDelete, fetchData} = this.props;
    fetchData(project.id);
  }

  public render() {
    const {project, onDelete, fetchData} = this.props;
    return (
      <div className="row">
        <div className="col-md-12 project">
          <h4 className="title"><a>{ project.name }</a></h4>
          <div>{ project.description }</div>
          <div className="meta">{ project.createdAt.toLocaleTimeString() }</div>
          <ButtonToolbar className="pull-right">
            <Button bsStyle="danger" className="pull-right" onClick={() => onDelete(project.id)}>delete</Button>
          </ButtonToolbar>
        </div>
      </div>
    );
  }
}
