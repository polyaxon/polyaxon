import * as React from 'react';

import * as groupsActions from '../../../actions/groups';
import { GroupModel } from '../../../models/group';
import { ProjectModel } from '../../../models/project';

export interface Props {
  cancelUrl: string;
  isLoading: boolean;
  isProjectEntity: boolean;
  projects: ProjectModel[];
  errors: any;
  onCreate: (group: GroupModel, user?: string, projectName?: string) => groupsActions.GroupAction;
}

export default class GroupCreateTemplate extends React.Component<Props, {}> {

  public render() {
    return (
      <div className="row form-content">
        <div className="col-md-11">
          <div className="row initialize-instructions">
            <div className="col-md-12">
              <div className="jumbotron jumbotron-action text-center empty-jumbotron">
                <h3>No template was found or you don't have access to this feature yet.</h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
