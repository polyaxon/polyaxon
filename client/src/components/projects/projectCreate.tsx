import * as React from 'react';

import * as actions from '../../actions/project';
import { NameSlug } from '../../constants/helpTexts';
import { ProjectModel } from '../../models/project';
import MDEdit from '../mdEditor/mdEdit';
import TagsEdit from '../tags/tagsEdit';

export interface Props {
  user: string;
  onCreate: (project: ProjectModel) => actions.ProjectAction;
}

export interface State {
  tags: Array<{ label: string, value: string }>;
  readme: string;
  description: string;
  name: string;
  is_public: boolean;
}

export default class ProjectCreate extends React.Component<Props, State> {

  constructor(props: Props) {
    super(props);
    this.state = {
      tags: [],
      readme: '',
      description: '',
      name: '',
      is_public: true
    };
  }

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

  public handleTagsChange = (value: Array<{ label: string, value: string }>) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      tags: value,
    }));
  };

   public handleReadmeChange = (value: string) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      readme: value,
    }));
  };

  public handleDescriptionChange = (description: string) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      description,
    }));
  };

  public handleNameChange = (name: string) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      name,
    }));
  };

  public handlePrivacyChange = (privacy: string) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      is_public: privacy === 'public',
    }));
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
                    onChange={(event) => this.handleNameChange(event.target.value)}
                  />
                  <span id="helpBlock" className="help-block">{NameSlug}</span>
                </div>
              </div>
              <div className="form-group">
                <label className="col-sm-2 control-label">Description</label>
                <div className="col-sm-10">
                  <input
                    type="text"
                    className="form-control input-sm"
                    onChange={(event) => this.handleDescriptionChange(event.target.value)}
                  />
                </div>
              </div>
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
              <div className="form-group">
                <label className="col-sm-2 control-label">Read me</label>
                <div className="col-sm-10">
                  <MDEdit
                    content=""
                    handleChange={this.handleReadmeChange}
                  />
                </div>
              </div>
              <div className="form-group">
                <label className="col-sm-2 control-label">Tags</label>
                <div className="col-sm-10">
                  <TagsEdit tags={[]} handleChange={this.handleTagsChange}/>
                </div>
              </div>

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
