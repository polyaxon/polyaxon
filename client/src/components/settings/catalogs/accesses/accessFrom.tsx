import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import * as actions from '../../../../actions/access';
import * as k8sResourcesActions from '../../../../actions/k8sResources';
import { AccessModel } from '../../../../models/access';
import { K8SResourceModel } from '../../../../models/k8sResource';
import {
  AccessField,
  DescriptionField,
  DescriptionSchema,
  ErrorsField,
  ModalFormButtons,
  NameField,
  NameSchema,
  sanitizeForm,
  TagsField,
} from '../../../forms';

export interface AccessState {
  host: string;
  k8s_secret: string | number;
  insecure: boolean;
}

export const getAccessEmptyState = () => ({
  host: '',
  k8s_secret: '',
  insecure: true,
});

export interface State {
  tags: Array<{ label: string, value: string }>;
  readme: string;
  description: string;
  name: string;
  access: AccessState;
}

export const getEmptyState = () => ({
  tags: [] as Array<{ label: string, value: string }>,
  readme: '',
  description: '',
  name: '',
  access: getAccessEmptyState(),
});

export interface Props {
  resource: string;
  access?: AccessModel;
  onCancel: () => void;
  isLoading: boolean;
  success: boolean;
  errors: any;
  onUpdate: (name: string, access: AccessModel) => actions.AccessAction;
  onCreate: (access: AccessModel) => actions.AccessAction;
  initState: (name: string) => actions.AccessAction;
  fetchSecrets: () => k8sResourcesActions.K8SResourceAction;
  secrets: K8SResourceModel[];
}

const ValidationSchema = Yup.object().shape({
  name: NameSchema.required('Required'),
  description: DescriptionSchema,
});

export default class AccessFrom extends React.Component<Props, {}> {

  public componentDidMount() {
    this.props.fetchSecrets();
    this.props.access ?
      this.props.initState(this.props.access.name) :
      this.props.initState('');
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (this.props.success) {
      this.props.onCancel();
    }
  }

  public onSave = (access: AccessModel) => {
    this.props.access ?
      this.props.onUpdate(this.props.access.name, access) :
      this.props.onCreate(access);
  };

  public saveEntity = (state: State) => {
    let form = {
      name: state.name,
      description: state.description,
      tags: state.tags.map((v) => v.value),
      host: state.access.host,
      k8s_secret: state.access.k8s_secret,
    } as AccessModel;

    if (this.showInsecure()) {
      form.insecure = state.access.insecure;
    }

    if (this.props.access) {
      if (this.props.access.name === form.name) {
        delete form.name;  // To prevent the owner-name validation on backend
      }
    } else {
      form = sanitizeForm(form) as AccessModel;
    }

    this.onSave(form);
  };

  public showInsecure = () => {
    return this.props.resource === 'registry_access';
  };

  public render() {
    const emptyState = getEmptyState();
    if (this.props.access) {
      emptyState.name = this.props.access.name;
      emptyState.description = this.props.access.description || '';
      emptyState.readme = this.props.access.readme || '';
      emptyState.access.host = this.props.access.host || '';
      emptyState.access.k8s_secret = this.props.access.k8s_secret || '';
      emptyState.access.insecure = this.props.access.insecure;
      emptyState.tags = this.props.access.tags ?
        this.props.access.tags.map((key: string) => ({label: key, value: key})) :
        [];
    }
    return (
      <div className="row form-content">
        <div className="col-md-12">
          <Formik
            initialValues={emptyState}
            validationSchema={ValidationSchema}
            onSubmit={(fValues: State, fActions: FormikActions<State>) => {
              this.saveEntity(fValues);
            }}
            render={(props: FormikProps<State>) => (
              <form onSubmit={props.handleSubmit}>
                {ErrorsField(this.props.errors)}
                {NameField(props, this.props.errors, true)}
                {AccessField(props, this.props.errors, this.props.secrets, this.showInsecure())}
                {DescriptionField(props, this.props.errors)}
                {TagsField(props, this.props.errors)}
                {ModalFormButtons(
                  this.props.onCancel,
                  this.props.isLoading,
                  this.props.access ? 'Update' : 'Create')}
              </form>
            )}
          />
        </div>
      </div>
    );
  }
}
