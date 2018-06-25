import * as React from 'react';
import './description.less';

export interface Props {
  description?: string;
  showEmpty?: boolean;
}

function Description({description, showEmpty = false}: Props) {
  function getDescription() {
    if (description) {
      return description;
    }
    if (showEmpty) {
      return (
        <div>
          <p>No description!</p>
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
