import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import * as k8sResourcesActions from '../../../../actions/k8sResources';
import * as actions from '../../../../actions/stores';
import { K8SResourceModel } from '../../../../models/k8sResource';
import { StoreModel } from '../../../../models/store';
import {
  DescriptionField,
  DescriptionSchema,
  ErrorsField,
  ModalFormButtons,
  NameField,
  NameSchema,
  sanitizeForm,
  StoreField,
  TagsField,
} from '../../../forms';

export interface StoreState {
  type: string;
  mount_path: string;
  host_path: string;
  volume_claim: string;
  bucket: string;
  k8s_secret: string | number;
  read_only: boolean;
}

export const getStoreEmptyState = () => ({
  type: 's3',
  mount_path: '',
  host_path: '',
  volume_claim: '',
  bucket: '',
  k8s_secret: '',
  read_only: false,
});

export interface State {
  tags: Array<{ label: string, value: string }>;
  readme: string;
  description: string;
  name: string;
  store: StoreState;
}

export const getEmptyState = () => ({
  tags: [] as Array<{ label: string, value: string }>,
  readme: '',
  description: '',
  name: '',
  store: getStoreEmptyState(),
});

export interface Props {
  resource: string;
  cstore?: StoreModel;
  onCancel: () => void;
  isLoading: boolean;
  success: boolean;
  errors: any;
  onUpdate: (name: string, store: StoreModel) => actions.StoreAction;
  onCreate: (store: StoreModel) => actions.StoreAction;
  initState: (name: string) => actions.StoreAction;
  fetchSecrets: () => k8sResourcesActions.K8SResourceAction;
  secrets: K8SResourceModel[];
}

const ValidationSchema = Yup.object().shape({
  name: NameSchema.required('Required'),
  description: DescriptionSchema,
});

export default class StoreFrom extends React.Component<Props, {}> {

  public componentDidMount() {
    this.props.fetchSecrets();
    this.props.cstore ?
      this.props.initState(this.props.cstore.name) :
      this.props.initState('');
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (this.props.success) {
      this.props.onCancel();
    }
  }

  public onSave = (store: StoreModel) => {
    this.props.cstore ?
      this.props.onUpdate(this.props.cstore.name, store) :
      this.props.onCreate(store);
  };

  public saveEntity = (state: State) => {
    let form = {
      name: state.name,
      description: state.description,
      tags: state.tags.map((v) => v.value),
      type: state.store.type,
      mount_path: state.store.mount_path,
      host_path: state.store.host_path,
      volume_claim: state.store.volume_claim,
      bucket: state.store.bucket,
      k8s_secret: state.store.k8s_secret,
      read_only: state.store.read_only,
    } as StoreModel;

    if (this.props.cstore) {
      if (this.props.cstore.name === form.name) {
        delete form.name;  // To prevent the owner-name validation on backend
      }
    } else {
      form = sanitizeForm(form) as StoreModel;
    }

    this.onSave(form);
  };

  public render() {
    const emptyState = getEmptyState();
    if (this.props.cstore) {
      emptyState.name = this.props.cstore.name;
      emptyState.description = this.props.cstore.description || '';
      emptyState.readme = this.props.cstore.readme || '';
      emptyState.store.type = this.props.cstore.type || 's3';
      emptyState.store.mount_path = this.props.cstore.mount_path || '';
      emptyState.store.host_path = this.props.cstore.host_path || '';
      emptyState.store.volume_claim = this.props.cstore.volume_claim || '';
      emptyState.store.bucket = this.props.cstore.bucket || '';
      emptyState.store.k8s_secret = this.props.cstore.k8s_secret || '';
      emptyState.store.read_only = this.props.cstore.read_only || false;
      emptyState.tags = this.props.cstore.tags ?
        this.props.cstore.tags.map((key: string) => ({label: key, value: key})) :
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
                {StoreField(props, this.props.errors, this.props.secrets)}
                {DescriptionField(props, this.props.errors)}
                {TagsField(props, this.props.errors)}
                {ModalFormButtons(
                  this.props.onCancel,
                  this.props.isLoading,
                  this.props.cstore ? 'Update' : 'Create')}
              </form>
            )}
          />
        </div>
      </div>
    );
  }
}
