import * as React from 'react';

import { getNotebookUrl, } from '../../constants/utils';
import HrefMetaInfo from './hrefMetaInfo';

export interface Props {
  project: string;
  inline?: boolean;
}

function NotebookTargetMetaInfo({project, inline = false}: Props) {
  return (
    <HrefMetaInfo
      icon="fas fa-link"
      name="Notebook"
      value="Link"
      link={getNotebookUrl(project)}
      inline={inline}
    />
  );
}

export default NotebookTargetMetaInfo;
