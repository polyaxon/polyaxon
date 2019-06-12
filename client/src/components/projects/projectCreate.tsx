import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import * as actions from '../../actions/projects';
import { ProjectModel } from '../../models/project';
import { getUserUrl } from '../../urls/utils';
import {
  BaseEmptyState,
  BaseState,
  DescriptionField,
  DescriptionSchema,
  ErrorsField, FormButtons,
  NameField,
  NameSchema,
  ReadmeField,
  ReadmeSchema,
  sanitizeForm,
  TagsField,
  VisibilityField
} from '../forms';

export interface Props {
  user: string;
  onCreate: (project: ProjectModel) => actions.ProjectAction;
  isLoading: boolean;
  errors: any;
}

export interface State extends BaseState {
  is_public: boolean;
  visibility: string;
}

const EmptyState = {...BaseEmptyState, is_public: true, visibility: 'Public'};

const ValidationSchema = Yup.object().shape({
  name: NameSchema.required('Required'),
  description: DescriptionSchema,
  readme: ReadmeSchema,
});

export default class ProjectCreate extends React.Component<Props, {}> {

  public createProject = (state: State) => {
    this.props.onCreate(sanitizeForm({
      tags: state.tags.map((v) => v.value),
      readme: state.readme,
      description: state.description,
      name: state.name,
      is_public: state.visibility === 'Public'
    }) as ProjectModel);
  };

  public render() {
    return (
      <>
        <div className="row form-header">
          <div className="col-md-12">
            <h3 className="form-title">New Project</h3>
          </div>
        </div>
        <div className="row form-content">
          <div className="col-md-offset-1 col-md-10">
            <Formik
              initialValues={EmptyState}
              validationSchema={ValidationSchema}
              onSubmit={(fValues: State, fActions: FormikActions<State>) => {
                this.createProject(fValues);
              }}
              render={(props: FormikProps<State>) => (
                <form onSubmit={props.handleSubmit}>
                  {ErrorsField(this.props.errors)}
                  {NameField(props, this.props.errors, true)}
                  {DescriptionField(props, this.props.errors)}
                  {VisibilityField}
                  {ReadmeField}
                  {TagsField(props, this.props.errors)}
                  {FormButtons(getUserUrl(this.props.user), this.props.isLoading, 'Create project')}
                </form>
              )}
            />
          </div>
        </div>
      </>
    );
  }
}
