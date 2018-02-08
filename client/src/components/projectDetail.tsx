import * as React from 'react';
import * as _ from 'lodash';
import * as moment from 'moment';
import { Tab, Tabs } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

import { ProjectModel } from '../models/project';
import Experiments from '../containers/experiments';
import Groups from '../containers/groups';
import { getUserUrl } from '../constants/utils';

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
    let visibility = project.is_public ? 'Public' : 'Private';
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <span className="title">
              <i className="fa fa-server icon" aria-hidden="true"/>
              <LinkContainer to={getUserUrl(project.user)}>
                <span>
                  <a className="title">
                    {project.user}
                  </a>/
                </span>
              </LinkContainer>
              <span className="title">
                {project.name}
              </span>
            </span>
            <div className="meta-description">
              {project.description}
            </div>
            <div className="meta">
              <span className="meta-info">
                <i className="fa fa-lock icon" aria-hidden="true"/>
                <span className="title">Visibility:</span>
                {visibility}
              </span>
              <span className="meta-info">
                <i className="fa fa-clock-o icon" aria-hidden="true"/>
                <span className="title">Last updated:</span>
                {moment(project.updated_at).fromNow()}
              </span>
              <span className="meta-info">
                <i className="fa fa-cube icon" aria-hidden="true"/>
                <span className="title">Experiments:</span>
                {project.num_experiments}
              </span>
              <span className="meta-info">
                <i className="fa fa-cubes icon" aria-hidden="true"/>
                <span className="title">Experiment Groups:</span>
                {project.num_experiment_groups}
              </span>
            </div>
          </div>
          <Tabs defaultActiveKey={1} id="uncontrolled-tab-example" className="plx-nav">
            <Tab eventKey={1} title="Independent Experiments">
              <Experiments fetchData={() => null} user={project.user} projectName={project.unique_name}/>
            </Tab>
            <Tab eventKey={2} title="Experiment groups">
              <Groups fetchData={() => null} user={project.user} projectName={project.unique_name}/>
            </Tab>
          </Tabs>
        </div>
      </div>
    );
  }
}
