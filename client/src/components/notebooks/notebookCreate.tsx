import * as React from 'react';

import * as projectsActions from '../../actions/projects';
import { getProjectUrl, getUserUrl } from '../../constants/utils';
import { NotebookModel } from '../../models/notebook';
import { ProjectModel } from '../../models/project';
import LinkedTab from '../linkedTab';
import NotebookCreateFull from './creationModes/full';
import NotebookCreateQuick from './creationModes/quick';
import NotebookCreateTemplate from './creationModes/template';

export interface Props {
  user: string;
  projectName: string;
  isLoading: boolean;
  isProjectEntity: boolean;
  projects: ProjectModel[];
  errors: any;
  onCreate: (notebook: NotebookModel, user?: string, projectName?: string) => projectsActions.ProjectAction;
  fetchProjects: (user: string) => projectsActions.ProjectAction;
}

export default class NotebookCreate extends React.Component<Props, {}> {

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
      baseUrl = projectUrl + '/notebooks/new';
    } else {
      cancelUrl = getUserUrl(this.props.user);
      baseUrl = '/app/notebooks/new';
    }
    return (
      <div className="row form-full-page">
        <div className="col-md-3">
          <h3 className="form-title">New Notebook</h3>
          <p>
            You can create Jupyter Notebooks or Jupyter Labs to explore data, try out new ideas and experiments.
          </p>
          <p>
            Jupyter Notebooks/Labs are created on a project level, and will give you access to project's linked code.
          </p>
          <p>
            <strong>Tip:</strong> You can use Polyaxon CLI to create & stop Notebooks as well.
          </p>
        </div>
        <div className="col-md-offset-1 col-md-8">
          <LinkedTab
            baseUrl={baseUrl}
            tabs={[
              {
                title: 'Quick Mode',
                component: <NotebookCreateQuick
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
                component: <NotebookCreateFull
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
                component: <NotebookCreateTemplate
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
