import * as React from 'react';

import * as experimentsActions from '../../actions/experiments';
import * as groupsActions from '../../actions/groups';
import * as projectsActions from '../../actions/projects';
import { ProjectModel } from '../../models/project';
import { TensorboardModel } from '../../models/tensorboard';
import { newTensorboardUrl } from '../../urls/routes/new';
import { getExperimentUrl, getGroupUrl, getProjectUrl, getUserUrl } from '../../urls/utils';
import LinkedTab from '../linkedTab';
import TensorboardCreateFull from './creationModes/full';
import TensorboardCreateQuick from './creationModes/quick';
import TensorboardCreateTemplate from './creationModes/template';

export interface Props {
  user: string;
  projectName: string;
  groupId: string;
  experimentId: string;
  isLoading: boolean;
  isProjectEntity: boolean;
  projects: ProjectModel[];
  errors: any;
  onCreate: (tensorboard: TensorboardModel, user?: string, projectName?: string) =>
    experimentsActions.ExperimentAction
    | groupsActions.GroupAction
    | projectsActions.ProjectAction;
  fetchProjects: (user: string) => projectsActions.ProjectAction;
}

export default class TensorboardCreate extends React.Component<Props, {}> {

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
      baseUrl = projectUrl + '/tensorboards/new';
      if (this.props.experimentId) {
        const experimentUrl = getExperimentUrl(this.props.user, this.props.projectName, this.props.experimentId);
        cancelUrl = experimentUrl;
        baseUrl = experimentUrl + '/tensorboards/new';
      } else if (this.props.groupId) {
        const groupUrl = getGroupUrl(this.props.user, this.props.projectName, this.props.groupId);
        cancelUrl = groupUrl;
        baseUrl = groupUrl + '/tensorboards/new';
      }
    } else {
      cancelUrl = getUserUrl(this.props.user);
      baseUrl = newTensorboardUrl;
    }

    return (
      <div className="row form-full-page">
        <div className="col-md-3">
          <h3 className="form-title">New Tensorboard</h3>
          <p>
            You can use TensorBoard to visualize your experiments' graph,
            plot quantitative metrics about the execution
            of your graph, and show additional data like images that pass through it.
          </p>
          <div>
            You can create a tensorboard to:
            <ul>
              <li>To visualize all metrics of all experiments under a project.</li>
              <li>To visualize all metrics of all experiments under a group or selection.</li>
              <li>To visualize all metrics of a particular experiment.</li>
            </ul>
          </div>
          <p>
            <strong>Tip:</strong> You can use Polyaxon CLI to create & stop tensorboards as well.
          </p>
        </div>
        <div className="col-md-offset-1 col-md-8">
          <LinkedTab
            baseUrl={baseUrl}
            tabs={[
              {
                title: 'Quick Mode',
                component: <TensorboardCreateQuick
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
                component: <TensorboardCreateFull
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
                component: <TensorboardCreateTemplate
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
