import * as React from 'react';

import LinkMetaInfo from './linkMetaInfo';
import { getExperimentUrl, getGroupUrl, getProjectUrl } from '../../constants/utils';

export interface Props {
  username: string;
  projectName: string;
  project: string;
  experiment?: string | number;
  group?: string | number;
  inline?: boolean;
}

function TensorboardLinkMetaInfo({
                                   username,
                                   projectName,
                                   project,
                                   experiment,
                                   group,
                                   inline = false
                                 }: Props) {
  return (
    <>
      {experiment &&
      <LinkMetaInfo
        icon="fas fa-cube"
        name="Experiment"
        value={experiment.toString()}
        link={getExperimentUrl(username, projectName, experiment)}
        inline={inline}
      />
      }
      {group &&
      <LinkMetaInfo
        icon="fas fa-cubes"
        name="Group"
        value={group.toString()}
        link={getGroupUrl(username, projectName, group)}
        inline={inline}
      />
      }
      {!(experiment || group) &&
      <LinkMetaInfo
        icon="fas fa-server"
        name="Project"
        value={project}
        link={getProjectUrl(username, projectName)}
        inline={inline}
      />
      }
    </>
  );
}

export default TensorboardLinkMetaInfo;
