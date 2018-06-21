import * as React from 'react';
import * as _ from 'lodash';

import { GroupModel } from '../models/group';
import {
  getProjectUrl,
  getUserUrl,
  splitProjectName
} from '../constants/utils';
import Experiments from '../containers/experiments';
import Breadcrumb from './breadcrumb';
import LinkedTab from './linkedTab';
import GroupOverview from './groupOverview';
import { getGroupUrl } from '../constants/utils';

export interface Props {
  group: GroupModel;
  onDelete: () => undefined;
  fetchData: () => undefined;
}

export default class GroupDetail extends React.Component<Props, Object> {
  componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const group = this.props.group;
    if (_.isNil(group)) {
      return (<div>Nothing</div>);
    }
    let values = splitProjectName(group.project_name);
    let groupUrl = getGroupUrl(values[0], values[1], this.props.group.id);
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb
              icon="fa-cubes"
              links={[
                {name: values[0], value: getUserUrl(values[0])},
                {name: values[1], value: getProjectUrl(values[0], values[1])},
                {name: `Group ${group.id}`}]}
            />
            <LinkedTab
              baseUrl={groupUrl}
              tabs={[
                {
                  title: 'Overview',
                  component: <GroupOverview group={group}/>,
                  relUrl: ''
                }, {
                  title: 'Experiments',
                  component: <Experiments user={group.user} projectName={group.project_name} groupId={group.id}/>,
                  relUrl: 'experiments'
                }
              ]}
            />
          </div>
        </div>
      </div>
    );
  }
}

