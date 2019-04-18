import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import * as experimentsActions from '../../../actions/experiments';
import { ExperimentModel } from '../../../models/experiment';
import { ProjectModel } from '../../../models/project';
import {
  CreateEntity,
  DescriptionField,
  DescriptionSchema,
  ErrorsField,
  FormButtons,
  getConfigFromRun,
  NameField,
  NameSchema,
  ProjectField,
  ReadmeField,
  ReadmeSchema,
  RunField,
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
  onCreate: (experiment: ExperimentModel, user?: string, projectName?: string) => experimentsActions.ExperimentAction;
}

const ValidationSchema = Yup.object().shape({
  name: NameSchema,
  description: DescriptionSchema,
  readme: ReadmeSchema,
});

export default class ExperimentCreateQuick extends React.Component<Props, {}> {

  public createExperiment = (state: State) => {
    const form = sanitizeForm({
      tags: state.tags.map((v) => v.value),
      readme: state.readme,
      description: state.description,
      name: state.name,
      config: state.run.command ? getConfigFromRun(state.run, 'experiment') : null,
      is_managed: true
    }) as ExperimentModel;

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
              this.createExperiment(fValues);
            }}
            render={(props: FormikProps<State>) => (
              <form onSubmit={props.handleSubmit}>
                {ErrorsField(this.props.errors)}
                {this.props.isProjectEntity && ProjectField(this.props.projects)}
                {RunField(props, this.props.errors, true)}
                {NameField(props, this.props.errors)}
                {DescriptionField(props, this.props.errors)}
                {ReadmeField}
                {TagsField(props, this.props.errors)}
                {FormButtons(this.props.cancelUrl, this.props.isLoading, 'Create experiment')}
              </form>
            )}
          />
        </div>
      </div>
    );
  }
}
