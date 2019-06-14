import * as React from 'react';

import * as actions from '../../../../actions/stores';
import { StoreModel } from '../../../../models/store';
import Description from '../../../description';
import DatesMetaInfo from '../../../metaInfo/datesMetaInfo';
import IdMetaInfo from '../../../metaInfo/idMetaInfo';
import MetaInfo from '../../../metaInfo/metaInfo';
import Tags from '../../../tags/tags';
import '../../settings.less';
import StoreActions from './storeActions';

export interface Props {
  onDelete: () => actions.StoreAction;
  onEdit: () => void;
  resource: string;
  store: StoreModel;
}

export default class Store extends React.Component<Props, {}> {
  public render() {
    const bucketInfo = (storeDef: StoreModel) => (
      <>
        <div className="meta">
          <MetaInfo
            icon="fas fa-circle"
            name="Bucket"
            value={storeDef.bucket}
            inline={true}
          />
        </div>
        {storeDef.k8s_secret &&
        <div className="meta">
          <MetaInfo
            icon="fas fa-circle"
            name="Secret"
            value={storeDef.k8s_secret}
            inline={true}
          />
        </div>
        }
      </>
    );
    const hostPathInfo = (storeDef: StoreModel) => (
      <>
        <div className="meta">
          <MetaInfo
            icon="fas fa-circle"
            name="Host Path"
            value={storeDef.host_path}
            inline={true}
          />
        </div>
        <div className="meta">
          <MetaInfo
            icon="fas fa-circle"
            name="Mount Path"
            value={storeDef.mount_path}
            inline={true}
          />
        </div>
        <div className="meta">
          <MetaInfo
            icon="fas fa-circle"
            name="Read Only"
            value={JSON.stringify(storeDef.read_only)}
            inline={true}
          />
        </div>
      </>
    );
    const mountPathInfo = (storeDef: StoreModel) => (
      <>
        <div className="meta">
          <MetaInfo
            icon="fas fa-circle"
            name="Volume Claim"
            value={storeDef.volume_claim}
            inline={true}
          />
        </div>
        <div className="meta">
          <MetaInfo
            icon="fas fa-circle"
            name="Mount Path"
            value={storeDef.mount_path}
            inline={true}
          />
        </div>
        <div className="meta">
          <MetaInfo
            icon="fas fa-circle"
            name="Read Only"
            value={JSON.stringify(storeDef.read_only)}
            inline={true}
          />
        </div>
      </>
    );
    const store = this.props.store;
    return (
      <tr className="list-item">
        <td className="block">
          <span className="title">{store.name}</span>
          <Description description={store.description}/>
          <div className="meta">
            <IdMetaInfo value={store.id} inline={true}/>
            {/*<UserMetaInfo user={store.user} inline={true}/>*/}
            <DatesMetaInfo
              createdAt={store.created_at}
              updatedAt={store.updated_at}
              inline={true}
            />
          </div>
          <Tags tags={store.tags}/>
        </td>
        <td className="block">
          <div className="meta">
            <MetaInfo
              icon="fas fa-circle"
              name="Store type"
              value={store.type}
              inline={true}
            />
          </div>
          {['s3', 'azure', 'gcs'].indexOf(store.type) > -1 && bucketInfo(store)}
          {store.type === 'host_path' && hostPathInfo(store)}
          {store.type === 'mount_path' && mountPathInfo(store)}
        </td>
        <td className="block pull-right">
          <StoreActions
            onDelete={this.props.onDelete}
            onEdit={this.props.onEdit}
            pullRight={false}
          />
        </td>
      </tr>
    );
  }
}
