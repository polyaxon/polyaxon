import * as React from 'react';

import { ActivityLogModel } from '../models/activitylog';
import PaginatedList from './paginatedList';
import { EmptyList } from './empty/emptyList';
import ActivityLog from './activityLog';
import ActivityLogHeader from './activityLogHeader';

export interface Props {
  activityLogs: ActivityLogModel[];
  count: number;
  fetchData: (offset: number) => any;
}

interface State {
  offset: number;
}

export default class ActivityLogs extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {offset: 0};
  }

  componentDidMount() {
    this.props.fetchData(this.state.offset);
  }

  public render() {
    const listBuilds = () => {
      return (
        <ul>
          {this.props.activityLogs.map(
            (activityLog: ActivityLogModel) =>
              <li className="activity-log" key={activityLog.id}>
                <ActivityLog activityLog={activityLog}/>
              </li>)}
        </ul>
      );
    };
    return (
      <PaginatedList
        count={this.props.count}
        componentList={listBuilds()}
        componentHeader={ActivityLogHeader()}
        componentEmpty={
          EmptyList(
            false,
            'activity',
            'activity')
        }
        filters={false}
        fetchData={this.props.fetchData}
      />
    );
  }
}
