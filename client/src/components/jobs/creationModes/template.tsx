import * as React from 'react';

import * as jobsActions from '../../../actions/jobs';
import { JobModel } from '../../../models/job';
import { ProjectModel } from '../../../models/project';

export interface Props {
  cancelUrl: string;
  isLoading: boolean;
  isProjectEntity: boolean;
  projects: ProjectModel[];
  errors: any;
  onCreate: (job: JobModel, user?: string, projectName?: string) => jobsActions.JobAction;
}

export default class JobCreateTemplate extends React.Component<Props, {}> {

  public render() {
    return (
      <div className="row form-content">
        <div className="col-md-11">
          <div className="row initialize-instructions">
            <div className="col-md-12">
              <div className="jumbotron jumbotron-action text-center empty-jumbotron">
                <h3>No templates was found or you don't have access to this feature yet.</h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
