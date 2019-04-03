import * as React from 'react';

import * as experimentsActions from '../../actions/experiments';
import * as projectsActions from '../../actions/projects';
import { getProjectUrl, getUserUrl } from '../../constants/utils';
import { ExperimentModel } from '../../models/experiment';
import { ProjectModel } from '../../models/project';
import { BaseState } from '../forms';
import LinkedTab from '../linkedTab';
import ExperimentCreateFull from './creationModes/full';
import ExperimentCreateQuick from './creationModes/quick';
import ExperimentCreateTemplate from './creationModes/template';

export interface Props {
  user: string;
  projectName: string;
  isLoading: boolean;
  isProjectEntity: boolean;
  projects: ProjectModel[];
  errors: any;
  onCreate: (experiment: ExperimentModel, user?: string, projectName?: string) => experimentsActions.ExperimentAction;
  fetchProjects: (user: string) => projectsActions.ProjectAction;
}

export interface State extends BaseState {
  config: string;
}

export default class ExperimentCreate extends React.Component<Props, {}> {

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
      baseUrl = projectUrl + '/experiments/new';
    } else {
      cancelUrl = getUserUrl(this.props.user);
      baseUrl = '/app/experiments/new';
    }
    return (
      <div className="row form-full-page">
        <div className="col-md-3">
          <h3 className="form-title">New Experiment</h3>
          <p>
            You can create Experiments to solve a problem.
            To speed up the learning process you can start a distributed experiment or
            use Polyaxon's built-in AutoML service to search a large space of hyperparams.
          </p>
          <p>
            Polyaxon provides different ways and backends to create experiments,
            you can check our documentation to learn more.
          </p>
          <p>
            <strong>Tip:</strong> You can use Polyaxon CLI to create & stop Experiments as well.
          </p>
        </div>
        <div className="col-md-offset-1 col-md-8">
          <LinkedTab
            baseUrl={baseUrl}
            tabs={[
              {
                title: 'Quick Mode',
                component: <ExperimentCreateQuick
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
                component: <ExperimentCreateFull
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
                component: <ExperimentCreateTemplate
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
