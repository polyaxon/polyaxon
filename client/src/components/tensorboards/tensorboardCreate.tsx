import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import * as Yup from 'yup';

import * as experimentsActions from '../../actions/experiments';
import * as groupsActions from '../../actions/groups';
import * as projectsActions from '../../actions/projects';
import { getExperimentUrl, getGroupUrl, getProjectUrl, getUserUrl, splitUniqueName } from '../../constants/utils';
import { ProjectModel } from '../../models/project';
import { TensorboardModel } from '../../models/tensorboard';
import { BaseEmptyState, BaseState } from '../forms/baseCeationState';
import { ConfigField, ConfigSchema, getConfig } from '../forms/configField';
import { DescriptionField, DescriptionSchema } from '../forms/descriptionField';
import { ErrorsField } from '../forms/errorsField';
import { NameField, NameSchema } from '../forms/nameField';
import { ProjectField } from '../forms/projectField';
import { TagsField } from '../forms/tagsField';
import { sanitizeForm } from '../forms/utils';

export interface Props {
  user: string;
  projectName: string;
  groupId: string;
  experimentId: string;
  isLoading: boolean;
  isProjectEntity: boolean;
  projects: ProjectModel[];
  errors: any;
  onCreate: (tensorboard: TensorboardModel, user?: string, projectName?: string) =>
    experimentsActions.ExperimentAction
    | groupsActions.GroupAction
    | projectsActions.ProjectAction;
  fetchProjects: (user: string) => projectsActions.ProjectAction;
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

export default class TensorboardCreate extends React.Component<Props, {}> {

  public componentDidMount() {
    if (this.props.isProjectEntity) {
      this.props.fetchProjects(this.props.user);
    }
  }

  public createTensorboard = (state: State) => {
    const form = sanitizeForm({
      tags: state.tags.map((v) => v.value),
      description: state.description,
      name: state.name,
      config: getConfig(state.config)
    }) as TensorboardModel;

    if (this.props.isProjectEntity) {
      const values = splitUniqueName(state.project);
      this.props.onCreate(form, values[0], values[1]);
    } else {
      this.props.onCreate(form);
    }
  };

  public render() {
    let cancelUrl = '';
    if (this.props.projectName) {
      cancelUrl = getProjectUrl(this.props.user, this.props.projectName);
      if (this.props.experimentId) {
        cancelUrl = getExperimentUrl(this.props.user, this.props.projectName, this.props.experimentId);
      } else if (this.props.groupId) {
        cancelUrl = getGroupUrl(this.props.user, this.props.projectName, this.props.groupId);
      }
    } else {
      cancelUrl = getUserUrl(this.props.user);
    }

    return (
      <>
        <div className="row form-header">
          <div className="col-md-12">
            <h3 className="form-title">Create Tensorboard</h3>
          </div>
        </div>
        <div className="row form-content">
          <div className="col-sm-offset-1 col-md-10">
            <Formik
              initialValues={EmptyState}
              validationSchema={ValidationSchema}
              onSubmit={(fValues: State, fActions: FormikActions<State>) => {
                this.createTensorboard(fValues);
              }}
              render={(props: FormikProps<State>) => (
                <form className="form-horizontal" onSubmit={props.handleSubmit}>
                  {ErrorsField(this.props.errors)}
                  {this.props.isProjectEntity && ProjectField(this.props.projects)}
                  {ConfigField(props, this.props.errors)}
                  {NameField(props, this.props.errors)}
                  {DescriptionField(props, this.props.errors)}
                  {TagsField(props, this.props.errors)}
                  <div className="form-group form-actions">
                    <div className="col-sm-offset-2 col-sm-10">
                      <button
                        type="submit"
                        className="btn btn-success"
                        disabled={this.props.isLoading}
                      >
                        Create tensorboard
                      </button>
                      <LinkContainer to={`${cancelUrl}#`}>
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
