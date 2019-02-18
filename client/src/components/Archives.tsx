import * as React from 'react';

import { getArchivesUrl, getUserUrl } from '../constants/utils';
import Builds from '../containers/builds';
import Experiments from '../containers/experiments';
import Groups from '../containers/groups';
import Jobs from '../containers/jobs';
import Projects from '../containers/projects';
import { ARCHIVES } from '../utils/endpointList';
import Breadcrumb from './breadcrumb';
import LinkedTab from './linkedTab';

export interface Props {
  user: string;
}

export default class Archives extends React.Component<Props, {}> {
  public render() {
    const archivesUrl = getArchivesUrl(this.props.user);

    return (
      <div className="row">
        <div className="col-md-12">
          <Breadcrumb
            icon="fa-archive"
            links={[
              {name: this.props.user, value: getUserUrl(this.props.user)},
              {name: 'archives'}]}
          />
          <LinkedTab
            baseUrl={archivesUrl}
            tabs={[
              {
                title: 'Experiments',
                component: <Experiments
                  user={this.props.user}
                  endpointList={ARCHIVES}
                  useFilters={false}
                  showBookmarks={false}
                  useCheckbox={false}
                  showDeleted={true}
                />,
                relUrl: 'experiments'
              }, {
                title: 'Experiment groups',
                component: <Groups
                  user={this.props.user}
                  endpointList={ARCHIVES}
                  useFilters={false}
                  showBookmarks={false}
                  showDeleted={true}
                />,
                relUrl: 'groups'
              }, {
                title: 'Jobs',
                component: <Jobs
                  user={this.props.user}
                  endpointList={ARCHIVES}
                  useFilters={false}
                  showBookmarks={false}
                  showDeleted={true}
                />,
                relUrl: 'jobs'
              }, {
                title: 'Builds',
                component: <Builds
                  user={this.props.user}
                  endpointList={ARCHIVES}
                  useFilters={false}
                  showBookmarks={false}
                  showDeleted={true}
                />,
                relUrl: 'builds'
              }, {
                title: 'Projects',
                component: <Projects user={this.props.user} endpointList={ARCHIVES} showDeleted={true}/>,
                relUrl: 'Projects'
              }
            ]}
          />
        </div>
      </div>
    );
  }
}
