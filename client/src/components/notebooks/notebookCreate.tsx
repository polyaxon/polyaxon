import { Formik, FormikActions, FormikProps } from 'formik';
import * as jsYaml from 'js-yaml';
import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import * as Yup from 'yup';

import * as actions from '../../actions/projects';
import { getProjectUrl } from '../../constants/utils';
import { NotebookModel } from '../../models/notebook';
import { BaseEmptyState, BaseState } from '../forms/baseCeationState';
import { ConfigField, ConfigSchema } from '../forms/configField';
import { DescriptionField, DescriptionSchema } from '../forms/descriptionField';
import { ErrorsField } from '../forms/errorsField';
import { NameField, NameSchema } from '../forms/nameField';
import { TagsField } from '../forms/tagsField';

export interface Props {
  user: string;
  projectName: string;
  onCreate: (notebook: NotebookModel) => actions.ProjectAction;
  isLoading: boolean;
  errors: any;
}

export interface State extends BaseState {
  config: string;
}

const EmptyState = {...BaseEmptyState, config: ''};

const ValidationSchema = Yup.object().shape({
  config: ConfigSchema.required('Required'),
  name: NameSchema,
  description: DescriptionSchema,
});

export default class NotebookCreate extends React.Component<Props, {}> {

  public getConfig = (config: string): { [key: string]: any } => {
    return jsYaml.safeLoad(config);
  };

  public createNotebook = (state: State) => {
    this.props.onCreate({
      tags: state.tags.map((v) => v.value),
      description: state.description,
      name: state.name,
      config: this.getConfig(state.config)
    } as NotebookModel);
  };

  public render() {
    return (
      <>
        <div className="row form-header">
          <div className="col-md-12">
            <h3 className="form-title">Create Notebook</h3>
          </div>
        </div>
        <div className="row form-content">
          <div className="col-sm-offset-1 col-md-10">
            <Formik
              initialValues={EmptyState}
              validationSchema={ValidationSchema}
              onSubmit={(fValues: State, fActions: FormikActions<State>) => {
                this.createNotebook(fValues);
              }}
              render={(props: FormikProps<State>) => (
                <form className="form-horizontal" onSubmit={props.handleSubmit}>
                  {ErrorsField(this.props.errors)}
                  {ConfigField(props, this.props.errors)}
                  {NameField(props, this.props.errors)}
                  {DescriptionField(props, this.props.errors)}
                  {TagsField(props, this.props.errors)}
                  <div className="form-group form-actions">
                    <div className="col-sm-offset-2 col-sm-10">
                      <button
                        type="submit"
                        className="btn btn-default btn-success"
                        disabled={this.props.isLoading}
                      >
                        Create notebook
                      </button>
                      <LinkContainer to={`${getProjectUrl(this.props.user, this.props.projectName)}#`}>
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
