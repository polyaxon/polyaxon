import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import * as experimentsActions from '../../../actions/experiments';
import * as groupsActions from '../../../actions/groups';
import * as projectsActions from '../../../actions/projects';
import { ProjectModel } from '../../../models/project';
import { TensorboardModel } from '../../../models/tensorboard';
import {
  CreateEntity,
  DescriptionField,
  DescriptionSchema,
  DockerImageField,
  DockerImageSchema,
  ErrorsField,
  FormButtons,
  getConfigFromImage,
  NameField,
  NameSchema,
  ProjectField,
  sanitizeForm,
  TagsField
} from '../../forms';
import { EmptyState, State } from './utils';

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

const ValidationSchema = Yup.object().shape({
  dockerImage: DockerImageSchema,
  name: NameSchema,
  description: DescriptionSchema,
});

export default class TensorboardCreateQuick extends React.Component<Props, {}> {

  public createTensorboard = (state: State) => {
    const form = sanitizeForm({
      tags: state.tags.map((v) => v.value),
      description: state.description,
      name: state.name,
      content: state.dockerImage ? getConfigFromImage(state.dockerImage, 'tensorboard') : null,
      is_managed: true
    }) as TensorboardModel;

    CreateEntity(this.props.onCreate, form, state.project, this.props.isProjectEntity, this.props.projects);
  };

  public render() {
    return (
      <div className="row form-content">
        <div className="col-md-11">
          <Formik
            initialValues={EmptyState}
            validationSchema={ValidationSchema}
            onSubmit={(fValues: State, fActions: FormikActions<State>) => {
              this.createTensorboard(fValues);
            }}
            render={(props: FormikProps<State>) => (
              <form onSubmit={props.handleSubmit}>
                {ErrorsField(this.props.errors)}
                {this.props.isProjectEntity && ProjectField(this.props.projects)}
                {DockerImageField(props, this.props.errors, 'TENSORBOARDS:DOCKER_IMAGE')}
                {NameField(props, this.props.errors)}
                {DescriptionField(props, this.props.errors)}
                {TagsField(props, this.props.errors)}
                {FormButtons(this.props.cancelUrl, this.props.isLoading, 'Create tensorboard')}
              </form>
            )}
          />
        </div>
      </div>
    );
  }
}
