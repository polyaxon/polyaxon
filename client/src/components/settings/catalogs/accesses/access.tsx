import * as React from 'react';

import * as actions from '../../../../actions/access';
import * as optionActions from '../../../../actions/options';
import { AccessModel } from '../../../../models/access';
import Description from '../../../description';
import DatesMetaInfo from '../../../metaInfo/datesMetaInfo';
import IdMetaInfo from '../../../metaInfo/idMetaInfo';
import MetaInfo from '../../../metaInfo/metaInfo';
import Tags from '../../../tags/tags';
import '../../settings.less';
import AccessActions from './accessActions';

export interface Props {
  onDelete: () => actions.AccessAction;
  onMakeDefault: () => optionActions.OptionAction;
  onEdit: () => void;
  resource: string;
  access: AccessModel;
}

export default class Access extends React.Component<Props, {}> {
  public render() {
    const access = this.props.access;
    return (
      <tr className="list-item">
        <td className="block">
          <span className="title">{access.name}</span>
          <Description description={access.description}/>
          <div className="meta">
            <IdMetaInfo value={access.id} inline={true}/>
            {/*<UserMetaInfo user={access.user} inline={true}/>*/}
            <DatesMetaInfo
              createdAt={access.created_at}
              updatedAt={access.updated_at}
              inline={true}
            />
          </div>
          <Tags tags={access.tags}/>
        </td>
        <td className="block">
          <div className="meta">
            <MetaInfo
              icon="fas fa-circle"
              name="Host"
              value={access.host}
              inline={true}
            />
          </div>
          {access.is_default &&
          <div className="meta">
            <MetaInfo
              icon="fas fa-check"
              name="Is Default"
              value="yes"
              inline={true}
            />
          </div>
          }
        </td>
        <td className="block pull-right">
          <AccessActions
            onDelete={this.props.onDelete}
            onMakeDefault={this.props.onMakeDefault}
            onEdit={this.props.onEdit}
            pullRight={false}
          />
        </td>
      </tr>
    );
  }
}
