import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import { getProjectUrl } from '../constants/utils';
import { ProjectModel } from '../models/project';
import Actions from './actions';
import Description from './description';
import DatesMetaInfo from './metaInfo/datesMetaInfo';
import MetaInfo from './metaInfo/metaInfo';
import Tags from './tags';

export interface Props {
  project: ProjectModel;
  onDelete: () => void;
}

function Project({project, onDelete}: Props) {
  const visibility = project.is_public ? 'Public' : 'Private';
  return (
    <tr className="list-item">
      <td className="block">
        <LinkContainer to={getProjectUrl(project.user, project.name)}>
          <a className="title">
            <i className="fa fa-server icon" aria-hidden="true"/>
            {project.name}
          </a>
        </LinkContainer>
        <Description description={project.description}/>
        <Tags tags={project.tags} />
      </td>

      <td className="block">
        <MetaInfo
          icon="fa-lock"
          name="Visibility"
          value={visibility}
        />
        <DatesMetaInfo createdAt={project.created_at} updatedAt={project.updated_at}/>
      </td>
      <td className="block">
        <Actions
          onDelete={onDelete}
          isRunning={false}
        />
      </td>
    </tr>
  );
}

export default Project;
