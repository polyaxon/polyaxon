import * as React from 'react';
import * as _ from 'lodash';

import { GroupModel } from '../models/group';
import {
  getProjectUrl,
  getUserUrl,
  splitUniqueName
} from '../constants/utils';
import Experiments from '../containers/experiments';
import Breadcrumb from './breadcrumb';
import LinkedTab from './linkedTab';
import GroupOverview from './groupOverview';
import { getGroupUrl } from '../constants/utils';
import { EmptyList } from './emptyList';
import GeneralInstructions from './generalInstructions';

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
      return EmptyList(false, 'experiment group', 'group');
    }
    let values = splitUniqueName(group.project);
    let groupUrl = getGroupUrl(values[0], values[1], this.props.group.id);
    let projectUrl = getProjectUrl(values[0], values[1]);
    return (
      <div className="row">
        <div className="col-md-12">
          <div className="entity-details">
            <Breadcrumb
              icon="fa-cubes"
              links={[
                {name: values[0], value: getUserUrl(values[0])},
                {name: values[1], value: projectUrl},
                {name: 'Groups', value: `${projectUrl}#groups`},
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
                  component: <Experiments user={group.user} projectName={group.project} groupId={group.id}/>,
                  relUrl: 'experiments'
                }, {
                  title: 'Instructions',
                  component: <GeneralInstructions entity="group" entityId={group.id}/>,
                  relUrl: 'instructions'
                }
              ]}
            />
          </div>
        </div>
      </div>
    );
  }
}
