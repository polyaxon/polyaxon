import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import { ProjectModel } from '../models/project';
import { getProjectUrl } from '../constants/utils';
import Tags from './tags';
import Description from './description';
import MetaInfo from './metaInfo/metaInfo';
import DatesMetaInfo from './metaInfo/datesMetaInfo';

export interface Props {
  project: ProjectModel;
  onDelete: () => void;
}

function Project({project, onDelete}: Props) {
  let visibility = project.is_public ? 'Public' : 'Private';
  return (
    <div className="row">
      <div className="col-md-10 block">
        <LinkContainer to={getProjectUrl(project.user, project.name)}>
          <a className="title">
            <i className="fa fa-server icon" aria-hidden="true"/>
            {project.name}
          </a>
        </LinkContainer>
        <Description description={project.description}/>
        <Tags tags={project.tags} />
      </div>

      <div className="col-md-2 block">
        <MetaInfo
          icon="fa-lock"
          name="Visibility"
          value={visibility}
        />
        <DatesMetaInfo createdAt={project.created_at} updatedAt={project.updated_at}/>
      </div>
    </div>
  );
}

export default Project;
