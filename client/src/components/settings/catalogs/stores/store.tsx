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
    const store = this.props.store;
    return (
      <tr className="list-item">
        <td className="block">
          {store.name}
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
              name="K8S ref"
              value={store.mount_path}
              inline={true}
            />
          </div>
          <div className="meta">
            <MetaInfo
              icon="fas fa-circle"
              name="keys"
              value={JSON.stringify(store.bucket)}
              inline={true}
            />
          </div>
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
