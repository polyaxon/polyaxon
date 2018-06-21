import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';
import * as moment from 'moment';

import { ProjectModel } from '../models/project';
import { getProjectUrl } from '../constants/utils';
import Tags from './tags';
import Description from './description';
import MetaInfo from './metaInfo';

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
          row={true}
        />
        <MetaInfo
          icon="fa-clock-o"
          name="Created at"
          value={moment(project.created_at).fromNow()}
          row={true}
        />
        <MetaInfo
          icon="fa-clock-o"
          name="Last updated"
          value={moment(project.updated_at).fromNow()}
          row={true}
        />
      </div>
    </div>
  );
}

export default Project;
