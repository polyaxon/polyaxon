import * as jsYaml from 'js-yaml';
import * as React from 'react';

import * as actions from '../../actions/experiment';
import { ExperimentModel } from '../../models/experiment';
import { BaseEmptyState, BaseState, CreateMixin } from '../createMixin';

export interface Props {
  user: string;
  projectName: string;
  onCreate: (project: ExperimentModel) => actions.ExperimentAction;
}

export interface State extends BaseState {
  polyaxonfile: string;
}

const EmptyState = {...BaseEmptyState, polyaxonfile: ''};

export default class ExperimentCreate extends CreateMixin<Props, State> {
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

  public getConfig = (polyaxonfile: string): { [key: string]: any } => {
    return jsYaml.safeLoad(polyaxonfile);
  };

  public createProject = (event: any) => {
    event.preventDefault();
    this.props.onCreate({
      tags: this.state.tags.map((v) => v.value),
      readme: this.state.readme,
      description: this.state.description,
      name: this.state.name,
      config: this.getConfig(this.state.polyaxonfile)
    } as ExperimentModel);
  };

  public render() {
    return (
      <>
        <div className="row form-header">
          <div className="col-md-12">
            <h3 className="form-title">Create Experiment</h3>
          </div>
        </div>
        <div className="row form-content">
          <div className="col-sm-offset-1 col-md-10">
            <form className="form-horizontal" onSubmit={this.createProject}>
              {this.renderConfig()}
              {this.renderName()}
              {this.renderDescription()}
              {this.renderReadme()}
              {this.renderTags()}
              <div className="form-group form-actions">
                <div className="col-sm-offset-2 col-sm-10">
                  <button
                    type="submit"
                    className="btn btn-default btn-success"
                    onClick={this.createProject}
                  >
                    Create experiment
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
