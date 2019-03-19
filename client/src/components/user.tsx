import * as React from 'react';

import * as actions from '../actions/project';
import Projects from '../containers/projects/projects';
import { ProjectModel } from '../models/project';
import Breadcrumb from './breadcrumb';

export interface Props {
  user: string;
  createProject: (project: ProjectModel) => actions.ProjectAction;
}

export default class User extends React.Component<Props, {}> {
  public render() {
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb links={[{name: this.props.user}, {name: 'projects'}]}/>
          </div>
          <Projects user={this.props.user}/>
        </div>
      </div>
    );
  }
}
