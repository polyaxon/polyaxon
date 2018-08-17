import * as React from 'react';
import { ConfigInterface } from '../interfaces/config';

export interface Props {
  config?: ConfigInterface;
}

function Preview({config}: Props) {
  return (
    <div className="columns">
      <div className="column is-8 is-offset-2">
        <div className="content">
          {JSON.stringify(config, null, ' ')}
        </div>
      </div>
    </div>
  );
}

export default Preview;
