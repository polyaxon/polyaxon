import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import * as Yup from 'yup';

import * as actions from '../../actions/projects';
import { getUserUrl } from '../../constants/utils';
import { ProjectModel } from '../../models/project';
import { BaseEmptyState, BaseState } from '../forms/baseCeationState';
import { DescriptionField, DescriptionSchema } from '../forms/descriptionField';
import { ErrorsField } from '../forms/errorsField';
import { NameField, NameSchema } from '../forms/nameField';
import { ReadmeField, ReadmeSchema } from '../forms/readmeField';
import { TagsField } from '../forms/tagsField';
import { sanitizeForm } from '../forms/utils';
import { VisibilityField } from '../forms/visibilityField';

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
            <h3 className="form-title">Create Project</h3>
          </div>
        </div>
        <div className="row form-content">
          <div className="col-sm-offset-1 col-md-10">
            <Formik
              initialValues={EmptyState}
              validationSchema={ValidationSchema}
              onSubmit={(fValues:  State, fActions: FormikActions<State>) => {
                this.createProject(fValues);
              }}
              render={(props: FormikProps<State>) => (
                <form className="form-horizontal" onSubmit={props.handleSubmit}>
                  {ErrorsField(this.props.errors)}
                  {NameField(props, this.props.errors)}
                  {DescriptionField(props, this.props.errors)}
                  {VisibilityField}
                  {ReadmeField}
                  {TagsField(props, this.props.errors)}
                  <div className="form-group form-actions">
                    <div className="col-sm-offset-2 col-sm-10">
                      <button
                        type="submit"
                        className="btn btn-success"
                        disabled={this.props.isLoading}
                      >
                        Create project
                      </button>
                      <LinkContainer to={getUserUrl(this.props.user)}>
                        <button className="btn btn-default pull-right">cancel</button>
                      </LinkContainer>
                    </div>
                  </div>
                </form>
              )}
            />
          </div>
        </div>
      </>
    );
  }
}
