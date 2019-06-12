import * as React from 'react';

import * as jobsActions from '../../actions/jobs';
import * as projectsActions from '../../actions/projects';
import { JobModel } from '../../models/job';
import { ProjectModel } from '../../models/project';
import { getProjectUrl, getUserUrl } from '../../urls/utils';
import LinkedTab from '../linkedTab';
import JobCreateFull from './creationModes/full';
import JobCreateQuick from './creationModes/quick';
import JobCreateTemplate from './creationModes/template';

export interface Props {
  user: string;
  projectName: string;
  isLoading: boolean;
  isProjectEntity: boolean;
  projects: ProjectModel[];
  errors: any;
  onCreate: (job: JobModel, user?: string, projectName?: string) => jobsActions.JobAction;
  fetchProjects: (user: string) => projectsActions.ProjectAction;
}

export default class JobCreate extends React.Component<Props, {}> {

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
      baseUrl = projectUrl + '/jobs/new';
    } else {
      cancelUrl = getUserUrl(this.props.user);
      baseUrl = '/app/jobs/new';
    }
    return (
      <div className="row form-full-page">
        <div className="col-md-3">
          <h3 className="form-title">New Job</h3>
          <p>
            You can create Jobs to download/move/process/prepare a dataset or any generic operations.
          </p>
          <p>
            In future Polyaxon versions, several re-usable operations/actions/events/integrations
            will be provided to interact or watch external environments.
          </p>
          <p>
            <strong>Tip:</strong> You can use Polyaxon CLI to create & stop Jobs as well.
          </p>
        </div>
        <div className="col-md-offset-1 col-md-8">
          <LinkedTab
            baseUrl={baseUrl}
            tabs={[
              {
                title: 'Quick Mode',
                component: <JobCreateQuick
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
                component: <JobCreateFull
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
                component: <JobCreateTemplate
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
