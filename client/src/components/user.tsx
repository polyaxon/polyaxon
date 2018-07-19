import * as React from 'react';

import RootModal from '../containers/modal';
import Projects from '../containers/projects';
import { ProjectModel } from '../models/project';
import Breadcrumb from './breadcrumb';

export interface Props {
  user: string;
  showModal: () => any;
  hideModal: () => any;
}

export default class User extends React.Component<Props, Object> {
  public render() {
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb links={[{name: this.props.user}, {name: 'projects'}]}/>
          </div>
          <RootModal hideModal={this.props.hideModal}/>
          <Projects user={this.props.user}/>
        </div>
      </div>
    );
  }
}
