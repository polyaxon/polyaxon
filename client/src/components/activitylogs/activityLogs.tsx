import * as React from 'react';

import { ActivityLogModel } from '../../models/activitylog';
import { EmptyList } from '../empty/emptyList';
import PaginatedList from '../tables/paginatedList';
import ActivityLog from './activityLog';
import ActivityLogHeader from './activityLogHeader';

export interface Props {
  activityLogs: ActivityLogModel[];
  count: number;
  fetchData: (offset: number) => any;
  isLoading: boolean;
  errors: any;
}

interface State {
  offset: number;
}

export default class ActivityLogs extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {offset: 0};
  }

  public componentDidMount() {
    this.props.fetchData(this.state.offset);
  }

  public render() {
    const listActivities = () => {
      const subjects = ['project', 'experiment_group', 'experiment', 'job', 'build'];
      return (
        <ul>
          {this.props.activityLogs
            .filter((activityLog: ActivityLogModel) => subjects.indexOf(activityLog.event_subject) > -1)
            .map(
              (activityLog: ActivityLogModel) =>
                <li className="list-item" key={activityLog.id}>
                  <ActivityLog activityLog={activityLog}/>
                </li>)}
        </ul>
      );
    };
    return (
      <PaginatedList
        isLoading={this.props.isLoading}
        errors={this.props.errors}
        count={this.props.count}
        componentList={listActivities()}
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
