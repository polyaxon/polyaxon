import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import * as actions from '../../../../actions/k8sResources';
import { K8SResourceModel } from '../../../../models/k8sResource';
import {
  DescriptionField,
  DescriptionSchema,
  ErrorsField,
  K8SRefField,
  K8SRefKeysField,
  K8SRefSchema,
  ModalFormButtons,
  NameField,
  NameSchema,
  sanitizeForm,
  TagsField,
} from '../../../forms';

export interface State {
  tags: Array<{ label: string, value: string }>;
  readme: string;
  description: string;
  name: string;
  k8s_ref: string;
  keys: string[];
}

export const EmptyState = {
  tags: [] as Array<{ label: string, value: string }>,
  readme: '',
  description: '',
  name: '',
  k8s_ref: '',
  keys: [] as string[]
};

export interface Props {
  resource: string;
  k8sResource?: K8SResourceModel;
  onCancel: () => void;
  isLoading: boolean;
  success: boolean;
  errors: any;
  onUpdate: (name: string, k8sResource: K8SResourceModel) => actions.K8SResourceAction;
  onCreate: (k8sResource: K8SResourceModel) => actions.K8SResourceAction;
  initState: (name: string) => actions.K8SResourceAction;
}

const ValidationSchema = Yup.object().shape({
  k8s_ref: K8SRefSchema.required('Required'),
  name: NameSchema.required('Required'),
  description: DescriptionSchema,
});

export default class K8sResourceFrom extends React.Component<Props, {}> {

  public componentDidMount() {
    this.props.k8sResource ?
    this.props.initState(this.props.k8sResource.name) :
    this.props.initState('') ;
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (this.props.success) {
      this.props.onCancel();
    }
  }

  public onSave = (k8sResource: K8SResourceModel) => {
    this.props.k8sResource ?
      this.props.onUpdate(this.props.k8sResource.name, k8sResource) :
      this.props.onCreate(k8sResource);
  };

  public saveEntity = (state: State) => {
    const form = sanitizeForm({
      name: state.name,
      description: state.description,
      k8s_ref: state.k8s_ref,
      keys: state.keys,
      tags: state.tags.map((v) => v.value),
    }) as K8SResourceModel;

    this.onSave(form);
  };

  public render() {
    const emptyState = EmptyState;
    if (this.props.k8sResource) {
      emptyState.name = this.props.k8sResource.name;
      emptyState.description = this.props.k8sResource.description || '';
      emptyState.readme = this.props.k8sResource.readme || '';
      emptyState.k8s_ref = this.props.k8sResource.k8s_ref;
      emptyState.keys = this.props.k8sResource.keys || [];
      emptyState.tags = this.props.k8sResource.tags ?
        this.props.k8sResource.tags.map((key: string) => ({label: key, value: key})) :
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
                {K8SRefField(props, this.props.errors)}
                {K8SRefKeysField(props, this.props.errors)}
                {DescriptionField(props, this.props.errors)}
                {TagsField(props, this.props.errors)}
                {ModalFormButtons(
                  this.props.onCancel,
                  this.props.isLoading,
                  this.props.k8sResource ? 'Update' : 'Create')}
              </form>
            )}
          />
        </div>
      </div>
    );
  }
}
