import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import * as actions from '../../actions/project';
import { getProjectUrl } from '../../constants/utils';
import { BookmarkInterface } from '../../interfaces/bookmarks';
import { ProjectModel } from '../../models/project';
import { getBookmark } from '../../utils/bookmarks';
import BookmarkStar from '../bookmarkStar';
import Description from '../description';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import MetaInfo from '../metaInfo/metaInfo';
import Tags from '../tags';
import ProjectActions from './projectActions';

export interface Props {
  project: ProjectModel;
  onDelete: () => actions.ProjectAction;
  onArchive: () => actions.ProjectAction;
  onRestore: () => actions.ProjectAction;
  showBookmarks: boolean;
  bookmark: () => actions.ProjectAction;
  unbookmark: () => actions.ProjectAction;
}

function Project({
                   project,
                   onDelete,
                   onArchive,
                   onRestore,
                   bookmark,
                   unbookmark,
                   showBookmarks
                 }: Props) {
  const visibility = project.is_public ? 'Public' : 'Private';
  const bookmarkStar: BookmarkInterface = getBookmark(
    project.bookmarked, bookmark, unbookmark);
  return (
    <tr className="list-item">
      <td className="block">
        <LinkContainer to={getProjectUrl(project.user, project.name)}>
          <a className="title">
            <i className="fa fa-server icon" aria-hidden="true"/>
            {project.name}
          </a>
        </LinkContainer>
        {showBookmarks &&
        <BookmarkStar active={bookmarkStar.active} callback={bookmarkStar.callback}/>
        }
        <Description description={project.description}/>
        <Tags tags={project.tags}/>
      </td>

      <td className="block">
        <MetaInfo
          icon="fa-lock"
          name="Visibility"
          value={visibility}
        />
        <DatesMetaInfo createdAt={project.created_at} updatedAt={project.updated_at}/>
      </td>
      <td className="block pull-right">
        <ProjectActions
          onDelete={onDelete}
          onArchive={project.deleted ? undefined : onArchive}
          onRestore={project.deleted ? onRestore : undefined}
          pullRight={false}
        />
      </td>
    </tr>
  );
}

export default Project;
