import * as React from 'react';
import * as _ from 'lodash';

import { ProjectModel } from '../models/project';
import Experiments from '../containers/experiments';
import Groups from '../containers/groups';
import { getUserUrl, getProjectUrl } from '../constants/utils';
import Breadcrumb from './breadcrumb';
import LinkedTab from './linkedTab';
import ProjectOverview from './projectOverview';

export interface Props {
  project: ProjectModel;
  onDelete: (project: ProjectModel) => undefined;
  fetchData: () => undefined;
}

export default class ProjectDetail extends React.Component<Props, Object> {
  componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const project = this.props.project;
    if (_.isNil(project)) {
      return (<div>Nothing</div>);
    }
    let projectUrl = getProjectUrl(project.user, project.name);

    return (
      <div className="row">
        <div className="col-md-12">
          <Breadcrumb
            icon="fa-server"
            links={[
              {name: project.user, value: getUserUrl(project.user)},
              {name: project.name}]}
          />
          <LinkedTab
            baseUrl={projectUrl}
            tabs={[
            {
              title: 'Overview',
              component: <ProjectOverview project={project}/>,
              relUrl: ''
            }, {
              title: 'Independent Experiments',
              component: <Experiments user={project.user} projectName={project.unique_name}/>,
              relUrl: 'experiments'
            }, {
              title: 'Experiment groups',
              component: <Groups user={project.user} projectName={project.unique_name}/>,
              relUrl: 'groups'
            }
          ]}
          />
        </div>
      </div>
    );
  }
}
