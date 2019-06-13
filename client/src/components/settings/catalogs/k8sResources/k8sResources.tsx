import * as React from 'react';
import { Modal } from 'react-bootstrap';

import * as actions from '../../../../actions/k8sResources';
import K8sResourceFrom from '../../../../containers/settings/catalogs/k8sResourceForm';
import { K8SResourceModel } from '../../../../models/k8sResource';
import { isLive } from '../../../../utils/isLive';
import { EmptyList } from '../../../empty/emptyList';
import PaginatedTable from '../../../tables/paginatedTable';
import CatalogsSidebar from '../sidebar';
import K8SResource from './k8sResource';
import K8SResourceHeader from './k8sResourceHeader';

import '../../../actions.less';
import '../../settings.less';

export interface Props {
  resource: string;
  k8sResources: K8SResourceModel[];
  count: number;
  isLoading: boolean;
  errors: any;
  showDeleted: boolean;
  onFetch: () => actions.K8SResourceAction;
  onDelete: (name: string) => actions.K8SResourceAction;
}

export interface State {
  showModal: boolean;
  k8sResource?: K8SResourceModel;
}

export default class K8SResources extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      showModal: false,
      k8sResource: undefined,
    };
  }

  public componentDidMount() {
    this.props.onFetch();
  }

  public handleClose = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState, showModal: false
    }));
  };

  public handleShow = (k8sResource?: K8SResourceModel) => {
    this.setState((prevState, prevProps) => ({
      ...prevState, showModal: true, k8sResource: k8sResource || undefined
    }));
  };

  public render() {
    const listK8SResources = () => {
      return (
        <table className="table table-hover table-responsive">
          <tbody>
          {K8SResourceHeader()}
          {this.props.k8sResources
            .filter(
              (k8sResource: K8SResourceModel) =>
                (!this.props.showDeleted && isLive(k8sResource)) || (this.props.showDeleted && !isLive(k8sResource)))
            .map(
              (k8sResource: K8SResourceModel) =>
                <K8SResource
                  key={k8sResource.uuid}
                  resource={this.props.resource}
                  k8sResource={k8sResource}
                  onDelete={() => this.props.onDelete(k8sResource.name)}
                  onEdit={() => this.handleShow(k8sResource)}
                />)}
          </tbody>
        </table>
      );
    };

    const k8sResourceModal = (
      <Modal show={this.state.showModal} onHide={this.handleClose}>
        <Modal.Header closeButton={true}>
          <Modal.Title>{this.state.k8sResource ? 'Update Resource' : 'Create New Resource'}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <K8sResourceFrom
            resource={this.props.resource}
            k8sResource={this.state.k8sResource}
            onCancel={this.handleClose}
          />
        </Modal.Body>
      </Modal>
    );

    return (
      <div className="row settings">
        <div className="col-md-3">
          <CatalogsSidebar/>
        </div>
        <div className="col-md-9">
          <h3 className="menu-header">
            {this.props.resource}
            <span className="actions pull-right">
              <button
                type="button"
                className="btn btn-sm btn-success"
                onClick={() => this.handleShow()}
              >
                <i className="fas fa-plus fa-sm icon"/> New
              </button>
            </span>
          </h3>
          <PaginatedTable
            isLoading={this.props.isLoading}
            errors={this.props.errors}
            count={this.props.count}
            componentList={listK8SResources()}
            componentEmpty={EmptyList(false, this.props.resource, '')}
            filters={false}
            fetchData={this.props.onFetch}
          />
        </div>
        {k8sResourceModal}
      </div>
    );
  }
}
