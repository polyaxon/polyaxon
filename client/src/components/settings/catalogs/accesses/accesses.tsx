import * as React from 'react';
import { Modal } from 'react-bootstrap';

import * as actions from '../../../../actions/access';
import * as optionActions from '../../../../actions/options';
import AccessFrom from '../../../../containers/settings/catalogs/accessForm';
import { AccessModel } from '../../../../models/access';
import { isLive } from '../../../../utils/isLive';
import { EmptyList } from '../../../empty/emptyList';
import PaginatedTable from '../../../tables/paginatedTable';
import CatalogsSidebar from '../sidebar';
import Access from './access';
import AccessHeader from './accessHeader';

import '../../../actions.less';
import '../../settings.less';

export interface Props {
  resource: string;
  accesses: AccessModel[];
  count: number;
  isLoading: boolean;
  errors: any;
  showDeleted: boolean;
  onFetch: () => actions.AccessAction;
  onDelete: (name: string) => actions.AccessAction;
  onMakeDefault: (id: number | string) => optionActions.OptionAction;
}

export interface State {
  showModal: boolean;
  access?: AccessModel;
}

export default class Accesses extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      showModal: false,
      access: undefined,
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

  public handleShow = (access?: AccessModel) => {
    this.setState((prevState, prevProps) => ({
      ...prevState, showModal: true, access: access || undefined
    }));
  };

  public render() {
    const listAccesses = () => {
      return (
        <table className="table table-hover table-responsive">
          <tbody>
          {AccessHeader()}
          {this.props.accesses
            .filter(
              (access: AccessModel) =>
                (!this.props.showDeleted && isLive(access)) || (this.props.showDeleted && !isLive(access)))
            .map(
              (access: AccessModel) =>
                <Access
                  key={access.uuid}
                  resource={this.props.resource}
                  access={access}
                  onDelete={() => this.props.onDelete(access.name)}
                  onMakeDefault={() => this.props.onMakeDefault(access.id)}
                  onEdit={() => this.handleShow(access)}
                />)}
          </tbody>
        </table>
      );
    };

    const AccessModal = (
      <Modal show={this.state.showModal} onHide={this.handleClose}>
        <Modal.Header closeButton={true}>
          <Modal.Title>{this.state.access ? 'Update Access' : 'Create New Access'}</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <AccessFrom
            resource={this.props.resource}
            access={this.state.access}
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
            componentList={listAccesses()}
            componentEmpty={EmptyList(false, this.props.resource, '')}
            filters={false}
            fetchData={this.props.onFetch}
          />
        </div>
        {AccessModal}
      </div>
    );
  }
}
