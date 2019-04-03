import * as React from 'react';

import * as buildsActions from '../../actions/builds';
import * as projectsActions from '../../actions/projects';
import { getProjectUrl, getUserUrl } from '../../constants/utils';
import { BuildModel } from '../../models/build';
import { ProjectModel } from '../../models/project';
import LinkedTab from '../linkedTab';
import BuildCreateFull from './creationModes/full';
import BuildCreateQuick from './creationModes/quick';
import BuildCreateTemplate from './creationModes/template';

export interface Props {
  user: string;
  projectName: string;
  isLoading: boolean;
  isProjectEntity: boolean;
  projects: ProjectModel[];
  errors: any;
  onCreate: (build: BuildModel, user?: string, projectName?: string) => buildsActions.BuildAction;
  fetchProjects: (user: string) => projectsActions.ProjectAction;
}

export default class BuildCreate extends React.Component<Props, {}> {

  public componentDidMount() {
    if (this.props.isProjectEntity) {
      this.props.fetchProjects(this.props.user);
    }
  }

  public render() {
    let cancelUrl = '';
    let baseUrl = '';
    if (this.props.projectName) {
      const projectUrl = getProjectUrl(this.props.user, this.props.projectName);
      cancelUrl = projectUrl;
      baseUrl = projectUrl + '/builds/new';
    } else {
      cancelUrl = getUserUrl(this.props.user);
      baseUrl = '/app/builds/new';
    }
    return (
      <div className="row form-full-page">
        <div className="col-md-3">
          <h3 className="form-title">New Build</h3>
          <p>
            You can create Builds to run your jobs, experiment, notebooks, ...
          </p>
          <p>
            Polyaxon provides different ways and backends to create builds,
            you can check our documentation to learn more.
          </p>
          <p>
            <strong>Tip:</strong> You can use Polyaxon CLI to create & stop Builds as well.
          </p>
        </div>
        <div className="col-md-offset-1 col-md-8">
          <LinkedTab
            baseUrl={baseUrl}
            tabs={[
              {
                title: 'Quick Mode',
                component: <BuildCreateQuick
                  cancelUrl={cancelUrl}
                  isLoading={this.props.isLoading}
                  isProjectEntity={this.props.isProjectEntity}
                  projects={this.props.projects}
                  errors={this.props.errors}
                  onCreate={this.props.onCreate}
                />,
                relUrl: ''
              }, {
                title: 'Create with Polyaxonfile',
                component: <BuildCreateFull
                  cancelUrl={cancelUrl}
                  isLoading={this.props.isLoading}
                  isProjectEntity={this.props.isProjectEntity}
                  projects={this.props.projects}
                  errors={this.props.errors}
                  onCreate={this.props.onCreate}
                />,
                relUrl: 'config'
              }, {
                title: 'Create from templates',
                component: <BuildCreateTemplate
                  cancelUrl={cancelUrl}
                  isLoading={this.props.isLoading}
                  isProjectEntity={this.props.isProjectEntity}
                  projects={this.props.projects}
                  errors={this.props.errors}
                  onCreate={this.props.onCreate}
                />,
                relUrl: 'templates'
              },
            ]}
          />
        </div>
      </div>
    );
  }
}
