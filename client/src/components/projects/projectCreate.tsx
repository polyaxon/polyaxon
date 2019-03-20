import * as React from 'react';

import * as actions from '../../actions/project';
import { ProjectModel } from '../../models/project';
import Tags from '../tags';

export interface Props {
  user: string;
  createProject: (project: ProjectModel) => actions.ProjectAction;
}

export default class ProjectCreate extends React.Component<Props, {}> {

  public createProject = (event: any) => {
    event.preventDefault();
  };

  public render() {
    return (
      <>
        <div className="row form-header">
          <div className="col-md-12">
            <h3 className="form-title">Create Project</h3>
          </div>
        </div>
        <div className="row form-content">
          <div className="col-sm-offset-1 col-md-10">
            <form className="form-horizontal" onSubmit={this.createProject}>
              <div className="form-group">
                <label className="col-sm-2 control-label">Name</label>
                <div className="col-sm-5">
                  <input
                    type="text"
                    className="form-control input-sm"
                    // onChange={(event) => this.setSelectionGroup(event.target.value)}
                  />
                </div>
              </div>
              <div className="form-group">
                <label className="col-sm-2 control-label">Description</label>
                <div className="col-sm-10">
                  <input
                    type="text"
                    className="form-control input-sm"
                    // onChange={(event) => this.setSelectionGroup(event.target.value)}
                  />
                </div>
              </div>
              <div className="form-group">
                <label className="col-sm-2 control-label">Visibility</label>
                <div className="col-sm-2">
                  <select className="form-control input-sm">
                    <option>Public</option>
                    <option>Private</option>
                  </select>
                </div>
              </div>
              <div className="form-group">
                <label className="col-sm-2 control-label">Tags</label>
                <div className="col-sm-10">
                  <Tags
                    tags={[]}
                    isEditMode={true}
                    onSave={(tags: string[]) => {
                      return;
                    }}
                  />
                </div>
              </div>

              <div className="form-group form-actions">
                <div className="col-sm-offset-2 col-sm-10">
                  <button type="submit" className="btn btn-default btn-success" onClick={this.createProject}>Save</button>
                  <button type="submit" className="btn btn-default pull-right">cancel</button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </>
    );
  }
}
