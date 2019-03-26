import { Formik, FormikActions, FormikProps } from 'formik';
import * as jsYaml from 'js-yaml';
import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import * as Yup from 'yup';

import * as actions from '../../actions/jobs';
import { getProjectUrl } from '../../constants/utils';
import { JobModel } from '../../models/job';
import { BaseEmptyState, BaseState } from '../forms/baseCeationState';
import { ConfigField, ConfigSchema, getConfig } from '../forms/configField';
import { DescriptionField, DescriptionSchema } from '../forms/descriptionField';
import { ErrorsField } from '../forms/errorsField';
import { NameField, NameSchema } from '../forms/nameField';
import { ReadmeField, ReadmeSchema } from '../forms/readmeField';
import { TagsField } from '../forms/tagsField';

export interface Props {
  user: string;
  projectName: string;
  onCreate: (job: JobModel) => actions.JobAction;
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
  readme: ReadmeSchema,
});

export default class JobCreate extends React.Component<Props, {}> {

  public createJob = (state: State) => {
    this.props.onCreate({
      tags: state.tags.map((v) => v.value),
      readme: state.readme,
      description: state.description,
      name: state.name,
      config: getConfig(state.config)
    } as JobModel);
  };

  public render() {
    return (
      <>
        <div className="row form-header">
          <div className="col-md-12">
            <h3 className="form-title">Create Job</h3>
          </div>
        </div>
        <div className="row form-content">
          <div className="col-sm-offset-1 col-md-10">
            <Formik
              initialValues={EmptyState}
              validationSchema={ValidationSchema}
              onSubmit={(fValues: State, fActions: FormikActions<State>) => {
                this.createJob(fValues);
              }}
              render={(props: FormikProps<State>) => (
                <form className="form-horizontal" onSubmit={props.handleSubmit}>
                  {ErrorsField(this.props.errors)}
                  {ConfigField(props, this.props.errors)}
                  {NameField(props, this.props.errors)}
                  {DescriptionField(props, this.props.errors)}
                  {ReadmeField}
                  {TagsField(props, this.props.errors)}
                  <div className="form-group form-actions">
                    <div className="col-sm-offset-2 col-sm-10">
                      <button
                        type="submit"
                        className="btn btn-default btn-success"
                        disabled={this.props.isLoading}
                      >
                        Create job
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
