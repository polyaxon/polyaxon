import * as React from 'react';

import Builds from '../containers/builds/builds';
import Experiments from '../containers/experiments/experiments';
import Groups from '../containers/groups/groups';
import Jobs from '../containers/jobs/jobs';
import Projects from '../containers/projects/projects';
import { getBookmarksUrl, getUserUrl } from '../urls/utils';
import { BOOKMARKS } from '../utils/endpointList';
import Breadcrumb from './breadcrumb';
import LinkedTab from './linkedTab';

export interface Props {
  user: string;
}

export default class Bookmarks extends React.Component<Props, {}> {
  public render() {
    const bookmarksUrl = getBookmarksUrl(this.props.user);

    return (
      <div className="row">
        <div className="col-md-12">
          <Breadcrumb
            icon="fas fa-star"
            links={[
              {name: this.props.user, value: getUserUrl(this.props.user)},
              {name: 'bookmarks'}]}
          />
          <LinkedTab
            baseUrl={bookmarksUrl}
            tabs={[
              {
                title: 'Experiments',
                component: <Experiments
                  user={this.props.user}
                  endpointList={BOOKMARKS}
                  useFilters={false}
                  showBookmarks={false}
                  useCheckbox={false}
                />,
                relUrl: 'experiments'
              }, {
                title: 'Experiment groups',
                component: <Groups
                  user={this.props.user}
                  endpointList={BOOKMARKS}
                  useFilters={false}
                  showBookmarks={false}
                />,
                relUrl: 'groups'
              }, {
                title: 'Jobs',
                component: <Jobs
                  user={this.props.user}
                  endpointList={BOOKMARKS}
                  useFilters={false}
                  showBookmarks={false}
                />,
                relUrl: 'jobs'
              }, {
                title: 'Builds',
                component: <Builds
                  user={this.props.user}
                  endpointList={BOOKMARKS}
                  useFilters={false}
                  showBookmarks={false}
                />,
                relUrl: 'builds'
              }, {
                title: 'Projects',
                component: <Projects user={this.props.user} endpointList={BOOKMARKS}/>,
                relUrl: 'Projects'
              }
            ]}
          />
        </div>
      </div>
    );
  }
}
