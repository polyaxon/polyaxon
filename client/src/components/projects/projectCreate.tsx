import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import * as actions from '../../actions/project';
import { ProjectModel } from '../../models/project';
import { BaseEmptyState, BaseState } from '../forms/baseCeationState';
import { DescriptionField, DescriptionSchema } from '../forms/descriptionField';
import { NameField, NameSchema } from '../forms/nameField';
import { ReadmeField, ReadmeSchema } from '../forms/readmeField';
import { TagsField } from '../forms/tagsField';
import { VisibilityField } from '../forms/visibilityField';

export interface Props {
  user: string;
  onCreate: (project: ProjectModel) => actions.ProjectAction;
}

export interface State extends BaseState {
  is_public: boolean;
}

const EmptyState = {...BaseEmptyState, is_public: true};

const ValidationSchema = Yup.object().shape({
  name: NameSchema.required('Required'),
  description: DescriptionSchema,
  readme: ReadmeSchema,
});

export default class ProjectCreate extends React.Component<Props, {}> {

  public createProject = (state: State) => {
    this.props.onCreate({
      tags: state.tags.map((v) => v.value),
      readme: state.readme,
      description: state.description,
      name: state.name,
      is_public: state.is_public
    } as ProjectModel);
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
                  {NameField(props)}
                  {DescriptionField(props)}
                  {VisibilityField}
                  {ReadmeField}
                  {TagsField}
                  <div className="form-group form-actions">
                    <div className="col-sm-offset-2 col-sm-10">
                      <button
                        type="submit"
                        className="btn btn-default btn-success"
                        disabled={props.isSubmitting}
                      >
                        Create project
                      </button>
                      <button className="btn btn-default pull-right">cancel</button>
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
