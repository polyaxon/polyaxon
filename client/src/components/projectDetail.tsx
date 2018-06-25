import * as React from 'react';
import * as _ from 'lodash';

import { ProjectModel } from '../models/project';
import Experiments from '../containers/experiments';
import Groups from '../containers/groups';
import Jobs from '../containers/jobs';
import Builds from '../containers/builds';
import { getUserUrl, getProjectUrl } from '../constants/utils';
import Breadcrumb from './breadcrumb';
import LinkedTab from './linkedTab';
import ProjectOverview from './projectOverview';
import ProjectInstructions from './projectInstructions';
import { EmptyList } from './emptyList';

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
      return EmptyList(false, 'project', 'project');
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
                title: 'Experiments',
                component: <Experiments user={project.user} projectName={project.unique_name}/>,
                relUrl: 'experiments'
              }, {
                title: 'Experiment groups',
                component: <Groups user={project.user} projectName={project.unique_name}/>,
                relUrl: 'groups'
              }, {
                title: 'Jobs',
                component: <Jobs user={project.user} projectName={project.unique_name}/>,
                relUrl: 'jobs'
              }, {
                title: 'Builds',
                component: <Builds user={project.user} projectName={project.unique_name}/>,
                relUrl: 'builds'
              }, {
                title: 'Instructions',
                component: <ProjectInstructions projectName={project.unique_name}/>,
                relUrl: 'instructions'
              }
            ]}
          />
        </div>
      </div>
    );
  }
}
