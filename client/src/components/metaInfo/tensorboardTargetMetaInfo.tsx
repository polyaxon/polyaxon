import * as React from 'react';

import {
  getExperimentTensorboardUrl,
  getGroupTensorboardUrl,
  getProjectTensorboardUrl,
} from '../../constants/utils';
import HrefMetaInfo from './hrefMetaInfo';

export interface Props {
  username: string;
  projectName: string;
  project: string;
  experiment?: string | number;
  group?: string | number;
  inline?: boolean;
}

function TensorboardTargetMetaInfo({
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
      <HrefMetaInfo
        icon="fas fa-link"
        name="Tensorboard"
        value="Link"
        link={getExperimentTensorboardUrl(project, experiment)}
        inline={inline}
      />
      }
      {group &&
      <HrefMetaInfo
        icon="fas fa-link"
        name="Tensorboard"
        value="Link"
        link={getGroupTensorboardUrl(project, group)}
        inline={inline}
      />
      }
      {!(experiment || group) &&
      <HrefMetaInfo
        icon="fas fa-link"
        name="Tensorboard"
        value="Link"
        link={getProjectTensorboardUrl(project)}
        inline={inline}
      />
      }
    </>
  );
}

export default TensorboardTargetMetaInfo;
