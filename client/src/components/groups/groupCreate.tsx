import * as React from 'react';

import * as groupsActions from '../../actions/groups';
import * as projectsActions from '../../actions/projects';
import { getProjectUrl, getUserUrl, splitUniqueName } from '../../constants/utils';
import { GroupModel } from '../../models/group';
import { ProjectModel } from '../../models/project';
import { BaseState, sanitizeForm } from '../forms';
import LinkedTab from '../linkedTab';
import GroupCreateFull from './creationModes/full';
import GroupCreateTemplate from './creationModes/template';

export interface Props {
  user: string;
  projectName: string;
  isLoading: boolean;
  isProjectEntity: boolean;
  projects: ProjectModel[];
  errors: any;
  onCreate: (group: GroupModel, user?: string, projectName?: string) => groupsActions.GroupAction;
  fetchProjects: (user: string) => projectsActions.ProjectAction;
}

export interface State extends BaseState {
  config: string;
}

export default class GroupCreate extends React.Component<Props, {}> {

  public componentDidMount() {
    if (this.props.isProjectEntity) {
      this.props.fetchProjects(this.props.user);
    }
  }

  public createGroup = (state: State) => {
    const form = sanitizeForm({
      tags: state.tags.map((v) => v.value),
      readme: state.readme,
      description: state.description,
      name: state.name,
      content: state.config
    }) as GroupModel;

    if (this.props.isProjectEntity) {
      const values = splitUniqueName(state.project);
      this.props.onCreate(form, values[0], values[1]);
    } else {
      this.props.onCreate(form);
    }
  };

  public render() {
    let cancelUrl = '';
    let baseUrl = '';
    if (this.props.projectName) {
      const projectUrl = getProjectUrl(this.props.user, this.props.projectName);
      cancelUrl = projectUrl;
      baseUrl = projectUrl + '/groups/new';
    } else {
      cancelUrl = getUserUrl(this.props.user);
      baseUrl = '/app/groups/new';
    }
    return (
      <div className="row form-full-page">
        <div className="col-md-3">
          <h3 className="form-title">New Group</h3>
          <p>
            You can create Experiment Groups to search a large space of hyperparams.
            Polyaxon's built-in AutoML service allows you to speed up
            to optimize your models and effectively use your cluster's resources.
          </p>
          <p>
            Polyaxon provides different algorithms and distributions to create groups,
            you can check our documentation to learn more.
          </p>
          <p>
            <strong>Tip:</strong> You can use Polyaxon CLI to create & stop Groups as well.
          </p>
          <p>
            <strong>Tip:</strong> If you only need to compare experiments,
            you can go the project's experiments table and create a group selection.
          </p>
        </div>
        <div className="col-md-offset-1 col-md-8">
          <LinkedTab
            baseUrl={baseUrl}
            tabs={[
              {
                title: 'Create with Polyaxonfile',
                component: <GroupCreateFull
                  cancelUrl={cancelUrl}
                  isLoading={this.props.isLoading}
                  isProjectEntity={this.props.isProjectEntity}
                  projects={this.props.projects}
                  errors={this.props.errors}
                  onCreate={this.props.onCreate}
                />,
                relUrl: ''
              }, {
                title: 'Create from templates',
                component: <GroupCreateTemplate
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
