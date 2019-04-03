import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import * as projectsActions from '../../../actions/projects';
import { NotebookModel } from '../../../models/notebook';
import { ProjectModel } from '../../../models/project';
import {
  ConfigField,
  ConfigSchema,
  CreateEntity,
  DescriptionField,
  DescriptionSchema,
  ErrorsField,
  FormButtons,
  getConfig,
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
  onCreate: (notebook: NotebookModel, user?: string, projectName?: string) => projectsActions.ProjectAction;
}

const ValidationSchema = Yup.object().shape({
  config: ConfigSchema.required('Required'),
  name: NameSchema,
  description: DescriptionSchema,
});

export default class NotebookCreateFull extends React.Component<Props, {}> {

  public createNotebook = (state: State) => {
    const form = sanitizeForm({
      tags: state.tags.map((v) => v.value),
      description: state.description,
      name: state.name,
      config: getConfig(state.config)
    }) as NotebookModel;

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
              this.createNotebook(fValues);
            }}
            render={(props: FormikProps<State>) => (
              <form onSubmit={props.handleSubmit}>
                {ErrorsField(this.props.errors)}
                {this.props.isProjectEntity && ProjectField(this.props.projects)}
                {ConfigField(props, this.props.errors, true)}
                {NameField(props, this.props.errors)}
                {DescriptionField(props, this.props.errors)}
                {TagsField(props, this.props.errors)}
                {FormButtons(this.props.cancelUrl, this.props.isLoading, 'Create notebook')}
              </form>
            )}
          />
        </div>
      </div>
    );
  }
}
