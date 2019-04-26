import * as React from 'react';
import * as Yup from 'yup';

import * as experimentsActions from '../../../actions/experiments';
import * as groupsActions from '../../../actions/groups';
import * as projectsActions from '../../../actions/projects';
import { ProjectModel } from '../../../models/project';
import { TensorboardModel } from '../../../models/tensorboard';
import {
  BaseState,
  ConfigSchema,
  CreateEntity,
  DescriptionSchema,
  getConfig,
  NameSchema,
  sanitizeForm
} from '../../forms';

export interface Props {
  cancelUrl: string;
  isLoading: boolean;
  isProjectEntity: boolean;
  projects: ProjectModel[];
  errors: any;
  onCreate: (tensorboard: TensorboardModel, user?: string, projectName?: string) =>
    experimentsActions.ExperimentAction
    | groupsActions.GroupAction
    | projectsActions.ProjectAction;
}

export interface State extends BaseState {
  config: string;
}

const ValidationSchema = Yup.object().shape({
  config: ConfigSchema.required('Required'),
  name: NameSchema,
  description: DescriptionSchema,
});

export default class TensorboardCreateTemplate extends React.Component<Props, {}> {

  public createTensorboard = (state: State) => {
    const form = sanitizeForm({
      tags: state.tags.map((v) => v.value),
      description: state.description,
      name: state.name,
      config: getConfig(state.config)
    }) as TensorboardModel;

    CreateEntity(this.props.onCreate, form, state.project, this.props.isProjectEntity, this.props.projects);
  };

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
