import * as React from 'react';

import TensorboardLinkMetaInfo from './tensorboardLinkMetaInfo';
import TensorboardTargetMetaInfo from './tensorboardTargetMetaInfo';

export interface Props {
  username: string;
  projectName: string;
  project: string;
  experiment?: string | number;
  group?: string | number;
  inline?: boolean;
}

function TensorboardInfoMetaInfo({
                                   username,
                                   projectName,
                                   project,
                                   experiment,
                                   group,
                                   inline = false
                                 }: Props) {
  return (
    <>
      <TensorboardLinkMetaInfo
        username={username}
        projectName={projectName}
        project={project}
        experiment={experiment}
        group={group}
        inline={inline}
      />
      <TensorboardTargetMetaInfo
        username={username}
        projectName={projectName}
        project={project}
        experiment={experiment}
        group={group}
        inline={inline}
      />
    </>
  );
}

export default TensorboardInfoMetaInfo;
