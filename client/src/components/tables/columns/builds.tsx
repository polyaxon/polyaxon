import * as React from 'react';
import { Link } from 'react-router-dom';

import * as actions from '../../../actions/builds';
import { getBuildUrl, splitUniqueName } from '../../../constants/utils';
import { BookmarkInterface } from '../../../interfaces/bookmarks';
import { ColumnInterface } from '../../../interfaces/tableColumns';
import { BuildModel } from '../../../models/build';
import { getBookmark } from '../../../utils/bookmarks';
import BookmarkStar from '../../bookmarkStar';
import Description from '../../description';
import BackendMetaInfo from '../../metaInfo/backendMetaInfo';
import DatesMetaInfo from '../../metaInfo/datesMetaInfo';
import IdMetaInfo from '../../metaInfo/idMetaInfo';
import PodIdMetaInfo from '../../metaInfo/podIdMetaInfo';
import UserMetaInfo from '../../metaInfo/userMetaInfo';
import Tags from '../../tags/tags';
import { getBaseGlobalRunColumnOptions, getBaseRunColumnOptions } from './base';
import { FILTER_EXAMPLES } from './examples';

export interface Props {
  showBookmarks: boolean;
  onDelete: (buildName: string) => actions.BuildAction;
  onStop: (buildName: string) => actions.BuildAction;
  onArchive: (buildName: string) => actions.BuildAction;
  onRestore: (buildName: string) => actions.BuildAction;
  bookmark: (buildName: string) => actions.BuildAction;
  unbookmark: (buildName: string) => actions.BuildAction;
}

const getExtraColumnOptions = (props: Props): { [key: string]: ColumnInterface } => {
  return {
    name: {
      name: 'Name',
      field: 'name',
      type: 'value',
      desc: FILTER_EXAMPLES.name('name'),
      sort: true,
      icon: 'fas fa-gavel',
      render: (text: any, build: BuildModel) => {
        const values = splitUniqueName(build.project);
        return (
          <Link className="title" to={getBuildUrl(values[0], values[1], build.id)}>
            <i className="fas fa-gavel icon" aria-hidden="true"/>  {build.name || build.unique_name}
          </Link>);
      },
    },
    build: {
      name: 'Build',
      field: 'name',
      type: 'value',
      desc: FILTER_EXAMPLES.name('name'),
      sort: false,
      icon: 'fas fa-minus',
      render: (text: any, build: BuildModel) => {
        const values = splitUniqueName(build.project);
        const bookmarkStar: BookmarkInterface = getBookmark(
          build.bookmarked,
          () => props.bookmark(build.unique_name),
          () => props.unbookmark(build.unique_name));
        return (
          <div className="block">
            <span>
            <Link className="title" to={getBuildUrl(values[0], values[1], build.id)}>
              <i className="fas fa-gavel icon" aria-hidden="true"/>
              {build.name || build.unique_name}
            </Link>
            {props.showBookmarks &&
            <BookmarkStar active={bookmarkStar.active} callback={bookmarkStar.callback}/>
            }
            <br/>
            </span>
            <Description description={build.description}/>
            <span className="meta">
              <BackendMetaInfo value={build.backend} inline={true}/>
            </span><br/>
            <span className="meta">
              <PodIdMetaInfo value={build.pod_id} inline={true}/>
            </span><br/>
            <span className="meta">
              <IdMetaInfo value={build.id} inline={true}/>
              <UserMetaInfo user={build.user} inline={true}/>
              <DatesMetaInfo
                createdAt={build.created_at}
                updatedAt={build.updated_at}
                inline={true}
              />
            </span>
            <Tags tags={build.tags}/>
          </div>);
      },
    },
    commit: {
      name: 'Commit',
      field: 'commit',
      type: 'value',
      desc: 'commit: 7afbc6aaf1054d4113b4a740396fb861518da044 or commit: hash1|hash2',
      sort: false,
      icon: 'fas fa-hashtag',
      dataIndex: 'commit',
    },
  };
};

export const getBuildColumnOptions = (props: Props): { [key: string]: ColumnInterface } => {
  return {
    ...getBaseRunColumnOptions(),
    ...getExtraColumnOptions(props)
  };
};

export const getBuildGlobalColumnOptions = (props: Props): { [key: string]: ColumnInterface } => {
  return {
  ...getBaseGlobalRunColumnOptions(),
  ...getExtraColumnOptions(props)
  };
};

export const BUILD_PINNED_COLUMNS = ['status', 'build', 'run'];
