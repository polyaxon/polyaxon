import * as React from 'react';
import './description.less';

export interface Props {
  description?: string;
  command?: string;
  entity?: string;
}

function Description({description, entity, command}: Props) {
  function getDescription() {
    if (description) {
      return description;
    }
    if (command && entity) {
      return (
        <div>
          <p>No description!</p>

          <p>You can add a description to this {entity} by using CLI: <b> {command} </b></p>
        </div>
      );
    }
    return (null);
  }

  return (
    <div className="description">
      {getDescription()}
    </div>
  );
}

export default Description;
