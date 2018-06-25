import * as React from 'react';

import './text.less';

export interface Props {
  title: string;
  text: string;
}

function Text({text, title}: Props) {
  function getText() {
    if (text) {
      return (
        <div className="text">
          <div className="row">
            <div className="col-md-12">
              <div className="text-header">
                {title}
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col-md-12">
              <div className="text-content">
                {text}
              </div>
            </div>
          </div>
        </div>
      );
    }
    return (null);
  }

  return (getText());
}

export default Text;
