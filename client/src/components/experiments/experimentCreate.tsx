import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import * as Yup from 'yup';

import * as experimentsActions from '../../actions/experiments';
import * as projectsActions from '../../actions/projects';
import { getProjectUrl, getUserUrl, splitUniqueName } from '../../constants/utils';
import { ExperimentModel } from '../../models/experiment';
import { ProjectModel } from '../../models/project';
import {
  BaseEmptyState,
  BaseState,
  ConfigField,
  ConfigSchema,
  DescriptionField,
  DescriptionSchema,
  ErrorsField,
  getConfig,
  NameField,
  NameSchema,
  ProjectField,
  ReadmeField,
  ReadmeSchema,
  sanitizeForm,
  TagsField
} from '../forms';

export interface Props {
  user: string;
  projectName: string;
  isLoading: boolean;
  isProjectEntity: boolean;
  projects: ProjectModel[];
  errors: any;
  onCreate: (experiment: ExperimentModel, user?: string, projectName?: string) => experimentsActions.ExperimentAction;
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
  readme: ReadmeSchema,
});

export default class ExperimentCreate extends React.Component<Props, {}> {

  public componentDidMount() {
    if (this.props.isProjectEntity) {
      this.props.fetchProjects(this.props.user);
    }
  }

  public createExperiment = (state: State) => {
    const form = sanitizeForm({
      tags: state.tags.map((v) => v.value),
      readme: state.readme,
      description: state.description,
      name: state.name,
      config: getConfig(state.config)
    }) as ExperimentModel;

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
    } else {
      cancelUrl = getUserUrl(this.props.user);
    }
    return (
      <>
        <div className="row form-header">
          <div className="col-md-12">
            <h3 className="form-title">Create Experiment</h3>
          </div>
        </div>
        <div className="row form-content">
          <div className="col-md-offset-1 col-md-10">
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
                  {ConfigField(props, this.props.errors, true)}
                  {NameField(props, this.props.errors)}
                  {DescriptionField(props, this.props.errors)}
                  {ReadmeField}
                  {TagsField(props, this.props.errors)}
                  <div className="form-group form-actions">
                    <div className="col-md-offset-2 col-md-10">
                      <button
                        type="submit"
                        className="btn btn-success"
                        disabled={this.props.isLoading}
                      >
                        Create experiment
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
