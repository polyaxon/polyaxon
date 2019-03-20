import * as React from 'react';

import * as actions from '../../actions/project';
import { ProjectModel } from '../../models/project';
import { BaseEmptyState, BaseState, CreateMixin } from '../createMixin';

export interface Props {
  user: string;
  onCreate: (project: ProjectModel) => actions.ProjectAction;
}

export interface State extends BaseState {
  is_public: boolean;
}

const EmptyState = {...BaseEmptyState, is_public: true};

export default class ProjectCreate extends CreateMixin<Props, State> {

  constructor(props: Props) {
    super(props);
    this.state = EmptyState;
  }

  public update = (dict: { [key: string]: any }) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      ...dict
    }));
  };

  public createProject = (event: any) => {
    event.preventDefault();
    this.props.onCreate({
      tags: this.state.tags.map((v) => v.value),
      readme: this.state.readme,
      description: this.state.description,
      name: this.state.name,
      is_public: this.state.is_public
    } as ProjectModel);
  };

  public handlePrivacyChange = (privacy: string) => {
    this.update({is_public: privacy === 'public'});
  };

  public renderVisibility = () => (
    <div className="form-group">
      <label className="col-sm-2 control-label">Visibility</label>
      <div className="col-sm-2">
        <select
          onChange={(event) => this.handlePrivacyChange(event.target.value)}
          className="form-control input-sm"
        >
          <option>Public</option>
          <option>Private</option>
        </select>
      </div>
    </div>
  );

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
              {this.renderName()}
              {this.renderDescription()}
              {this.renderVisibility()}
              {this.renderReadme()}
              {this.renderTags()}
              <div className="form-group form-actions">
                <div className="col-sm-offset-2 col-sm-10">
                  <button
                    type="submit"
                    className="btn btn-default btn-success"
                    onClick={this.createProject}
                  >
                    Create project
                  </button>
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
