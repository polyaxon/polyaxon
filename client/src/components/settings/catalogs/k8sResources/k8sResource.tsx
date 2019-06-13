import * as React from 'react';

import * as actions from '../../../../actions/k8sResources';
import { K8SResourceModel } from '../../../../models/k8sResource';
import Description from '../../../description';
import DatesMetaInfo from '../../../metaInfo/datesMetaInfo';
import IdMetaInfo from '../../../metaInfo/idMetaInfo';
import MetaInfo from '../../../metaInfo/metaInfo';
import Tags from '../../../tags/tags';
import '../../settings.less';
import K8SResourceActions from './k8sResourceActions';

export interface Props {
  onDelete: () => actions.K8SResourceAction;
  onEdit: () => void;
  resource: string;
  k8sResource: K8SResourceModel;
}

export default class K8SResource extends React.Component<Props, {}> {
  public render() {
    const k8sResource = this.props.k8sResource;
    return (
      <tr className="list-item">
        <td className="block">
          {k8sResource.name}
          <Description description={k8sResource.description}/>
          <div className="meta">
            <IdMetaInfo value={k8sResource.id} inline={true}/>
            {/*<UserMetaInfo user={k8sResource.user} inline={true}/>*/}
            <DatesMetaInfo
              createdAt={k8sResource.created_at}
              updatedAt={k8sResource.updated_at}
              inline={true}
            />
          </div>
          <Tags tags={k8sResource.tags}/>
        </td>
        <td className="block">
          <div className="meta">
            <MetaInfo
              icon="fas fa-circle"
              name="K8S ref"
              value={k8sResource.k8s_ref}
              inline={true}
            />
          </div>
          <div className="meta">
            <MetaInfo
              icon="fas fa-circle"
              name="keys"
              value={JSON.stringify(k8sResource.keys)}
              inline={true}
            />
          </div>
        </td>
        <td className="block pull-right">
          <K8SResourceActions
            onDelete={this.props.onDelete}
            onEdit={this.props.onEdit}
            pullRight={false}
          />
        </td>
      </tr>
    );
  }
}
